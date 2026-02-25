from __future__ import annotations

from typing import Any

ALLOWED_ACCOUNT_TYPES = {"401k", "roth_ira", "traditional_ira", "taxable"}
ALLOWED_INCOME_TYPES = {"w2", "1099", "dividend"}
ALLOWED_STATE_CODES = {"MA", "CA"}


class ValidationError(ValueError):
    """Raised when plan JSON is missing required fields or has invalid values."""


def _type_name(expected_type: Any) -> str:
    if isinstance(expected_type, tuple):
        return " or ".join(t.__name__ for t in expected_type)
    return expected_type.__name__


def _require(mapping: dict[str, Any], key: str, expected_type: Any, path: str) -> Any:
    if key not in mapping:
        raise ValidationError(f"Missing required field: {path}.{key}")
    value = mapping[key]
    if not isinstance(value, expected_type):
        raise ValidationError(f"Invalid type for {path}.{key}: expected {_type_name(expected_type)}")
    return value


def validate_plan(data: dict[str, Any]) -> None:
    household = _require(data, "household", dict, "root")
    spouses = _require(household, "spouses", list, "root.household")
    if len(spouses) != 2:
        raise ValidationError("root.household.spouses must contain exactly 2 spouses")

    spouse_names = set()
    for idx, spouse in enumerate(spouses):
        if not isinstance(spouse, dict):
            raise ValidationError(f"root.household.spouses[{idx}] must be an object")
        name = _require(spouse, "name", str, f"root.household.spouses[{idx}]")
        spouse_names.add(name)
        _require(spouse, "current_age", int, f"root.household.spouses[{idx}]")
        _require(spouse, "retirement_age", int, f"root.household.spouses[{idx}]")
        _require(spouse, "death_age", int, f"root.household.spouses[{idx}]")

    assumptions = _require(data, "assumptions", dict, "root")
    start_year = _require(assumptions, "start_year", int, "root.assumptions")
    years = _require(assumptions, "years", int, "root.assumptions")
    _require(assumptions, "inflation_rate", (int, float), "root.assumptions")
    _require(assumptions, "w2_growth_rate", (int, float), "root.assumptions")
    _require(assumptions, "w2_401k_contribution_rate", (int, float), "root.assumptions")
    _require(assumptions, "tax_year", int, "root.assumptions")
    if years <= 0:
        raise ValidationError("root.assumptions.years must be > 0")

    taxes = _require(data, "taxes", dict, "root")
    state = _require(taxes, "state", str, "root.taxes")
    if state not in ALLOWED_STATE_CODES:
        raise ValidationError(f"root.taxes.state must be one of {sorted(ALLOWED_STATE_CODES)}")

    accounts = _require(data, "accounts", list, "root")
    if not accounts:
        raise ValidationError("root.accounts must not be empty")
    for idx, account in enumerate(accounts):
        if not isinstance(account, dict):
            raise ValidationError(f"root.accounts[{idx}] must be an object")
        acct_type = _require(account, "type", str, f"root.accounts[{idx}]")
        if acct_type not in ALLOWED_ACCOUNT_TYPES:
            raise ValidationError(
                f"root.accounts[{idx}].type must be one of {sorted(ALLOWED_ACCOUNT_TYPES)}"
            )
        _require(account, "name", str, f"root.accounts[{idx}]")
        _require(account, "balance", (int, float), f"root.accounts[{idx}]")
        _require(account, "growth_rate", (int, float), f"root.accounts[{idx}]")


    has_401k = any(a.get("type") == "401k" for a in accounts)
    has_taxable = any(a.get("type") == "taxable" for a in accounts)
    if not has_401k:
        raise ValidationError("root.accounts must include at least one 401k account")
    if not has_taxable:
        raise ValidationError("root.accounts must include at least one taxable account")

    incomes = _require(data, "incomes", list, "root")
    for idx, income in enumerate(incomes):
        if not isinstance(income, dict):
            raise ValidationError(f"root.incomes[{idx}] must be an object")
        income_type = _require(income, "type", str, f"root.incomes[{idx}]")
        if income_type not in ALLOWED_INCOME_TYPES:
            raise ValidationError(
                f"root.incomes[{idx}].type must be one of {sorted(ALLOWED_INCOME_TYPES)}"
            )
        _require(income, "amount", (int, float), f"root.incomes[{idx}]")
        spouse = _require(income, "spouse", str, f"root.incomes[{idx}]")
        if spouse not in spouse_names:
            raise ValidationError(
                f"root.incomes[{idx}].spouse must match one of household spouse names: {sorted(spouse_names)}"
            )
        inc_start = _require(income, "start_year", int, f"root.incomes[{idx}]")
        inc_end = _require(income, "end_year", int, f"root.incomes[{idx}]")
        if inc_end < inc_start:
            raise ValidationError(f"root.incomes[{idx}].end_year must be >= start_year")
        model_end = start_year + years - 1
        if inc_end < start_year or inc_start > model_end:
            raise ValidationError(
                f"root.incomes[{idx}] active years must overlap model window {start_year}-{model_end}"
            )

    spending = _require(data, "spending", dict, "root")
    _require(spending, "base_annual", (int, float), "root.spending")
    _require(data, "withdrawal_order", list, "root")

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .tax import estimate_rmd, federal_tax_mfj_2026, state_income_tax

SCENARIO_RETURN_ADJUST = {
    "worst": -0.02,
    "average": 0.00,
    "best": 0.02,
}


@dataclass
class ProjectionResult:
    years: list[int]
    account_balances: dict[str, list[float]]
    spending_by_source: dict[str, list[float]]


def _income_label(income: dict[str, Any], idx: int) -> str:
    return (
        f"{income['type']}:{income['spouse']}"
        f":{income['start_year']}-{income['end_year']}#{idx + 1}"
    )


def _income_components_for_year(
    incomes: list[dict[str, Any]],
    current_year: int,
    w2_growth_rate: float,
) -> tuple[dict[str, float], float]:
    components: dict[str, float] = {}
    total_w2_income = 0.0

    for idx, income in enumerate(incomes):
        if current_year < income["start_year"] or current_year > income["end_year"]:
            continue

        amount = float(income["amount"])
        if income["type"] == "w2":
            growth_years = current_year - int(income["start_year"])
            effective_amount = amount * ((1 + w2_growth_rate) ** growth_years)
            total_w2_income += effective_amount
        else:
            effective_amount = amount

        components[_income_label(income, idx)] = effective_amount

    return components, total_w2_income


def run_plan(plan: dict[str, Any], scenario: str) -> ProjectionResult:
    assumptions = plan["assumptions"]
    years = assumptions["years"]
    start_year = assumptions["start_year"]
    inflation = assumptions["inflation_rate"]
    w2_growth = assumptions["w2_growth_rate"]
    w2_401k_contrib_rate = assumptions["w2_401k_contribution_rate"]

    balances = {a["name"]: float(a["balance"]) for a in plan["accounts"]}
    account_types = {a["name"]: a["type"] for a in plan["accounts"]}
    growth_rates = {
        a["name"]: float(a["growth_rate"]) + SCENARIO_RETURN_ADJUST.get(scenario, 0.0)
        for a in plan["accounts"]
    }

    taxable_account_name = next(name for name, acc_type in account_types.items() if acc_type == "taxable")
    first_401k_name = next(name for name, acc_type in account_types.items() if acc_type == "401k")

    withdrawal_order = plan["withdrawal_order"]
    base_spending = float(plan["spending"]["base_annual"])
    state = plan["taxes"]["state"]
    oldest_age = max(s["current_age"] for s in plan["household"]["spouses"])

    income_labels = [_income_label(income, idx) for idx, income in enumerate(plan["incomes"])]
    income_labels.append("rmd")

    yearly_years = []
    account_balances = {acct: [] for acct in balances}
    spending_sources = {label: [] for label in income_labels}
    for acct in balances:
        spending_sources[acct] = []

    for i in range(years):
        year = start_year + i
        yearly_years.append(year)

        for acct in balances:
            balances[acct] *= 1 + growth_rates[acct]

        gross_components, w2_income = _income_components_for_year(plan["incomes"], year, w2_growth)
        employee_401k_contribution = w2_income * w2_401k_contrib_rate
        balances[first_401k_name] += employee_401k_contribution

        current_age = oldest_age + i
        traditional_total = sum(
            bal for name, bal in balances.items() if account_types[name] in {"401k", "traditional_ira"}
        )
        rmd = estimate_rmd(current_age, traditional_total)

        taxable_components = {**gross_components}
        taxable_components["rmd"] = rmd

        if employee_401k_contribution > 0 and w2_income > 0:
            for label in list(taxable_components):
                if label.startswith("w2:"):
                    w2_share = taxable_components[label] / w2_income
                    taxable_components[label] -= employee_401k_contribution * w2_share

        taxable_income = max(0.0, sum(taxable_components.values()))
        federal = federal_tax_mfj_2026(taxable_income)
        state_tax = state_income_tax(state, taxable_income)
        post_tax_income = max(0.0, taxable_income - federal - state_tax)

        net_income_components = {label: 0.0 for label in income_labels}
        if taxable_income > 0:
            for label in taxable_components:
                net_income_components[label] = post_tax_income * (taxable_components[label] / taxable_income)

        required_spending = base_spending * ((1 + inflation) ** i)
        remaining = required_spending

        for label in income_labels:
            available = net_income_components.get(label, 0.0)
            used = min(remaining, available)
            spending_sources[label].append(used)
            remaining -= used

        for acct in balances:
            spending_sources[acct].append(0.0)

        for acct_name in withdrawal_order:
            if remaining <= 0:
                break
            if acct_name not in balances:
                continue
            draw = min(remaining, balances[acct_name])
            balances[acct_name] -= draw
            spending_sources[acct_name][-1] += draw
            remaining -= draw

        income_spent = sum(spending_sources[label][-1] for label in income_labels)
        surplus_cash = max(0.0, post_tax_income - income_spent)
        balances[taxable_account_name] += surplus_cash

        for acct, balance in balances.items():
            account_balances[acct].append(balance)

    return ProjectionResult(
        years=yearly_years,
        account_balances=account_balances,
        spending_by_source=spending_sources,
    )

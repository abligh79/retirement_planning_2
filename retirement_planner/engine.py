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


def _income_for_year(incomes: list[dict[str, Any]], current_year: int, w2_growth_rate: float) -> float:
    total = 0.0
    for income in incomes:
        if current_year < income["start_year"] or current_year > income["end_year"]:
            continue
        amount = float(income["amount"])
        if income["type"] == "w2":
            growth_years = current_year - int(income["start_year"])
            total += amount * ((1 + w2_growth_rate) ** growth_years)
        else:
            total += amount
    return total


def run_plan(plan: dict[str, Any], scenario: str) -> ProjectionResult:
    assumptions = plan["assumptions"]
    years = assumptions["years"]
    start_year = assumptions["start_year"]
    inflation = assumptions["inflation_rate"]
    w2_growth = assumptions["w2_growth_rate"]

    balances = {a["name"]: float(a["balance"]) for a in plan["accounts"]}
    account_types = {a["name"]: a["type"] for a in plan["accounts"]}
    growth_rates = {
        a["name"]: float(a["growth_rate"]) + SCENARIO_RETURN_ADJUST.get(scenario, 0.0)
        for a in plan["accounts"]
    }

    withdrawal_order = plan["withdrawal_order"]
    base_spending = float(plan["spending"]["base_annual"])
    state = plan["taxes"]["state"]
    oldest_age = max(s["current_age"] for s in plan["household"]["spouses"])

    yearly_years = []
    account_balances = {acct: [] for acct in balances}
    spending_sources = {acct: [] for acct in balances}
    spending_sources["income"] = []

    for i in range(years):
        year = start_year + i
        yearly_years.append(year)

        for acct in balances:
            balances[acct] *= 1 + growth_rates[acct]

        total_income = _income_for_year(plan["incomes"], year, w2_growth)
        required_spending = base_spending * ((1 + inflation) ** i)

        current_age = oldest_age + i
        traditional_total = sum(
            bal for name, bal in balances.items() if account_types[name] in {"401k", "traditional_ira"}
        )
        rmd = estimate_rmd(current_age, traditional_total)
        total_income += rmd

        federal = federal_tax_mfj_2026(total_income)
        state_tax = state_income_tax(state, total_income)
        post_tax_income = max(0.0, total_income - federal - state_tax)

        remaining = required_spending
        from_income = min(remaining, post_tax_income)
        spending_sources["income"].append(from_income)
        remaining -= from_income

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

        for acct, balance in balances.items():
            account_balances[acct].append(balance)

    return ProjectionResult(years=yearly_years, account_balances=account_balances, spending_by_source=spending_sources)

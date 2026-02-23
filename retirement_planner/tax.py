from __future__ import annotations

FEDERAL_BRACKETS_MFJ_2026 = [
    (0, 0.10),
    (23_200, 0.12),
    (94_300, 0.22),
    (201_050, 0.24),
    (383_900, 0.32),
    (487_450, 0.35),
    (731_200, 0.37),
]

STATE_FLAT_TAX = {
    "MA": 0.05,
    "CA": 0.09,
}


def federal_tax_mfj_2026(taxable_income: float) -> float:
    tax = 0.0
    if taxable_income <= 0:
        return tax
    for i, (threshold, rate) in enumerate(FEDERAL_BRACKETS_MFJ_2026):
        next_threshold = (
            FEDERAL_BRACKETS_MFJ_2026[i + 1][0]
            if i + 1 < len(FEDERAL_BRACKETS_MFJ_2026)
            else taxable_income
        )
        if taxable_income > threshold:
            taxable_at_rate = min(taxable_income, next_threshold) - threshold
            tax += taxable_at_rate * rate
    return max(tax, 0.0)


def state_income_tax(state: str, taxable_income: float) -> float:
    rate = STATE_FLAT_TAX.get(state, 0.0)
    return max(taxable_income, 0.0) * rate


def estimate_rmd(age: int, traditional_balance: float) -> float:
    if age < 73:
        return 0.0
    return max(traditional_balance, 0.0) / 26.5

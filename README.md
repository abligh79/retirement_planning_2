# Retirement Planning App (Local Python MVP)

This repository now includes an initial runnable Python scaffold for the retirement planner plus the discovery requirements.

## Current Status

- Discovery requirements are tracked in `discovery_questionnaire.md` (v0.4).
- A first CLI implementation is available in `retirement_planner/`.
- The CLI validates input JSON (fail-fast) and generates yearly PNG charts for worst/average/best scenarios.

## Implemented MVP Foundations

- JSON input loading and validation.
- Support for account types: `401k`, `roth_ira`, `traditional_ira`, `taxable`.
- Support for income types: `w2`, `1099`, `dividend` (including multiple W-2 and 1099 entries).
- W-2 salary growth-rate assumption and per-income active windows (`start_year`/`end_year`).
- W-2 employee 401(k) contribution allocation via `assumptions.w2_401k_contribution_rate`.
- Post-tax surplus cash (after spending + tax + 401(k) contribution effects) is deposited into the taxable account.
- Tax scaffolding for federal + state support (`MA`, `CA`) with tax year baseline `2026`.
- RMD handling for applicable traditional balances.
- PNG chart outputs:
  - `account_values_<scenario>.png`
  - `spending_sources_<scenario>.png`

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m retirement_planner --input sample_plan.json --output out

# optional: run a single scenario
python -m retirement_planner --input sample_plan.json --output out --scenario average
```


## Spending Chart Behavior

- The `spending_sources_<scenario>.png` chart shows **only sources used to fund annual spending**, split into each configured income stream (`w2`, `1099`, `dividend`) plus `rmd`, and then account withdrawals if needed.
- Income is used first (after tax/401(k) treatment), then remaining spending is funded from accounts using `withdrawal_order`.
- If post-tax income exceeds annual spending, the surplus is **not plotted as spending**; it is reinvested into the taxable account balance.

## Repository Contents

- `discovery_questionnaire.md` — requirements and decisions.
- `sample_plan.json` — example input for local runs.
- `requirements.txt` — Python dependencies.
- `retirement_planner/` — initial planner CLI and projection/chart modules.

## Next Build Steps

1. Replace simplified tax scaffolding with full tax-engine detail for 2026 tables and richer state logic.
2. Add contribution and employer-match phase modeling with work/retirement transitions by spouse.
3. Add per-account withdrawal tax treatment and RMD reinvestment behavior.
4. Add spouse-level income reporting views and richer chart outputs.
5. Define formal JSON schema and add automated tests.

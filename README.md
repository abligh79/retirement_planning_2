# Retirement Planning App (Local Python MVP)

This repository contains the discovery and planning artifacts for a **locally executed Python retirement planning app** focused on a single married couple in the U.S.

## Current Project Status

The project is currently in the **requirements and design-definition phase**. The detailed MVP scope, assumptions, and implementation decisions are captured in:

- `discovery_questionnaire.md`

## MVP Goals

The initial version is intended to:

1. Support **early retirement planning**.
2. Include key **federal employee concepts** (FERS, TSP, FEHB, Social Security supplement).
3. Produce **yearly graphical outputs** from local Python execution.

## Key Product Decisions (v0.4)

- Input format: **JSON** (no account-linking integrations).
- Modeling approach: **deterministic scenarios** (best / average / worst).
- Tax scope: **U.S. federal bracket logic with filing status**, plus state tax support for at least two states (including **MA**).
- Initial tax-year baseline: **2026**.
- Withdrawal behavior: **user-configurable in input JSON**.
- Chart outputs: **PNG files**.
- Validation: **fail-fast** on missing/invalid JSON fields.
- Include **RMD handling** for applicable account types.
- Support account coverage for at least **401(k), Roth IRA, Traditional IRA, and taxable investment accounts**.
- Support income coverage for at least **W-2, freelance/1099, and dividend** income, including **W-2 growth-rate assumptions**.

## Repository Contents

- `discovery_questionnaire.md` — consolidated requirements and decision log for v0.4.
- `README.md` — project overview and quick-start orientation.

## Suggested Next Build Steps

1. Define and document a strict JSON schema for all household, income, account, and scenario inputs.
2. Implement input validation that exits with clear error messages on schema violations.
3. Build a deterministic year-by-year projection engine for both spouses across the model horizon.
4. Add federal employee-specific modules (FERS estimate, TSP flows, FEHB assumptions, SS supplement timing).
5. Generate the two primary yearly charts:
   - Account values over time.
   - Spending-source stacked bar chart.

## Local Workflow

Once implementation begins, a typical local workflow can be:

```bash
# 1) Create/activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate

# 2) Install dependencies (to be added during implementation)
pip install -r requirements.txt

# 3) Run the planner (entrypoint to be added)
python -m retirement_planner --input sample_plan.json --output ./out
```

## Contributing

For now, keep changes small and focused, and update `discovery_questionnaire.md` whenever a major requirement or decision changes.

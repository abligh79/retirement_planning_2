# Retirement Planning App — Requirements (v0.4)

This document captures confirmed requirements and implementation decisions for a **locally executed Python retirement planning app**.

## Confirmed Requirements

### 1) Users & Personas
- Primary users are a **single married couple**.
- No advisor/admin multi-client scope for v1.

### 2) Data Input
- No automatic account linking.
- The app uses an **easy-to-use input document** that captures all required planning data.
- **Input format for v1: JSON**.

### 3) Planning Method
- No stochastic / Monte Carlo requirement for v1.
- The app should support exploration of a variety of deterministic scenarios based on user-provided assumptions.
- The app should provide at least these scenario outputs:
  - **Best case**
  - **Average case**
  - **Worst case**

### 4) Jurisdiction
- Tax/rules scope starts with the **United States**.

### 5) Platform & Execution
- Local execution of Python only.
- No required hosted web/mobile deployment in v1.

### 6) Top MVP Features
1. Support **early retirement planning**.
2. Include concepts specific to **U.S. federal employees**.
3. Produce **graphical output** from locally run Python.

## Federal Employee Requirements (v1)
All of the following are in-scope for v1:
- **FERS pension estimate**
- **TSP contribution/match modeling**
- **401(k) employer-match modeling** (in addition to TSP matching)
- **FEHB healthcare cost assumptions**
- **Social Security supplement assumptions**

## Tax Requirements (v1)
- Implement **detailed U.S. federal bracket logic** and filing-status logic.
- Include **state income tax support for at least two states**, with **Massachusetts (MA)** required as one supported state.
- Start with **tax year 2026** assumptions/tables.
- Include **RMD (Required Minimum Distribution)** handling for applicable account types.

## Account & Income Modeling Requirements (v1)
- Support multiple account types, including at least:
  - **401(k)**
  - **Roth IRA**
  - **Traditional IRA**
  - **Taxable investment account**
- Support multiple income types, including at least:
  - **W-2 wage income**
  - **Freelance / 1099 income**
  - **Dividend income**
- Include a configurable **growth rate for W-2 salary** over time.

## Scenario & Assumption Coverage
Scenario exploration should support changes in:
- Investment returns
- Spending levels/patterns
- Inflation
- Other user-provided variables (extensible assumption set)

## Time Horizon & Household Modeling
- Spouses can have different:
  - Starting ages
  - Stop-working / retirement ages
  - Expected death ages
- Planning horizon should support roughly **65 years of modeling**.

## Required Graphical Outputs (Critical)
The following yearly charts are required in v1:
1. **Account values over time** (yearly).
2. **Spending source breakdown over time** (yearly), showing where spending is funded from (accounts and/or income sources), preferably as a **stacked bar chart**.

## Proposed v1 Deliverables
- Python CLI entrypoint to run a plan from local JSON input.
- Validated JSON input schema for household, assets, income, expenses, federal-employee details, and assumptions.
- Deterministic projections for best/average/worst and custom scenarios.
- Yearly visualization outputs for account trajectories and spending-source composition.

## Confirmed Implementation Decisions (v0.4)
1. **Tax detail depth:** Use **detailed U.S. federal tax bracket logic** and filing status logic.
2. **State taxes:** Support at least two state income tax models, including **MA**.
3. **Tax-year baseline:** Start with **2026** tax-year assumptions.
4. **Withdrawal strategy:** Spending-withdrawal order is **user-configurable from the input JSON file**.
5. **Output format:** Generate chart outputs as **PNG files**.
6. **Validation strictness:** Use **fail-fast validation** for missing/invalid JSON fields.
7. **Scenario definitions:** Exact best/average/worst definitions are **TBD** and will be refined during implementation.
8. **Output success criteria:** Detailed pass/fail planning success metrics are **TBD** and will be refined during implementation.

## Initial Decision Log
- Decision: Focus scope on one married-couple household.
  - Rationale: Keep v1 simple and directly aligned with intended users.
- Decision: Use manual/local data entry; no account linking.
  - Rationale: Prioritizes simplicity and local privacy.
- Decision: Use JSON as the v1 input format.
  - Rationale: Explicitly requested and straightforward for local Python workflows.
- Decision: Deterministic best/avg/worst outputs with custom scenario exploration.
  - Rationale: Meets planning needs without adding stochastic complexity.
- Decision: US-only rules for v1.
  - Rationale: Reduce complexity and align to stated need.
- Decision: Local Python execution.
  - Rationale: Matches deployment preference and lowers infrastructure needs.
- Decision: Include federal employee concepts (FERS, TSP, FEHB, SS supplement) in v1.
  - Rationale: Explicit MVP priority.
- Decision: Require yearly account-value and spending-source charts.
  - Rationale: Critical requested outputs for plan analysis.

- Decision: Implement detailed U.S. federal tax bracket and filing-status logic.
  - Rationale: Explicitly requested for v1 tax modeling depth.
- Decision: Add state income tax support for at least two states, including MA.
  - Rationale: Required for more realistic U.S. household projections.
- Decision: Use tax year 2026 as the initial baseline.
  - Rationale: Provides a concrete starting point for coding and validation.
- Decision: Make withdrawal order user-configurable via input JSON.
  - Rationale: Enables scenario flexibility without code changes.
- Decision: Standardize chart output to PNG.
  - Rationale: Clear local artifact format for analysis and sharing.
- Decision: Enforce fail-fast input validation.
  - Rationale: Prevents silent defaults and improves model correctness.
- Decision: Support account types including 401(k), Roth IRA, Traditional IRA, and taxable investment accounts.
  - Rationale: Establishes the minimum account coverage for practical planning.
- Decision: Support income types including W-2, 1099, and dividends, plus W-2 growth-rate assumptions.
  - Rationale: Captures core working-years and investment-income cash flows.
- Decision: Include RMD handling for applicable accounts.
  - Rationale: Required for realistic retirement withdrawal and tax modeling.
- Decision: Leave scenario parameterization details and output success thresholds as TBD.
  - Rationale: These will be finalized through iterative implementation and review.

# Retirement Planning App — Requirements (v0.3)

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
- **FEHB healthcare cost assumptions**
- **Social Security supplement assumptions**

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

## Confirmed Implementation Decisions (v0.3)
1. **Tax detail depth:** Use **detailed U.S. federal tax bracket logic** and filing status logic.
2. **Withdrawal strategy:** Spending-withdrawal order is **user-configurable from the input JSON file**.
3. **Output format:** Generate chart outputs as **PNG files**.
4. **Validation strictness:** Use **fail-fast validation** for missing/invalid JSON fields.

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
- Decision: Make withdrawal order user-configurable via input JSON.
  - Rationale: Enables scenario flexibility without code changes.
- Decision: Standardize chart output to PNG.
  - Rationale: Clear local artifact format for analysis and sharing.
- Decision: Enforce fail-fast input validation.
  - Rationale: Prevents silent defaults and improves model correctness.

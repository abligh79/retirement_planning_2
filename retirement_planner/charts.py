from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from .engine import ProjectionResult


def plot_account_values(result: ProjectionResult, output_dir: Path, scenario: str) -> Path:
    out = output_dir / f"account_values_{scenario}.png"
    plt.figure(figsize=(10, 5))
    plt.plot(result.years, result.total_balances, linewidth=2)
    plt.title(f"Account Values Over Time ({scenario.title()})")
    plt.xlabel("Year")
    plt.ylabel("Total Account Value ($)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def plot_spending_sources(result: ProjectionResult, output_dir: Path, scenario: str) -> Path:
    out = output_dir / f"spending_sources_{scenario}.png"
    labels = list(result.spending_by_source.keys())
    data = [result.spending_by_source[k] for k in labels]

    plt.figure(figsize=(12, 6))
    plt.stackplot(result.years, *data, labels=labels, alpha=0.8)
    plt.title(f"Spending Source Breakdown ({scenario.title()})")
    plt.xlabel("Year")
    plt.ylabel("Annual Spending by Source ($)")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out

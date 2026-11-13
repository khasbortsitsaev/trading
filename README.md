# Crypto Quant Research

Research-first cryptocurrency trading project. The objective is to identify, reproduce where useful, and independently validate systematic trading strategies with **net economic profitability**, then decide whether a paper-trading and live-trading system is justified.

**Status (2026-11-13):** preliminary venue feasibility and spot-cost comparisons completed, with a small cost-accounting calculator and six passing synthetic checks. No strategy backtest, validated alpha, selected exchange, or live trading system exists.

## Agreed constraints
- Initial endowment: **0.5 ETH**, not EUR 500. No arbitrary limit on the number of positions or assets.
- Research/reporting numeraire: **USDC / USD equivalent**, with ETH buy-and-hold and cash benchmarks. Report ETH-equivalent results too.
- Long and short strategies may be researched, but **no leveraged portfolio exposure** is desired. Gross exposure <= 100% of equity is an initial constraint to validate; derivatives and borrowed shorts still introduce margin/liquidation risks.
- No commitment to any specific exchange or execution venue yet. **Bitvavo is the reference behind the initial cost estimate**, not a selected execution venue.
- Focus on returns **after** commissions, spread, slippage, and where applicable borrowing/funding/conversion costs.
- Preserve the original **0.15%, 0.25%, 0.50% all-in round-trip scenarios** as legacy comparisons. Use [verified market-specific fees and explicit friction scenarios](docs/COSTS.md) for new research: entry-tier taker commissions sum to approximately 0.10% for Bitvavo crypto/USDC, 0.50% for Bitvavo crypto/EUR, and 1.60% for current Kraken regular spot. These exclude spread/slippage and do not establish account rates. Do not double-count costs.
- Prefer reproducible, interpretable signals over complex ML for its own sake.
- Academic papers are candidate specifications, **not proof** of profitability for our account.
- No real orders, API-key permissions, or autonomous trading until explicit authorization and a separate safety review.

## Workflow
First complete the six [review priorities](docs/ROADMAP.md): preliminary venue/data feasibility, calibrated costs, decision criteria, shorting constraints, a frozen research protocol, and a data/execution specification. These precede real-data strategy development. Initial scope is fully funded spot; the objective is capital growth with no planned withdrawals.

1. Maintain a broad, evidence-graded literature catalogue; distinguish peer-reviewed research from working papers.
2. Build a reusable Python data and backtesting research platform, not an exchange-connected bot.
3. Implement standalone strategies, then test combinations and alternative portfolio construction.
4. Use chronological nested walk-forward validation; purging/embargo when labels overlap; an untouched final holdout. Track the number of hypotheses tested.
5. Evaluate net compounded return, ETH-relative return, Sharpe/Sortino, drawdown, turnover, capital utilization, and stability across regimes and cost assumptions.
6. Recheck preliminary venue/data feasibility against experiment findings and current access conditions.
7. Only after a research go/no-go decision: prospective paper trading, then optionally a tightly controlled live experiment.

## Documentation
- [Agent working rules](AGENTS.md)
- [Project decisions](docs/DECISIONS.md)
- [Strategy universe](docs/STRATEGIES.md)
- [Research bibliography](docs/PAPERS.md)
- [Validation and costs](docs/METHODOLOGY.md)
- [Development roadmap](docs/ROADMAP.md)
- [Preliminary venue and data feasibility](docs/FEASIBILITY.md)
- [Spot cost analysis and reproducible accounting checks](docs/COSTS.md)

## Research principle
The goal is not to find the best historical backtest. It is to find an economically meaningful, implementable edge that survives out-of-sample testing and realistic costs. A negative result is a valid outcome.

## Validate the cost-accounting helper
From the repository root, run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` (standard library only). These are synthetic accounting checks, not trading-profitability evidence. See docs/COSTS.md for the observed-book methodology and its replay limitations.

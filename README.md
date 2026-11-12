# Crypto Quant Research

Research-first cryptocurrency trading project. The objective is to identify, reproduce where useful, and independently validate systematic trading strategies with **net economic profitability**, then decide whether a paper-trading and live-trading system is justified.

**Status (2026-11-12):** research and project specification only. No independent backtest, validated alpha, exchange selection, or live trading system exists yet.

## Agreed constraints
- Initial endowment: **0.5 ETH**, not EUR 500. No arbitrary limit on the number of positions or assets.
- Research/reporting numeraire: **USDC / USD equivalent**, with ETH buy-and-hold and cash benchmarks. Report ETH-equivalent results too.
- Long and short strategies may be researched, but **no leveraged portfolio exposure** is desired. Gross exposure <= 100% of equity is an initial constraint to validate; derivatives and borrowed shorts still introduce margin/liquidation risks.
- No commitment to any specific exchange or execution venue yet. **Bitvavo is the reference behind the initial cost estimate**, not a selected execution venue.
- Focus on returns **after** commissions, spread, slippage, and where applicable borrowing/funding/conversion costs.
- Baseline assumed **0.25% all-in per round trip**; stress test 0.15% and 0.50%. These are provisional Bitvavo-based estimates, **not measured execution costs or verified current exchange commissions**. See [cost provenance and verification](docs/METHODOLOGY.md#cost-provenance-and-exchange-selection). Do not double-count fees/spread.
- Prefer reproducible, interpretable signals over complex ML for its own sake.
- Academic papers are candidate specifications, **not proof** of profitability for our account.
- No real orders, API-key permissions, or autonomous trading until explicit authorization and a separate safety review.

## Workflow
1. Maintain a broad, evidence-graded literature catalogue; distinguish peer-reviewed research from working papers.
2. Build a reusable Python data and backtesting research platform, not an exchange-connected bot.
3. Implement standalone strategies, then test combinations and alternative portfolio construction.
4. Use chronological nested walk-forward validation; purging/embargo when labels overlap; an untouched final holdout. Track the number of hypotheses tested.
5. Evaluate net compounded return, ETH-relative return, Sharpe/Sortino, drawdown, turnover, capital utilization, and stability across regimes and cost assumptions.
6. Study exchange-specific historical data, spreads, volumes, order constraints, borrowability and API feasibility.
7. Only after a research go/no-go decision: prospective paper trading, then optionally a tightly controlled live experiment.

## Documentation
- [Agent working rules](AGENTS.md)
- [Project decisions](docs/DECISIONS.md)
- [Strategy universe](docs/STRATEGIES.md)
- [Research bibliography](docs/PAPERS.md)
- [Validation and costs](docs/METHODOLOGY.md)
- [Development roadmap](docs/ROADMAP.md)

## Research principle
The goal is not to find the best historical backtest. It is to find an economically meaningful, implementable edge that survives out-of-sample testing and realistic costs. A negative result is a valid outcome.

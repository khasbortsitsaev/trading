# Research methodology and economics

## Capital and benchmark
Start each simulation with a **0.5 ETH** endowment valued at the observed ETH/USDC price at the simulation start. USDC is a reporting numeraire, not a risk-free asset. Report final USDC P&L and total return, ETH-equivalent wealth and relative return against holding 0.5 ETH. Also compare with a no-trade USDC benchmark. Model conversion explicitly if a strategy requires it.

## Transaction costs
Temporary *round-trip all-in* assumptions:
- Low: 0.15%
- Baseline: 0.25%
- Stress: 0.50%

These include provisional commissions + spread + slippage, not measured execution costs. For asymmetric or partial trades allocate costs to the executed legs consistently. Never charge both an all-in assumption and its components. Shorts additionally require explicit borrow/funding and collateral modeling. Compare real exchange/pair-specific costs before go/no-go.

## Validation
- Use only information known at each decision timestamp.
- Preserve chronological ordering; expanding/rolling walk-forward train/validation.
- Use purging and embargo when label/event horizons overlap.
- Keep one untouched final holdout, preferably including periods after publication/selection.
- Treat paper results already examined as research-selection information; historical OOS in a paper is not automatically independent OOS for our project.
- Record number of trials, seeds and configuration searches; consider Deflated Sharpe / probability of backtest overfitting.
- Use historical point-in-time universes; avoid survivor-only asset selection.
- Include bull, bear, sideways and high-volatility market regimes.
- Compare against ETH hold, USDC hold and simple baseline strategies.
- Explicitly test sensitivity to transaction costs, delayed fills, missing data and reasonable parameter changes.

## Performance report
Net compounded return; terminal wealth; return relative to ETH; max drawdown; Sharpe/Sortino; turnover; trade expectancy and profit factor; exposure, utilization, long/short decomposition; fold-by-fold performance; confidence intervals where defensible. Distinguish gross and net results.

## Technical safeguards
No same-bar close execution unless the signal is known and executable at that price. Model order size, exchange precision, minimum notional, liquidity and market impact when data allow. A short position is not automatically safe because nominal gross exposure is <= equity. No real trades in research phase.

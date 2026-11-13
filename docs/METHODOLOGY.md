# Research methodology and economics

## Capital and benchmark
Start each simulation with a **0.5 ETH** endowment valued at the observed ETH/USDC price at the simulation start. USDC is a reporting numeraire, not a risk-free asset. Report final USDC P&L and total return, ETH-equivalent wealth and relative return against holding 0.5 ETH. Also compare with a no-trade USDC benchmark. Model conversion explicitly if a strategy requires it.

## Transaction costs
Legacy *round-trip all-in* assumptions, initially based on Bitvavo. Preserve these for comparison; they are not universal low/base/stress execution estimates:
- Original low scenario: 0.15%
- Original baseline scenario: 0.25%
- Original stress scenario: 0.50%

These include provisional commissions + spread + slippage, not measured execution costs. For asymmetric or partial trades allocate costs to the executed legs consistently. Never charge both an all-in assumption and its components. Shorts additionally require explicit borrow/funding and collateral modeling. Use the [market-specific cost analysis](COSTS.md) and [explicit model](cost-model.json) for current fee assumptions, distinguishing published commissions, sampled books and uncalibrated friction scenarios. Compare real exchange/pair-specific costs before go/no-go.

### Cost provenance and exchange selection
The user confirmed on 2026-11-12 that Bitvavo was the basis for the initial cost estimate. **Bitvavo has not been selected as the execution venue.** This records the estimate's origin, not an independent verification of a current fee schedule.

The 0.15%, 0.25% and 0.50% scenarios are all-in round-trip assumptions. They are not quoted Bitvavo commission rates, not per-side fees, and not measured fills. The exact original maker/taker mix, volume tier and spread/slippage breakdown have not yet been documented or independently verified.

Before interpreting a backtest as economically feasible:
- Verify each candidate venue's official fee schedule, applicable account/volume tier, maker/taker rates and actual pair availability. Record source URLs and verification dates.
- Calculate commissions for both entry and exit. Add pair- and order-size-specific spread/slippage estimates using consistent execution accounting; do not add a spread charge again if it is already represented in bid/ask fills.
- Include conversion and deposit/withdrawal or network charges only when the workflow incurs them. Centralized spot order-book trades do not each require an on-chain transaction.
- Model borrow/funding separately if shorting or derivatives are used. Do not charge those costs to ordinary fully funded spot purchases.
- Check whether USDC execution pairs exist and are sufficiently liquid; the USDC reporting numeraire does not require every trade to execute against USDC.
- Keep the original scenarios for sensitivity analysis, but revise or expand them if verified costs are outside their range. Another exchange's fees cannot establish Bitvavo's costs.
- Keep transaction costs, recurring infrastructure/data expenses and personal taxes separate. Net trading P&L is not automatically after-tax disposable income.

The earlier Kraken example in conversation illustrated venue differences only. It is not the basis for this project's cost model.

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

## Required pre-experiment feasibility record
For each shortlisted venue, record official source URL, retrieval date, applicable jurisdiction/product restrictions and whether access is generally documented or account-confirmed. Keep personal/account information out of git. Compare available spot pairs, minimum notional and quantity, precision, liquidity evidence, historical data endpoints, licensing, retention limits, delisted markets and missing periods. Public documentation alone does not establish account eligibility. Separate the signal data venue from the proposed execution venue.

For each candidate market, record maker/taker commissions per execution and volume tier; estimate spread and size-dependent slippage from dated observations, with uncertainty. Include realistic order sizes derived from the 0.5 ETH allocation and conversion path. Maker fees do not imply maker fills. The review's Bitvavo entry-tier fee figures were checked against primary sources in COSTS.md; paper interpretations remain unverified until separately audited. Keep the original cost scenarios as sensitivity cases, not calibrated facts.

Report break-even costs by rerunning frozen rules under increasing execution costs with an explicit unit (for example basis points per traded notional per side). State whether the threshold means zero absolute net P&L or zero excess return over a named benchmark; report both when useful. Handle no-trade and non-monotonic cases explicitly. Keep fixed infrastructure/data costs and EUR conversion assumptions separate from trading friction. Do not optimize strategy parameters against the preferred cost estimate.

## Frozen research protocol and stopping rules
Before the first real-data search, register:
1. Economic hypothesis, fully specified signal/allocation rules, benchmark objective and permitted parameter ranges.
2. A finite number of trials per family and total batch, including seeds, assets, timeframes and abandoned variants. Numerical budgets are pending, not implicitly unlimited.
3. Dataset hashes, point-in-time universe policy, chronological train/validation windows and sealed final holdout boundaries. Fit transformations only on past training data. Specify purging/embargo from label overlap rather than arbitrary defaults.
4. Selection procedure confined to training/validation; criteria for economic rejection, robustness and minimum usable evidence. Numeric thresholds must be fixed before searches, with consequential choices referred to the user.
5. Higher-cost, delayed-fill and nearby-parameter checks; profit concentration by coin, month and regime; dependence-aware uncertainty. Raw trade counts are not counts of independent observations.
6. A holdout access record identifying the frozen code/configuration and selection procedure before opening. If it fails, record the outcome; do not retune and reuse it as an untouched holdout. A fresh evaluation requires genuinely new data or an explicitly revised evidence label.
7. A batch-ending decision: proceed to prospective validation, reject, or inconclusive due to specified limitations. Additional searches or complexity require a new hypothesis, recorded rationale and budget, not silent continuation.

Numerical live loss tolerance is separate from research acceptance. Evaluate absolute capital growth and performance relative to ETH/cash, with drawdown and risk-adjusted metrics; lower drawdown does not automatically satisfy the capital-growth objective. Historical success never establishes certainty of live profits.

## Data and execution contract
- Preserve exchange event time, candle interval boundaries, timezone and actual feature availability time. On-chain features require publication delays and revision/version history.
- Reconstruct historical listings/delistings and universe eligibility using past information. If coverage cannot support that, narrow the universe claim and disclose survivor bias.
- Specify missing/duplicate/out-of-order data handling. Do not silently forward-fill tradable prices or manufacture executions; flag exclusions and evaluate sensitivity.
- Execute after information becomes available with declared latency and price assumptions. Candles cannot establish limit queue position, fills or intrabar stop/target order. Use conservative ambiguity rules, finer data where available, or reject unsupported execution claims.
- Document partial fills, unfilled orders, minimum sizes, residual cash, precision and data/venue mismatches. Use order-book/trade data when the strategy's execution claim requires it.
- Initial executable scope is fully funded spot. Any borrowed short requires independently documented availability, financing, collateral, recall and liquidation treatment plus a separate scope decision; a 1x gross exposure cap is insufficient.

## Concrete review specifications
The detailed operational specifications are now in [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) (points 3 and 5), [RISK_SCOPE.md](RISK_SCOPE.md) (point 4), and [DATA_EXECUTION.md](DATA_EXECUTION.md) (point 6). [research-policy.json](research-policy.json) mirrors proposed numerical defaults and explicitly records that they are not frozen. These documents specify controls; they do not claim their implementation or successful execution.

The proposed first-batch growth gate is positive net growth, at least 2 percentage points/year above ETH holding and no more than 30% historical drawdown, plus cost/consistency/robustness/evidence gates. Those numbers are agent proposals pending a user decision, not agreed investment requirements or live loss limits. Do not start a real-data search before the accepted version, exact variants, data and split manifests are committed. Independent synthetic accounting work can proceed with its preregistered fixtures.

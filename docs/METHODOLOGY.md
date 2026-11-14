# Research rules

Updated 13 November 2026. This is the single methodology for the six review items. The executable assumptions and exact first-batch variants are in [research-policy.json](../config/research-policy.json); evidence is under [research/reports](../research/reports). Positive historical returns have been observed; no repeatable trading edge is established.

## Objective and decision criteria

The user clarified that the objective is **repeatable positive expected trading returns after costs, with acceptable risk**. Existing ETH is available capital, not a preferred investment or a required growth benchmark. Starting inventory remains editable in config/runner.json. Use USD/USDC-source reporting; ETH/BTC/cash comparisons diagnose exposure and opportunity cost, not mandatory outperformance.

Current research evaluation:

- Positive net profitability across dates/regimes, reported together with losing periods and sensitivity, not inferred from one bull-market run. Execution/conversion costs included; business overhead must be separately included or explicitly excluded.
- Drawdown, loss from initial capital and exposure assessed alongside returns. The existing 30% drawdown and three-positive-fold screens remain provisional agent research heuristics, not user-approved live limits. No new threshold is fitted to observed results.
- Cost, delay and parameter robustness must support the mechanism; preserve failed tests and total trial counts. No ETH-relative wealth requirement for neighbors or stress cases.
- Attribute performance to decisions versus simply carrying crypto risk, using predeclared exposure/risk-matched passive controls. Underperforming full ETH in a rally is not failure by itself; outperforming ETH in a crash is not success by itself.
- Dependence-aware uncertainty and multiple-search accounting remain necessary. Overlapping rolling windows are descriptive, not independent evidence. A positive median return or a positive result in most windows does not establish positive expected profit.
- No candidate is promoted without sufficient controls/robustness and subsequent prospective paper validation. Before final holdout access, freeze one candidate and exact criteria. Never use the holdout to select the new objective or tune parameters.

The former >=2 percentage points/year above ETH rule is retired following the user's objective clarification, not because a backtest was made to pass. Original reports retain their original decision labels; their numerical results are unchanged. Reassessment means **edge unproven**, not retroactive success. No live risk limit is set.

CAGR uses elapsed seconds/365.25 days. Drawdown is loss from an equity high-water mark; loss from starting capital is reported separately. Net growth includes declared execution/conversion and recurring expenses, with costs separately attributed. Taxes are not invented; label results pre-tax unless a specific tax model has been reviewed. Sharpe, Sortino, turnover, utilization and time under water supplement wealth, rather than replacing it.

**No live risk limit is set.** The earlier broad drawdown discussion does not authorize losing 50%, and the 30% research screen is not a live stop or a bound on future loss.

## Data and market route

The user clarified that **EUR is not a trading constraint**. Do not select an expensive execution route merely because one exchange has longer EUR history.

- Research long historical series in USD or USDC from a suitable source independently of the eventual execution venue. Select source, coverage and supported access methods before interpreting strategy results. TradingView exports may be evaluated if suitable; their availability or completeness is not assumed.
- Prioritize low total-cost spot execution. Bitvavo crypto/USDC is the current fee-based candidate, not a final venue commitment. Compare commissions, spread/slippage and necessary conversions together, rather than insisting on one quote currency regardless of cost.
- No routine EUR conversion is required. Starting with owned ETH does not require EUR funding; cash/rotation legs can remain in USDC. Model EUR only if actual external funding or final cash-out uses it.
- The audited EUR data remain valid QA evidence or a cross-check, not a mandatory route. The shorter Bitvavo crypto/USDC history does not force all signal research onto EUR books or fees; another source can supply longer history.
- Distinguish signal data, execution assumptions and reporting units. Longer USD-source studies do not reproduce Bitvavo USDC fills. Record source-specific volume for volume/OBV signals, price-basis differences and USD/USDC deviations; never assert USD and USDC are identical prices. Use available venue overlap for execution-basis validation, with explicit limitations elsewhere.
- A fixed BTC/ETH study retains selection/survivorship limitations and is not a historical all-coin universe. Cross-sectional confirmation still needs past eligibility data.

Raw data stay outside git unless their redistribution is permitted. Record source IDs, timestamps, hashes, returned coverage, transformations and terms. Use official/supported access or exports, not invented access rights. Uncertainty about one provider does **not** require a Bitvavo permission request or block building the research system; choose another suitable source. No provider was contacted.

## Costs and portfolio scope

Start with owned ETH inventory. Sell it only if the strategy needs cash or another asset; do not impose a sell/rebuy on ETH holding. Rotation between assets consists of the actual sell and buy, not two additional abstract round trips. Physical EUR/USDC conversion is separate from reporting translation. Network fees apply only to actual external transfers, not every centralized fill.

Use actual public entry-tier taker schedules as conservative research scenarios, without unverified discounts: Bitvavo EUR 0.25% per execution, USDC crypto 0.05%, USDC/EUR conversion 0.10%; Kraken regular spot tier 1 is 0.80% per execution in the verified current schedule. Public fees are not authenticated account fees. Final account eligibility, fee asset/rounding and any negotiated rate require account evidence before funded use; they need not block a conservative simulated cost case.

Total noncommission friction scenarios are 15, 30 and 50 bps per round trip, allocated by executed notional. These are stress assumptions, not a calibrated slippage distribution. Do not add spread twice when reference prices already represent bid/ask or book depth. The original 0.15%/0.25%/0.50% all-in values remain historical comparison cases, not universal low/base/stress estimates. [COSTS evidence](../research/reports/costs.md) distinguishes sampled prices from actual fills.

Initial scope is **fully funded long/flat spot**: nonnegative cash/inventory and target weights, sum of risky weights no greater than one with fees reserved. Support multiple simultaneous positions without a fixed count cap. Sell only owned inventory; sell reductions before buys and do not spend unavailable settlement proceeds. Negative signals leave cash. No margin, borrowed shorts, derivatives, leveraged/inverse products, staking or collateral reuse.

Borrowed shorts remain possible future research, not initial scope. A 1x gross portfolio can still have borrowing, recall, collateral and liquidation risk. A later short-product decision requires actual jurisdiction/product access, historical financing or stressed rates, collateral/haircuts, forced-cover and liquidation rules, loss scenarios and explicit user acceptance of the residual risk. Do not substitute derivatives to bypass the no-leverage preference.

## Finite first batch and protocol

**POC update:** S1 first, then S2 and S3. The multi-variant batch below is retained as a paused preregistration, not the next task. Preserve the one completed trial and all prior settings/results. No generic batch orchestrator is required for S1 close-out. S2 specification is now frozen in policy; one reserved S2 slot replaces unexecuted TREND-365 within the unchanged 18-slot ceiling. The old family counts below describe the original paused batch.

The first batch has a cap of 18 selection variants. Twelve are now specified in the policy: six simple positive-return trend lookbacks and six long/flat reversal configurations on the fixed BTC/ETH universe. Six cross-sectional slots remain disabled until feasible. Exact signal definitions, four nearest preregistered neighbors and equal-universe-weight allocation are recorded before evaluating returns. An inactive asset's weight stays in cash; do not renormalize into an always-invested portfolio. No ML, RL or allocation-model search in this batch.

A changed universe, venue, timeframe, seed, allocation, cost choice or signal parameter after inspecting performance is a new variant. Failed and abandoned variants count. Passive controls are not search variants; tradable baselines are. Retain negative results and defect-driven reruns in [experiments.md](experiments.md).

Exact UTC splits are frozen in the policy: accounting starts 2021-01-01 after 2020 warmup; four contiguous 180-day development test windows run from 2023-11-24 through 2025-11-12. Each fold fits only on prior history; the last 180 training observations are inner validation when fitting is necessary. Purge overlapping information/label intervals and derive a boundary gap from relevant horizons, at least one decision bar. No shuffled temporal cross-validation. An algorithm must not pretend fixed rules need fitting.

Score a continuously funded stitched development portfolio, with actual rebalance costs across folds. Rank qualifying candidates by net CAGR, then lower turnover, fewer fitted parameters and preregistered ID. Choose one champion. Four neighbor checks reuse existing variants; five additional champion sensitivity scenarios produce a ceiling of 92 outer fold/scenario evaluations, not 92 independent tests. The first batch stops if its champion fails mandatory robustness; do not silently promote a runner-up.

The configured uncertainty sensitivity uses paired circular moving blocks of 7, 30 and 90 days, seed 20261113, an 18-variant multiplicity allowance, and 2,000 initial/20,000 champion replicates. These are conservative working heuristics, not exact guarantees in a changing market. Preserve paired strategy/ETH returns and report adequacy limits. Large correlated samples do not become independent evidence through resampling.

## Holdout and stopping rules

The sealed assessment window is **2025-11-13 inclusive through 2026-11-13 exclusive**. This development audit did not retrieve it. Earlier public price snapshots exist; disclose that prior price awareness and published-paper contamination rather than claiming the period was unknown to the world.

Before access, commit the selected algorithm/update rules, code, dataset hashes, costs, exact acceptance criteria and champion identity. Optimization must not read the final partition. One access bundle may produce the champion's predeclared baseline, cost stress and extra-delay outputs, not select among candidates. A historical holdout is followed by prospective paper validation, never directly by presumed profitable live use.

Reject when reliable evidence fails the frozen criteria; invalidate a run with accounting/leakage defects; label insufficient data or unsupported uncertainty inconclusive. Preserve all outcomes. A failed holdout cannot be retuned against and called untouched again. A new research batch needs a recorded rationale, retained trial history and valid new evaluation, not merely added complexity.

## Causal data and execution contract

Canonical records preserve venue/instrument, event time, information availability (observed versus assumed), receipt time, source IDs and dataset version. Prices/cash/fees use decimal arithmetic. Candle intervals are UTC half-open ranges with positive OHLC, `low <= open/close <= high`, nonnegative volume and a completion flag. Feature publications/revisions need vintage timestamps; today's revised values cannot masquerade as historical information.

Normalize order explicitly. Identical page overlaps are deduplicated with provenance; conflicts fail. Trade IDs, not timestamps, identify repeated trades. Missing bars are diagnosed and reported, never filled into fabricated executions. A carried valuation is explicitly stale, not a fresh quote; unresolved stale scored holdings prevent a pass. Check page boundaries and effective limits rather than trusting HTTP 200, requested dates or a documented row cap.

Every action requires `input_available <= decision < order_ready <= fill_event`. For the daily candle proxy, assume five-minute publication and processing lags separately, explicitly tagged assumptions. Choose the designated daily bar whose start is strictly after order readiness; a missing/suspended designated interval means no fill, not a favorable later replacement. One extra-bar delay is a required sensitivity. Candle open references remain modeled proxies, not guaranteed execution at the interval boundary.

Validate fees, tick/quantity precision, both base and quote minimums, inventory and fee-inclusive cash before a fill; reject atomically if infeasible. Reserve cash/inventory for pending orders; cancel prior targets before reusing reserves. Reference-price slippage is applied adversely, without double-counting observed spread. Model actual fee assets before claiming venue-specific reconciliation.

Do not infer maker queue fills, stop/target order or executable last-price exits from candles. Suspensions/delistings prohibit new fills; unavailable exits require impairment bounds or an inconclusive result, not removal of the loss. Initial limited-universe data cannot support broad cross-sectional or short-feasibility claims.

The offline primitives and daily runner now have 40 passing acceptance tests, including multi-asset rotation, quote/base fees, negative-balance rejection, precision/minimums, timing, gaps, stale marks, suspensions, collector boundaries and holdout rejection. A bounded USD collector, delayed-proxy backtester and ledger/benchmark reports are implemented. They are **not actual exchange integration or a complete selection/robustness/uncertainty system**. Cost-ledger fixtures and data audits are software evidence only. Commit code/config before runs and result artifacts separately, with actual commands/counts and limitations in the experiment registry.

## Implemented runner and admitted development data

The admitted USD source is the official Bitstamp daily OHLC API. The collector uses the documented 1,000-row maximum and end-parameter precedence, verifies source pair identity/response hashes and rejects requested or returned holdout overlap. Both BTC/USD and ETH/USD contain all 2,143 expected development days from 2020-01-01 through 2025-11-12, with valid OHLC and nonnegative volume. Raw bodies and normalized data remain outside Git; public metadata and the admission hash are in config/research-policy.json and research/artifacts/usd-source-audit.json. This is private research through supported access; no unrestricted commercial-data license or raw redistribution is claimed. The API documentation has a separate commercial-company licensing notice; the terms-page interstitial was not bypassed or represented as verified content.

The runner consumes only previously completed/available closes, fixes target quantities at the decision, then queues them for the designated future daily-open proxy. At modeled execution it sells reductions before buys, uses adverse prices/tick rounding, enforces fees/minimums and resizes unaffordable buys down. Delayed targets are queued instructions, not resting venue orders; actual cash is never borrowed. Initial strategy capital stays in owned ETH until the rule requires a trade. Cash benchmark's initial conversion is charged once; ETH holding has no invented conversion.

A run on external USD prices reports a USD ledger and explicitly does not claim actual USDC wealth. Static current Bitvavo USDC-like fee/minimum assumptions are only a prospective-cost proxy, not source-venue history or a USD/USDC parity finding. Full ledgers remain private; aggregate summaries identify code/config/data hashes and evidence type. Future-price perturbation, extra delay, cash resizing, source hash/gap failure and no-network holdout rejection all have executed tests.

S1-001 is the first registered historical development pilot, not a champion or final holdout result. It failed the historical ETH-growth/drawdown screens; ETH outperformance is no longer a current gate. No parameter/window/fee change or holdout access followed that result. The remaining predeclared variants are still untested; one negative baseline neither proves nor disproves the broader project.

## Start-date robustness

Use paired, fixed-horizon fresh portfolios across every eligible monthly start, not selected endpoints. Current registered analysis: 12 calendar months, 2021-01 through 2024-11, same USD 1000 initial-equity ETH endowment, state reset, costs and baseline signals. Compare each strategy against ETH on identical dates and record all windows, losses, paired excess returns and drawdowns. Overlap and post-hoc development design prevent independent-trial significance claims. Preserve the first single-start experiments as period-specific evidence; do not choose the best starting date or tune to these results. Details/assumptions in policy rolling_start_analysis.

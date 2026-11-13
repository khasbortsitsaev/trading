# Research rules

Updated 13 November 2026. This is the single methodology for the six review items. The executable assumptions and exact first-batch variants are in [research-policy.json](../config/research-policy.json); evidence is under [research/reports](../research/reports). No strategy has been shown profitable.

## Objective and decision criteria

The agreed objective is capital growth from **0.5 ETH**, with no planned withdrawals. Report portfolio wealth in USDC, EUR and ETH-equivalent units. Compare identical dates against holding the original ETH and a no-trade cash benchmark, charging each only its actual necessary conversions. Stablecoins and cash are not assumed risk-free or interest-bearing.

To resolve the previously open research settings, the agent has frozen the following **research-only working defaults** under the user's instruction to resolve the review. These are not a statement that the user chose these as personal/live investment preferences:

- Growth candidate: positive net CAGR, at least 2 percentage points/year above ETH, and maximum historical drawdown no greater than 30%, separately on stitched development OOS and the final holdout.
- At least three of four development folds profitable; no dependence on the single best month; at least three of four preregistered neighboring variants retain positive growth and ETH-relative wealth.
- Positive growth and ETH-relative wealth under current commissions plus 30 bps total round-trip noncommission friction, and with one extra daily execution delay. Report the 50-bps friction case even if it fails.
- A paired, dependence-aware uncertainty check must support excess daily log growth after accounting for the full selection budget. If evidence is weak or the method is not valid for the sample, report inconclusive.
- A positive-growth/lower-drawdown strategy that does not beat ETH is reported as a **defensive result**, not silently accepted under a changed objective. The user can decide its value later; research need not wait to measure both outcomes.

CAGR uses elapsed seconds/365.25 days. Drawdown is loss from an equity high-water mark; loss from starting capital is reported separately. Net growth includes declared execution/conversion and recurring expenses, with costs separately attributed. Taxes are not invented; label results pre-tax unless a specific tax model has been reviewed. Sharpe, Sortino, turnover, utilization and time under water supplement wealth, rather than replacing it.

**No live risk limit is set.** The earlier broad drawdown discussion does not authorize losing 50%, and the 30% research screen is not a live stop or a bound on future loss.

## Data and market route

Actual development-data auditing changes the first research route:

- Use **Bitvavo BTC/EUR and ETH/EUR** as a fixed limited-universe research candidate. The fetched 2020-01-01 through 2025-11-12 development samples each have 2,143 daily candles with no missing days after pagination repairs.
- Use actual USDC/EUR marks for USDC reporting, not an assumed USD peg. Its daily series is complete during the accounting period beginning 2021-01-01. The earlier EUR-only data is indicator warmup, not a period with invented FX marks.
- BTC/USDC and ETH/USDC only returned history from July 2024 in the audited windows, with two early missing days. Their cheaper fees do not justify shortening evaluation or applying USDC execution fees to EUR prices. Retain them for later appropriately scoped/prospective evaluation.
- The fixed BTC/ETH selection has survivor/selection limitations. It is not a historical all-coin universe. Cross-sectional confirmation is deferred until dated listing/delisting/jurisdiction events support it; unused variant slots are not reassigned.

The raw price data remain outside git. Provenance includes URLs/parameters without secrets, retrieval timestamps, SHA-256 hashes, returned coverage, transformations, conflicts, gaps, venue/pair and terms versions. Preserve archive checksums and TLS verification. The [history audit](../research/artifacts/readiness-history.json) contains counts and diagnostic metadata, not a redistributable dataset.

The chosen operational purpose is own-account research, not a data redistribution/customer product. Official Bitvavo API terms tie data retention/use to authorized use of its services. **Standalone historical/AI-assisted research permission was not explicitly confirmed by the vendor.** This cannot be represented as a granted license; the exact remaining clarification is recorded in the feasibility report. A noncommercial third-party license is not silently treated as permission for this capital-growth project. Synthetic development and bounded quality checks are independent of this unresolved strategy-data permission.

## Costs and portfolio scope

Start with owned ETH inventory. Sell it only if the strategy needs cash or another asset; do not impose a sell/rebuy on ETH holding. Rotation between assets consists of the actual sell and buy, not two additional abstract round trips. Physical EUR/USDC conversion is separate from reporting translation. Network fees apply only to actual external transfers, not every centralized fill.

Use actual public entry-tier taker schedules as conservative research scenarios, without unverified discounts: Bitvavo EUR 0.25% per execution, USDC crypto 0.05%, USDC/EUR conversion 0.10%; Kraken regular spot tier 1 is 0.80% per execution in the verified current schedule. Public fees are not authenticated account fees. Final account eligibility, fee asset/rounding and any negotiated rate require account evidence before funded use; they need not block a conservative simulated cost case.

Total noncommission friction scenarios are 15, 30 and 50 bps per round trip, allocated by executed notional. These are stress assumptions, not a calibrated slippage distribution. Do not add spread twice when reference prices already represent bid/ask or book depth. The original 0.15%/0.25%/0.50% all-in values remain historical comparison cases, not universal low/base/stress estimates. [COSTS evidence](../research/reports/costs.md) distinguishes sampled prices from actual fills.

Initial scope is **fully funded long/flat spot**: nonnegative cash/inventory and target weights, sum of risky weights no greater than one with fees reserved. Support multiple simultaneous positions without a fixed count cap. Sell only owned inventory; sell reductions before buys and do not spend unavailable settlement proceeds. Negative signals leave cash. No margin, borrowed shorts, derivatives, leveraged/inverse products, staking or collateral reuse.

Borrowed shorts remain possible future research, not initial scope. A 1x gross portfolio can still have borrowing, recall, collateral and liquidation risk. A later short-product decision requires actual jurisdiction/product access, historical financing or stressed rates, collateral/haircuts, forced-cover and liquidation rules, loss scenarios and explicit user acceptance of the residual risk. Do not substitute derivatives to bypass the no-leverage preference.

## Finite first batch and protocol

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

The offline primitives now have executed synthetic acceptance tests, including multi-asset rotation, quote/base fees, negative-balance rejection, precision/minimums, timing, gaps, stale marks, suspensions and holdout rejection. They are **not a complete backtester, ingestion service or exchange integration**. Cost-ledger fixtures and data audits are software evidence only. Commit code/config before runs and result artifacts separately, with actual commands/counts and limitations in the experiment registry.

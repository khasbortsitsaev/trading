# POC strategies

| Strategy | Buy / hold | Sell | Status |
|---|---|---|---|
| **S1 trend** | Completed close above the close L days earlier; current pilot L=20 | Target zero when return over L days is zero or negative | Offline pipeline and DEV-001 complete; research close-out next |
| **S2 volume/technical** | Price/volume confirmation, exact rule to specify | Must be specified with entry, before testing | Deferred until S1 close-out; no implemented S2 rule |
| **S3 mean reversion** | Implemented candidate buys when trailing log-price z-score <= negative entry threshold | Exit when z >= 0; zero variance means flat; otherwise retain state | Code exists, historical evaluation paused |

## S1 mechanics and exits

For each asset, calculate `close[t] / close[t-L] - 1` from completed, available daily bars. A positive value activates its allocation; zero or negative leaves its allocation in cash. The current two-asset pilot assigns each active asset half the fee-reserved portfolio; an inactive allocation stays cash.

The runner recomputes target quantities daily. It may sell part of a holding to restore its target weight even while the trend stays positive. A signal exit targets zero, but minimum order sizes can leave dust. Execution uses a delayed future daily-open proxy, fees and adverse price rounding, not an immediate fill at the signal close.

There is **no fixed profit target, stop-loss or maximum holding period** in this baseline. A position can stay open while the trend remains positive, and can exit at a loss. Profit targets, stops, less frequent rebalancing or signal-change-only trading are separate testable hypotheses, not silent tweaks to the existing result. Candle data cannot establish the order of intrabar stop/target hits.

The algorithm, allocation, costs and timing are separate components. Edit lookbacks in [research-policy.json](../config/research-policy.json); baseline funding/cost/timing assumptions in [runner.json](../config/runner.json). Register changes before new historical evaluation. Keep S1, S2 and S3 experiment entries and artifacts separate; reuse the common engine.

## Later ideas

Pairs/cointegration, copulas, event-driven or cost-aware ML, on-chain/cross-sectional factors, regime models and advanced allocation are outside this POC. Candidate sources remain in [PAPERS.md](PAPERS.md). Existing repositories may provide reusable components after license and suitability checks; no new external-code audit was performed for this feedback update. Lower-frequency equity investing is a possible future direction, not current implementation scope.

# POC strategies

| Strategy | Buy / hold | Sell | Status |
|---|---|---|---|
| **S1 trend** | Completed close above the close L days earlier; current pilot L=20 | Target zero when return over L days is zero or negative | Baseline closed: failed promotion; see below |
| **S2 volume/technical** | Price/volume confirmation, exact rule to specify | Must be specified with entry, before testing | Deferred until S1 close-out; no implemented S2 rule |
| **S3 mean reversion** | Implemented candidate buys when trailing log-price z-score <= negative entry threshold | Exit when z >= 0; zero variance means flat; otherwise retain state | Code exists, historical evaluation paused |

## S1 mechanics and exits

For each asset, calculate `close[t] / close[t-L] - 1` from completed, available daily bars. A positive value activates its allocation; zero or negative leaves its allocation in cash. The current two-asset pilot assigns each active asset half the fee-reserved portfolio; an inactive allocation stays cash.

The runner recomputes target quantities daily. It may sell part of a holding to restore its target weight even while the trend stays positive. A signal exit targets zero, but minimum order sizes can leave dust. Execution uses a delayed future daily-open proxy, fees and adverse price rounding, not an immediate fill at the signal close.

There is **no fixed profit target, stop-loss or maximum holding period** in this baseline. A position can stay open while the trend remains positive, and can exit at a loss. Profit targets, stops, less frequent rebalancing or signal-change-only trading are separate testable hypotheses, not silent tweaks to the existing result. Candle data cannot establish the order of intrabar stop/target hits.

The algorithm, allocation, costs and timing are separate components. Edit lookbacks in [research-policy.json](../config/research-policy.json); baseline funding/cost/timing assumptions in [runner.json](../config/runner.json). Register changes before new historical evaluation. Keep S1, S2 and S3 experiment entries and artifacts separate; reuse the common engine.

## S1 baseline conclusion: do not promote

DEV-001, historical development proxy, 2023-11-24 through 2025-11-12: **+62.32% net growth versus ETH +65.52%; drawdown 44.89%**. Annual growth lagged ETH by 1.27 percentage points, against a required +2-point margin; drawdown exceeded the 30% research screen. Lower drawdown than ETH is useful context, not a passing growth result. This rejects TREND-20 under these settings, not all trend following.

Concrete examples from the exactly reconstructed ledger (UTC; modeled fills, not real orders):

| Action | Available signal | Modeled fill | Meaning |
|---|---|---|---|
| ETH sell | 30 Nov 2023: 20-day return -4.33% | 1 Dec: sell the remaining ETH position | Signal turned nonpositive; -4.33% is the signal return, not the position's realized loss |
| ETH buy | 2 Dec 2023: 20-day return +1.69% | 3 Dec: buy ETH again | Trend turned positive; illustrates rapid exit/re-entry |
| BTC partial sell | 29 Nov 2023: trend still +6.17% | 30 Nov: sell about $5.43 | Daily target adjustment while the trend remains active |

425 fills over 720 days comprised 2 initial-allocation fills, 87 signal-entry fills, 89 signal-exit fills and 247 active-state resizing fills. Counts are classified by their generating decision, not by the later fill-day signal, and are not completed round trips. Another 410 targets were skipped for cash/rounding/minimums.

Total traded notional was $124,300; commissions $62.15 and modeled adverse price/tick costs $93.77. The $155.92 cost sum equals 15.12% of initial equity, **not** a measured reduction in terminal return; no zero-cost counterfactual was run. Active-state resizing produced 58.1% of fills but only $4.16 (2.7%) of direct costs. Entry/exit signal flips dominated costs. Reducing daily resizing alone is therefore a limited cost-saving hypothesis, not a demonstrated solution.

**Evidence gaps:** unmeasured USD/USDC and source/execution differences, fixed BTC/ETH selection, candle-based rather than actual fills, and no completed parameter/cost/delay robustness, uncertainty analysis or prospective paper test. These prevent a positive edge claim. The failed baseline needs no champion/holdout evaluation. Holdout stays sealed; one variant remains evaluated. [Aggregate checks](../research/artifacts/S1/dev-001-closeout.json).

**Next:** define one S2 rule, including entry, exit and sizing, using the existing reuse review. Keep its evidence separate. A slower S1 signal/exit experiment remains an alternative future hypothesis, not a change to this result.

## Later ideas

Pairs/cointegration, copulas, event-driven or cost-aware ML, on-chain/cross-sectional factors, regime models and advanced allocation are outside this POC. Candidate sources remain in [PAPERS.md](PAPERS.md). Existing repositories may provide reusable components after license and suitability checks; no new external-code audit was performed for this feedback update. Lower-frequency equity investing is a possible future direction, not current implementation scope.

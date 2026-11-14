# POC strategies

| Strategy | Buy / hold | Sell | Status |
|---|---|---|---|
| **S1 trend** | Completed close above the close L days earlier; current pilot L=20 | Target zero when return over L days is zero or negative | Pilot complete; edge unproven |
| **S2 volume/technical** | Positive 20-day trend plus unusually high volume | Nonpositive 20-day trend; volume alone does not exit | Pilot complete; lower drawdown, edge unproven |
| **S3 mean reversion** | Implemented candidate buys when trailing log-price z-score <= negative entry threshold | Exit when z >= 0; zero variance means flat; otherwise retain state | Pilot complete; edge unproven |

## Current objective reassessment

The user clarified that ETH is available capital, not the required investment benchmark. The mandatory ETH-outperformance criterion is removed. Historical verdicts below describe the old screens; they are not current family-wide rejection decisions. Old results/parameters are unchanged; no strategy is automatically promoted.

| Existing 47 overlapping 12-month windows | S1 | S2 | S3 |
|---|---:|---:|---:|
| Profitable windows | 26/47 (55%) | 30/47 (64%) | 33/47 (70%) |
| Median net return | +6.66% | +14.22% | +21.86% |
| Worst return | -50.92% | -37.19% | -46.27% |
| Median drawdown | 38.38% | 25.44% | 30.60% |
| Worst drawdown | 55.03% | 42.45% | 58.27% |

**Interpretation:** S1 has substantial risk and inconsistent profitability; S2 has the most favorable observed drawdown profile; S3 has more profitable windows but substantial downside. None is disqualified just for trailing ETH. None demonstrates a reliable edge: market exposure may explain profits, overlapping windows are dependent, and robustness/uncertainty/prospective evidence is missing. These descriptive figures do not imply a future probability of profit.

Returns are pre-tax and include modeled commissions/friction, not fixed hosting/data costs or withdrawals. The 30% drawdown screen remains provisional; it is not a live loss limit. No monthly revenue forecast is supported. Next: predeclare exposure/risk-matched passive controls and a bounded cost/delay check before evaluating more. Do not fit parameters or pick an objective to make a candidate pass.

## S1 mechanics and exits

For each asset, calculate `close[t] / close[t-L] - 1` from completed, available daily bars. A positive value activates its allocation; zero or negative leaves its allocation in cash. The current two-asset pilot assigns each active asset half the fee-reserved portfolio; an inactive allocation stays cash.

The runner recomputes target quantities daily. It may sell part of a holding to restore its target weight even while the trend stays positive. A signal exit targets zero, but minimum order sizes can leave dust. Execution uses a delayed future daily-open proxy, fees and adverse price rounding, not an immediate fill at the signal close.

There is **no fixed profit target, stop-loss or maximum holding period** in this baseline. A position can stay open while the trend remains positive, and can exit at a loss. Profit targets, stops, less frequent rebalancing or signal-change-only trading are separate testable hypotheses, not silent tweaks to the existing result. Candle data cannot establish the order of intrabar stop/target hits.

The algorithm, allocation, costs and timing are separate components. Edit lookbacks in [research-policy.json](../config/research-policy.json); baseline funding/cost/timing assumptions in [runner.json](../config/runner.json). Register changes before new historical evaluation. Keep S1, S2 and S3 experiment entries and artifacts separate; reuse the common engine.

## S1 historical pilot under the original screens

S1-001, historical development proxy, 2023-11-24 through 2025-11-12: **+62.32% net growth versus ETH +65.52%; drawdown 44.89%**. Annual growth lagged ETH by 1.27 percentage points, against a required +2-point margin; drawdown exceeded the 30% research screen. Lower drawdown than ETH is useful context, not a passing growth result. This rejects TREND-20 under these settings, not all trend following.

Concrete examples from the exactly reconstructed ledger (UTC; modeled fills, not real orders):

| Action | Available signal | Modeled fill | Meaning |
|---|---|---|---|
| ETH sell | 30 Nov 2023: 20-day return -4.33% | 1 Dec: sell the remaining ETH position | Signal turned nonpositive; -4.33% is the signal return, not the position's realized loss |
| ETH buy | 2 Dec 2023: 20-day return +1.69% | 3 Dec: buy ETH again | Trend turned positive; illustrates rapid exit/re-entry |
| BTC partial sell | 29 Nov 2023: trend still +6.17% | 30 Nov: sell about $5.43 | Daily target adjustment while the trend remains active |

425 fills over 720 days comprised 2 initial-allocation fills, 87 signal-entry fills, 89 signal-exit fills and 247 active-state resizing fills. Counts are classified by their generating decision, not by the later fill-day signal, and are not completed round trips. Another 410 targets were skipped for cash/rounding/minimums.

Total traded notional was $124,300; commissions $62.15 and modeled adverse price/tick costs $93.77. The $155.92 cost sum equals 15.12% of initial equity, **not** a measured reduction in terminal return; no zero-cost counterfactual was run. Active-state resizing produced 58.1% of fills but only $4.16 (2.7%) of direct costs. Entry/exit signal flips dominated costs. Reducing daily resizing alone is therefore a limited cost-saving hypothesis, not a demonstrated solution.

**Evidence gaps:** unmeasured USD/USDC and source/execution differences, fixed BTC/ETH selection, candle-based rather than actual fills, and no completed parameter/cost/delay robustness, uncertainty analysis or prospective paper test. These prevent a positive edge claim. The failed baseline needs no champion/holdout evaluation. Holdout stays sealed; this S1 evaluation counts as one of the two historical variants used. [Aggregate checks](../research/artifacts/S1/s1-001-diagnostics.json).

S2 implementation and development test are now complete. A slower S1 experiment remains a separate future hypothesis.

## S2: volume-confirmed trend

**Hypothesis:** requiring strong participation before entry may improve after-cost trend results. This is an agent-selected hypothesis after reviewing S1, not a reproduced paper or proven improvement.

- **Buy:** while inactive, latest completed close exceeds the close 20 days earlier **and** latest completed daily volume exceeds 1.5 times the mean of the preceding 20 days, excluding the latest day. Exact equality does not enter.
- **Hold / sell:** while active, hold while the 20-day price return stays positive; target zero at zero or negative return. Low volume alone does not sell. No fixed profit target, stop-loss or time limit.
- **Size / execute:** reuse S1 daily fee-reserved equal-universe allocation and delayed execution. This can still resize a holding daily; the volume condition gates entry, not every partial buy/resize. Inactive allocations stay cash.
- **Initialize:** inactive signals at the first scored decision, even though starting inventory may contain ETH. Need 21 completed warmup bars; no trades before scoring. A zero prior-volume mean blocks entry; missing/invalid volume fails validation.

Example: preceding average volume 100 units means entry requires strictly more than 150 units alongside a positive trend. A held position can remain active at volume 80 if its price trend stays positive.

Parameters and exact conventions live in `poc.s2_spec` in [research-policy.json](../config/research-policy.json). The 20-day window reuses S1 and 1.5 is a simple untested assumption; no threshold search. Source volume is Bitstamp-specific, not total crypto-market or eventual execution-venue volume.

Reuse review: the existing short trend formula, portfolio and accounting code are sufficient. Copying a community strategy with different indicators/ROI/stops or migrating frameworks would add unrelated changes. No third-party source is copied. This test evaluates the combined entry gate and stateful holding rule; it cannot isolate volume's incremental contribution from entry timing without a separately registered control.

One S2 pilot will use the same admitted development dates, costs and ETH/cash controls as S1. It reserves the untested TREND-365 budget slot; the total cap stays 18 and one historical variant remains used. S1's result has influenced this hypothesis, so S2 is adaptive development research, not independent validation. Holdout remains sealed. [Validation plan](experiments.md#s2-001-volume-confirmed-trend-plan).

### S2 historical pilot under the original screens

Historical development proxy, same 720-day window as S1; not prospective or independent final validation:

| Metric | S1 | S2 | ETH holding |
|---|---:|---:|---:|
| Net growth | +62.32% | +46.99% | +65.52% |
| Annual growth | 27.85% | 21.58% | 29.13% |
| Maximum drawdown | 44.89% | 27.02% | 63.80% |
| Modeled commissions + adverse costs | $155.92 | $60.62 | No trading costs |

S2 had 270 fills and 306 skipped targets; three of four continuous development folds were profitable. It meets the positive-growth/drawdown screens but misses the required ETH-relative growth margin. Costs and drawdown improved descriptively; this does not isolate volume's contribution or prove the change caused an improvement. No promotion, retuning or holdout access. Missing robustness/uncertainty and execution-basis calibration remain limitations.

49 software checks pass; this is not an investment-performance conclusion. Synthetic fixtures exercise actual buys, holds and exits; the default random-volume CLI smoke only sold initial inventory, so its completion alone is not signal coverage. All 720 historical decisions/equity points and 270 fills' timing were audited. [Result](../research/artifacts/S2/s2-001-summary.json), [checks and fold results](../research/artifacts/S2/s2-001-validation.json). S3 is now completed below.

## S3 historical pilot under the original screens

REVERSAL-20-1 buys when the latest completed log price is at least one sample standard deviation below the latest 20-day log-price average (including that close). Sell when it reaches/exceeds the moving average; retain signal state between thresholds. Zero variance means flat. Start inactive, with at least 20 warmup closes. No fixed profit target, stop-loss or time exit. Parameters remain in the policy's existing variant definition; sizing/timing/costs reuse S1/S2.

S3-001 historical development proxy: **+58.39% net growth, 26.27% CAGR, 30.64% maximum drawdown**; ETH +65.52%, 29.13% CAGR. Three of four continuous folds profitable. 250 fills, 329 skipped targets; $34.75 commissions and $52.42 adverse modeled costs. Fails the ETH growth margin and 30% drawdown screens; no promotion or retuning. A dip can keep falling, and the moving average can fall toward price; a mean-crossing exit need not realize a profit.

55 software checks pass, including S3 state/warmup/startup/future-price and full synthetic ledger checks. Historical decisions were independently recomputed with Decimal logs/sample variance, daily equity/costs reconciled and fill timing checked. [S3-001 result](../research/artifacts/S3/s3-001-summary.json), [validation/folds](../research/artifacts/S3/s3-001-validation.json). Adaptive development after S1/S2, fixed assets and execution proxies prevent independent or live edge claims; robustness/uncertainty/paper evidence is absent.

**POC conclusion:** all three baseline pipelines run end to end, but none meets the current growth/risk criteria. S2 has the lowest drawdown, with lower growth. Review that tradeoff before defining a new bounded experiment; no automatic expansion or holdout access.

## Monthly-start sensitivity: fixed 12-month horizon

The single-start results above are not general verdicts on a strategy family. At the user's request, S1-002/S2-002/S3-002 restart each unchanged strategy on **every month-start January 2021 through November 2024**, holding for 12 calendar months. All 47 eligible windows used; 2020 supplies warmup. This spans more development regimes than the original pilots. Holdout unchanged and untouched.

Each fresh portfolio starts with owned ETH worth **$1,000** at that date's open, shared by strategy/benchmark; constant dollars reduce minimum-order/size confounding. Inactive initial signal state, no artificial initial purchase fee, no final liquidation. Same baseline costs/price source, no retuning.

| Across 47 overlapping windows | S1 | S2 | S3 | ETH hold |
|---|---:|---:|---:|---:|
| Beats ETH | 21/47 | 20/47 | 24/47 | Reference |
| Median 12-month return | +6.66% | +14.22% | +21.86% | +25.80% |
| Worst 12-month return | -50.92% | -37.19% | -46.27% | -72.00% |
| Losing windows | 21/47 | 17/47 | 14/47 | 19/47 |
| Median within-window drawdown | 38.38% | 25.44% | 30.60% | 57.25% |
| Worst within-window drawdown | 55.03% | 42.45% | 58.27% | 79.29% |

S3's **median paired excess return is +0.50 percentage points**: compare each strategy/ETH pair first, then take the median. That differs from subtracting the separate return medians. S1/S2 paired excess medians are -15.67/-14.45 points.

**Conclusion:** date choice matters. S3 is mixed, not consistently inferior; none has demonstrated a robust growth edge. S2 looks more defensive. Large drawdowns remain, and overlapping windows are dependent, so 47 observations do not provide 47 independent trials. This is post-hoc development sensitivity, not unseen final validation or confidence of beating ETH in future.

Per-window evidence: [S1-002](../research/artifacts/S1/s1-002-rolling.json), [S2-002](../research/artifacts/S2/s2-002-rolling.json), [S3-002](../research/artifacts/S3/s3-002-rolling.json). All 141 ledgers audited; 57 software checks passed. No promotion or parameter change follows automatically.

## Composition diagnostic and execution stress

S1-003/S2-003/S3-003 reuse all 47 windows and unchanged signals. Control is a once-traded BTC/ETH/cash portfolio whose starting weights equal the strategy's realized mean weights over that window. **Those weights require hindsight** and subsequently drift: this is an approximate composition diagnostic, not a tradable or risk-matched alternative and not a causal alpha test. Initial rebalance has the same delay/fees/minimums; no further trades or forced liquidation.

| Across 47 windows | S1 | S2 | S3 |
|---|---:|---:|---:|
| Baseline median net return (15bps friction) | +6.66% | +14.22% | +21.86% |
| Median at 30bps friction | +3.20% | +12.05% | +19.90% |
| Median at 50bps friction | -1.21% | +10.15% | +17.33% |
| Median with one extra daily delay, baseline friction | +8.35% | +13.12% | +12.32% |
| Beats hindsight composition control | 16/47 | 18/47 | 25/47 |
| Median paired excess over that control | -14.22 points | -4.03 points | +0.57 points |

Friction is total round-trip noncommission cost; 0.05% commission per execution stays unchanged. Stress assumptions are not calibrated actual costs. Medians across overlapping 12-month windows are not expected annual returns, and separate stress cases are not combined. All methods retain substantial downside; S3's worst stress-case drawdown reaches about 59%.

**Conclusion:** S1 is cost-fragile; S2/S3 retain positive median profits under these cost stresses. S3's composition-adjusted advantage is small and its median return falls with an extra day delay. None demonstrates a reliable edge. Next: predeclare an ex-ante passive-control comparison for unchanged S3, with weights fixed without future information; no new signal parameter sweep or automatic paper/live promotion.

[Full S1-003](../research/artifacts/S1/s1-003-attribution.json), [S2-003](../research/artifacts/S2/s2-003-attribution.json), [S3-003](../research/artifacts/S3/s3-003-attribution.json). 60 software checks passed; all 564 new ledgers audited. Holdout untouched, no new market data, three signal hypotheses retained.

## Later ideas

Pairs/cointegration, copulas, event-driven or cost-aware ML, on-chain/cross-sectional factors, regime models and advanced allocation are outside this POC. Candidate sources remain in [PAPERS.md](PAPERS.md). Existing repositories may provide reusable components after license and suitability checks; no new external-code audit was performed for this feedback update. Lower-frequency equity investing is a possible future direction, not current implementation scope.

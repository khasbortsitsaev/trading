# Resume here

Updated 14 November 2026. No background work is scheduled.

## Conclusions

| Experiment | Net growth | Drawdown | Decision |
|---|---:|---:|---|
| [S1-001: trend](../research/artifacts/S1/s1-001-summary.json) | +62.32% | 44.89% | Failed growth/drawdown screens |
| [S2-001: volume-confirmed trend](../research/artifacts/S2/s2-001-summary.json) | +46.99% | 27.02% | Failed ETH-relative growth screen |
| [S3-001: mean reversion](../research/artifacts/S3/s3-001-summary.json) | +58.39% | 30.64% | Failed growth/drawdown screens |

ETH holding returned +65.52% over the same development window. None of the three baselines is promoted. These are historical USD-source proxy results, not actual USDC fills, independent prospective evidence or a validated edge. Lower S2 drawdown is a defensive result, not a changed objective.

## Implementation and evidence

Shared offline signals, allocation, execution proxies, accounting and data loader are implemented. **57 software checks passed**, including S2 entry/hold/exit, boundaries and future-information checks; this does not mean investment success. S1's exact replay matches its original result hash. All three ledgers' daily equity and signal/timing checks reconcile. S3 signals were independently checked using Decimal logs/sample variance. Details: [strategies](STRATEGIES.md), [experiment registry](experiments.md).

Results live only under `research/artifacts/S1/` `S2/` and `S3/`, named with strategy-specific experiment IDs. Shared source/software evidence stays at the artifacts root. S1-001 was originally DEV-001; renaming preserved JSON bytes and result hashes.

Local data, if retained: `/workspace/work/s1-closeout/recovered-data`; S1 replay `/workspace/work/s1-closeout/replay.json`; S2 ledger `/workspace/work/s2-pilot/ledger.json`; S3 ledger `/workspace/work/s3-pilot/ledger.json`. Check these before downloading. Source/admission hashes and explicit recapture metadata are in policy; never bypass them. No raw data/full source-derived ledger in Git.

## Constraints and next task

POC is S1/S2/S3, one strategy at a time. All three baselines are closed; no historical variant active. Three trials used, cap 18 unchanged. Holdout **2025-11-13 inclusive to 2026-11-13 exclusive** stays sealed; never move dates with the calendar. No retuning or additional variants to rescue failures.

## Rolling-start analysis completed

User challenged single-date dependence. S1-002/S2-002/S3-002 evaluate every month-start 2021-01 through 2024-11 for 12 calendar months: 47 windows per method, 141 additional scenarios, no new signal variants or holdout. Each starts with owned ETH worth USD 1000; fixed dollars, same costs/state reset. Code/config commit c4cdd49. Full ledgers `/workspace/work/rolling/ledgers`; per-strategy public `sN-002-rolling.json`.

Beat ETH: S1 21/47, S2 20/47, S3 24/47. Median paired excess: -15.67/-14.45/+0.50 percentage points. S3 is mixed/start-sensitive, not a generally disproven strategy; S2 more defensive. Worst drawdowns 55.03%/42.45%/58.27%, ETH 79.29%. No promotion. Overlapping adaptive development windows are not independent tests. All 141 hashes, 51,501 daily equities, 19,298 fill timings and terminal returns/fees audited. All 57 software checks pass.

**Next:** discuss the rolling findings and growth/risk objective before registering a further bounded hypothesis. Do not pick the best starting date, retune parameters or inspect holdout. The three first-pilot failures remain specific to their original window; current evidence is broader but still not prospective validation.

Capital/cost/timing assumptions: `config/runner.json`; signals, screens, trial history and protected dates: `config/research-policy.json`. Capital is illustrative, not a constraint. Keep docs concise and conclusions separate from software checks. No live trading, leverage, borrowing, paid commitments or vendor messages authorized. Commit/push completed work and verify the remote.

User input for a next batch: discuss whether beating ETH remains essential or lower-growth/lower-drawdown outcomes are useful. No new run pending. Holdout untouched.

# Resume here

Updated 14 November 2026. No background work is scheduled.

## Current conclusion

Objective is a repeatable positive trading edge after costs with acceptable risk. ETH is available capital; ETH/BTC/cash are attribution references, not mandatory return hurdles. Removed the agent's two-percentage-point ETH CAGR rule. Original experiment files/old verdicts remain unchanged; no rerun or retroactive promotion.

Existing rolling development evidence: S1 profitable 26/47 windows, median return +6.66%, worst drawdown 55.03%; S2 30/47, +14.22%, 42.45%; S3 33/47, +21.86%, 58.27%. S2 has lower observed risk; S3 more profitable windows. No repeatable edge established: returns may reflect crypto exposure, windows overlap, and cost/parameter robustness/uncertainty/prospective evidence is missing. Fixed business costs/taxes are excluded. [Reassessment](STRATEGIES.md#current-objective-reassessment).

## Implementation and evidence

Shared offline signals, allocation, execution proxies, accounting and data loader are implemented. **57 software checks passed**, including S2 entry/hold/exit, boundaries and future-information checks; this does not mean investment success. S1's exact replay matches its original result hash. All three ledgers' daily equity and signal/timing checks reconcile. S3 signals were independently checked using Decimal logs/sample variance. Details: [strategies](STRATEGIES.md), [experiment registry](experiments.md).

Results live only under `research/artifacts/S1/` `S2/` and `S3/`, named with strategy-specific experiment IDs. Shared source/software evidence stays at the artifacts root. S1-001 was originally DEV-001; renaming preserved JSON bytes and result hashes.

Local data, if retained: `/workspace/work/s1-closeout/recovered-data`; S1 replay `/workspace/work/s1-closeout/replay.json`; S2 ledger `/workspace/work/s2-pilot/ledger.json`; S3 ledger `/workspace/work/s3-pilot/ledger.json`. Check these before downloading. Source/admission hashes and explicit recapture metadata are in policy; never bypass them. No raw data/full source-derived ledger in Git.

## Constraints and next task

POC is S1/S2/S3, one strategy at a time. All three pilots are complete, current edge status unproven; no historical variant active. Three trials used, cap 18 unchanged. Holdout **2025-11-13 inclusive to 2026-11-13 exclusive** stays sealed; never move dates with the calendar. No retuning or additional variants to rescue failures.

## Rolling-start analysis completed

User challenged single-date dependence. S1-002/S2-002/S3-002 evaluate every month-start 2021-01 through 2024-11 for 12 calendar months: 47 windows per method, 141 additional scenarios, no new signal variants or holdout. Each starts with owned ETH worth USD 1000; fixed dollars, same costs/state reset. Code/config commit c4cdd49. Full ledgers `/workspace/work/rolling/ledgers`; per-strategy public `sN-002-rolling.json`.

Beat ETH: S1 21/47, S2 20/47, S3 24/47. Median paired excess: -15.67/-14.45/+0.50 percentage points. S3 is mixed/start-sensitive, not a generally disproven strategy; S2 more defensive. Worst drawdowns 55.03%/42.45%/58.27%, ETH 79.29%. No promotion. Overlapping adaptive development windows are not independent tests. All 141 hashes, 51,501 daily equities, 19,298 fill timings and terminal returns/fees audited. All 57 software checks pass.

**Next:** register a bounded exposure/risk-matched passive-control comparison plus cost/delay robustness check, reusing the existing data and ledgers before running anything. No required ETH outperformance. Keep 30% drawdown as an agent research screen, not a live user preference; do not choose new risk thresholds based on these results.

Capital/cost/timing assumptions: `config/runner.json`; signals, screens, trial history and protected dates: `config/research-policy.json`. Capital is illustrative, not a constraint. Keep docs concise and conclusions separate from software checks. No live trading, leverage, borrowing, paid commitments or vendor messages authorized. Commit/push completed work and verify the remote.

User input needed now: none to define the next attribution protocol. Objective clarified; no new experiment in this reassessment, holdout untouched. All frozen evidence hashes checked unchanged.

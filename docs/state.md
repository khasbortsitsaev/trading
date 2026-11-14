# Resume here

Updated 14 November 2026. No background work is scheduled.

## Conclusions

| Experiment | Net growth | Drawdown | Decision |
|---|---:|---:|---|
| [S1-001: trend](../research/artifacts/S1/s1-001-summary.json) | +62.32% | 44.89% | Failed growth/drawdown screens |
| [S2-001: volume-confirmed trend](../research/artifacts/S2/s2-001-summary.json) | +46.99% | 27.02% | Failed ETH-relative growth screen |

ETH holding returned +65.52% over the same development window. Neither strategy is promoted. These are historical USD-source proxy results, not actual USDC fills, independent prospective evidence or a validated edge. Lower S2 drawdown is a defensive result, not a changed objective.

## Implementation and evidence

Shared offline signals, allocation, execution proxies, accounting and data loader are implemented. **49 software checks passed**, including S2 entry/hold/exit, boundaries and future-information checks; this does not mean investment success. S1's exact replay matches its original result hash. Both ledgers' daily equity and signal/timing checks reconcile. Details: [strategies](STRATEGIES.md), [experiment registry](experiments.md).

Results live only under `research/artifacts/S1/` and `S2/`, named with strategy-specific experiment IDs. Shared source/software evidence stays at the artifacts root. S1-001 was originally DEV-001; renaming preserved JSON bytes and result hashes.

Local data, if retained: `/workspace/work/s1-closeout/recovered-data`; S1 replay `/workspace/work/s1-closeout/replay.json`; S2 ledger `/workspace/work/s2-pilot/ledger.json`. Check these before downloading. Source/admission hashes and explicit recapture metadata are in policy; never bypass them. No raw data/full source-derived ledger in Git.

## Constraints and next task

POC is S1/S2/S3, one strategy at a time. S1 and S2 are closed; no historical variant active. Two trials used, cap 18 unchanged. Holdout **2025-11-13 inclusive to 2026-11-13 exclusive** stays sealed; never move dates with the calendar. No retuning or additional variants to rescue failures.

**Next:** specify one S3 mean-reversion pilot from the existing reversal code before inspecting its returns. Register entry, exit, sizing and checks before enabling it. Reuse the existing pipeline and [reuse review](../research/reports/repository-reuse-review.md); no framework migration needed.

Capital/cost/timing assumptions: `config/runner.json`; signals, screens, trial history and protected dates: `config/research-policy.json`. Capital is illustrative, not a constraint. Keep docs concise and conclusions separate from software checks. No live trading, leverage, borrowing, paid commitments or vendor messages authorized. Commit/push completed work and verify the remote.

User input needed: none for the S3 specification. Cleanup validation: all renamed evidence files are byte-identical, with current strategy links checked; no strategy runs performed.

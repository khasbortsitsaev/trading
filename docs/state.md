# Resume here

Updated 14 November 2026. No background work is scheduled.

**Conclusion:** the offline S1 pipeline is implemented; the first historical development test did not establish an edge. DEV-001 returned +62.32% versus +65.52% for ETH holding, with 44.89% drawdown. It failed the working growth/drawdown screens. [Evidence](../research/artifacts/dev-001-summary.json).

## Current scope

- POC: S1 trend, S2 volume/technical, S3 mean reversion. Complete S1 end to end before starting S2/S3. Other families and the eleven untested registered variants are paused, not automatically queued.
- Capital is illustrative and editable in `config/runner.json`, alongside baseline costs/timing. `config/research-policy.json` holds signals, validation and dates. Preserve old run settings and trial counts when editing.
- Keep docs short, reuse existing code, and keep each strategy's experiment entries/results distinct. Report conclusion, evidence, next step and user input needed after each completed step.
- No live trading, borrowed shorts, leverage, paid commitments or vendor messages are authorized.

## Existing implementation and evidence

`src/trading_research/` contains signals, allocation, delayed candle-proxy execution and spot accounting. `scripts/run_research.py` provides the complete offline path. All 41 tests pass after the feedback update, including a CLI check proving changed capital/default friction and an explicit friction override reach the run output. Earlier synthetic and historical ledger reconciliation are documented in [experiments](experiments.md). Synthetic results are software evidence only.

Development data: official Bitstamp BTC/USD and ETH/USD daily candles, 2020-01-01 through 2025-11-12, 2,143 gap-free rows each. Admission hashes are in the policy. USD prices with hypothetical USDC-like fees are proxy evidence, not actual Bitvavo fills or USDC wealth. Fixed BTC/ETH selection and uncalibrated execution costs remain limitations.

Local data, if retained: `/workspace/research-data/bitstamp-usd-development-v1/{manifest,normalized}.json`; full ledger `/workspace/research-data/dev-001-ledger.json`. Check for these before downloading. If missing, use the existing collector with unchanged development dates; review changed capture metadata/hashes rather than bypassing admission. Do not redownload to repeat a completed result.

**Holdout remains sealed:** 2025-11-13 inclusive through 2026-11-13 exclusive. Never move these dates with the calendar or access it to improve S1. One trial has been used; existing budget/multiplicity history is preserved.

Reuse review already completed: [framework/strategy review](../research/reports/repository-reuse-review.md). Freqtrade is the leading candidate, CCXT a potential data adapter and bt an allocation reference. Nothing was installed or parity-tested. Reuse this review; a migration or framework spike is optional only if it saves work on a concrete S1 gap.

Feedback-update validation: 41 tests passed and the committed-code synthetic CLI smoke run completed. No historical strategy rerun or holdout access.

## S1 close-out completed

The missing source data were recovered into `/workspace/work/s1-closeout/recovered-data`; normalized prices match the original admitted hash exactly. The recaptured manifest hash was explicitly reviewed/versioned in policy, retaining its predecessor. Replay `/workspace/work/s1-closeout/replay.json` at `412d8fd` matches the original result hash exactly; it adds no independent evidence or trial. Original public result unchanged.

All 41 tests passed after close-out; all 720 decisions' signals and 425 fills' causal timing checked. 247 active-state resizing fills generated only $4.16 of $155.92 direct modeled costs; signal entry/exit flips dominated costs. Concrete buy/sell/resize examples and concise interpretation are in [STRATEGIES](STRATEGIES.md); aggregate checks under [S1 evidence](../research/artifacts/S1/dev-001-closeout.json). The baseline is closed without promotion. Missing execution/robustness evidence is stated; no further checks or holdout access are needed to reject it.

## S2 specification completed

S2-TREND-VOL-20-1.5 is frozen in `poc.s2_spec` in the policy: positive 20-day price trend plus latest volume strictly above 1.5 times the prior 20-day average to enter; hold through low volume, exit at nonpositive price trend. Reuse daily sizing/accounting/execution. No performance claim. Its reserved slot replaces unexecuted TREND-365; cap 18, one used trial, disabled cross-sectional slots and sealed holdout unchanged. Old TREND-365 definition remains provenance, not an enabled run.

The CLI blocks historical runs while no executable pilot is active. S2 is specification only; do not interpret configuration as implemented capability. Plan/acceptance checks in [experiments](experiments.md#s2-001-volume-confirmed-trend-plan). No new sources, market-data reads or historical tests in this step. All 41 existing tests pass; the CLI guard was checked to reject a historical request before data loading/output.

## One next task

Implement S2's stateful signal and synthetic fixtures, then commit passing checks before enabling its one historical pilot. Reuse existing pipeline, keep outputs under S2, and preserve S1 results. Do not start other variants or inspect holdout. No framework migration needed.

**User input needed now:** none. The 1.5 volume threshold is an agent-selected, editable assumption; discuss alternatives before evaluation rather than fitting after seeing its result.

Completed work is committed and pushed to GitHub `main`, then checked against the remote. Detailed historical commands/results remain in [experiments](experiments.md), not duplicated here.

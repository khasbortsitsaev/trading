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

**Holdout remains sealed:** 2025-11-13 inclusive through 2026-11-13 exclusive. Never move these dates with the calendar or access it to improve S1. Two historical variants have been used; existing budget/multiplicity history is preserved.

Reuse review already completed: [framework/strategy review](../research/reports/repository-reuse-review.md). Freqtrade is the leading candidate, CCXT a potential data adapter and bt an allocation reference. Nothing was installed or parity-tested. Reuse this review; a migration or framework spike is optional only if it saves work on a concrete S1 gap.

Feedback-update validation: 41 tests passed and the committed-code synthetic CLI smoke run completed. No historical strategy rerun or holdout access.

## S1 close-out completed

The missing source data were recovered into `/workspace/work/s1-closeout/recovered-data`; normalized prices match the original admitted hash exactly. The recaptured manifest hash was explicitly reviewed/versioned in policy, retaining its predecessor. Replay `/workspace/work/s1-closeout/replay.json` at `412d8fd` matches the original result hash exactly; it adds no independent evidence or trial. Original public result unchanged.

All 41 tests passed after close-out; all 720 decisions' signals and 425 fills' causal timing checked. 247 active-state resizing fills generated only $4.16 of $155.92 direct modeled costs; signal entry/exit flips dominated costs. Concrete buy/sell/resize examples and concise interpretation are in [STRATEGIES](STRATEGIES.md); aggregate checks under [S1 evidence](../research/artifacts/S1/dev-001-closeout.json). The baseline is closed without promotion. Missing execution/robustness evidence is stated; no further checks or holdout access are needed to reject it.

## S2 baseline completed

S2's implemented volume-gated entry / stateful trend exit passed 49 tests. At code commit `60a6ead`, its one registered development pilot returned +46.99% versus ETH +65.52%, with 27.02% drawdown. Three of four continuous folds profitable; 270 fills, 306 skips, $60.62 direct modeled costs. Fails the ETH-relative growth screen; closed without promotion. Lower drawdown is a defensive result, not a validated growth edge.

[Result](../research/artifacts/S2/dev-001-summary.json) and [validation/folds](../research/artifacts/S2/validation.json). All 720 decisions' signal formulas and daily equities, fees/adverse costs and 270 fills' timing checked. Private ledger `/workspace/work/s2-pilot/ledger.json`; input remains `/workspace/work/s1-closeout/recovered-data`. Full executed command in experiments.md. Synthetic fixtures cover buys/holds/exits; default random-volume CLI smoke only exercised initial liquidation.

Policy now records two used historical trials and no active historical variant; cap 18 and sealed holdout unchanged. The old S1 and S2 results/settings remain preserved. No robustness/holdout escalation for these failed baselines; no retuning, new datasets or source requests.

## One next task

Specify one S3 mean-reversion pilot using the existing reversal code and reserved candidates. Choose one transparent parameter set before inspecting its returns, state its entry/exit/sizing and validation plan, then commit before enabling a historical run. Keep S3 artifacts separate. No framework migration or variant batch needed.

**User input needed now:** none. The user may discuss whether S2's lower-risk/lower-growth behavior is useful; do not silently change the growth objective to accept it.

Completed work is committed and pushed to GitHub `main`, then checked against the remote. Detailed commands/results remain in experiments.md.

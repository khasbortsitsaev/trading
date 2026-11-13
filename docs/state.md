# Resume here

Updated 13 November 2026. No background work is scheduled.

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

## One next task

Produce a compact S1 research close-out from the existing ledger: show an actual buy, a signal-driven exit and a daily resize, explain turnover/costs and the failed screen, and identify which execution/robustness evidence remains missing. Recover the admitted data only if needed. Do not launch the eleven-variant batch or build a general orchestration framework. S1 completion means an understandable, auditable conclusion, including rejection, not forcing a profitable result or trading live.

**User input needed now:** none. Before changing S1's exit/rebalance behavior, explain the tradeoff and register it as a new hypothesis; never overwrite DEV-001. Future live risk/venue choices remain separate.

Completed work is committed and pushed to GitHub `main`, then checked against the remote. Detailed historical commands/results remain in [experiments](experiments.md), not duplicated here.

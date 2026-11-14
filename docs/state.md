# Resume here

Updated 14 November 2026. No background work scheduled.

## Objective and conclusion

Seek repeatable positive trading returns after costs with acceptable risk. ETH/BTC/cash are diagnostic references, not mandatory outperformance hurdles. **No validated edge; no-go for deployment of S1/S2/S3.** S1 is cost-sensitive, S2's volume contribution is unidentified, unchanged S3 has no established incremental benefit. No new economic experiment is active.

MODEL-001 execution/risk repairs are complete: impossible reversal settings rejected and REVERSAL-5-2 disabled; S3's evaluated formula unchanged. Optional independently sourced intraday fills, explicit daily-close drawdown/OHLC risk bounds, suspension valuation flags, continuous-state reporting and causal/joint cost stresses are implemented. Synthetic checks establish behavior, not profitability. Historical drawdowns remain daily-close, within-window. [Contract](METHODOLOGY.md#quant-review-repair-contract-model-001).

## DATA-001 completed

Admitted official Bitstamp BTC/USD and ETH/USD 15-minute candles over the original development window **2020-01-01 inclusive to 2025-11-13 exclusive**: 205,728 rows per asset, 411,456 total, full gap-free coverage. All 418 captured response hashes/bounded requests and raw-to-normalized reconstruction verified. Daily recovered prices match the original admitted normalized hash exactly; only recovery metadata is versioned, with its predecessor retained. All 4,286 trade-OHLC aggregates and daily volume sums match exactly, no price tolerance needed. [Final audit](../research/artifacts/data-001-execution-audit.json), [source metadata](../research/artifacts/data-001-intraday-manifest.json).

Initial audit blocked admission on two daily-open mismatches, both 2020-04-26. Leading zero-volume source bars carried each previous close; the first positive-volume 00:45 bar agrees with the daily open. The [failed audit](../research/artifacts/data-001-initial-audit.json) is preserved. An explicit QA amendment after observing source data calculates trade OHLC over positive-volume bars, retains the complete grid, reports raw-all-bar mismatches and still checks all-bar daily bounds. No source price/date/tolerance or strategy parameter changed. BTC 107/ETH 226 zero-volume bars include 1/3 proposed 00:15 references. They remain in the source and cannot generate fills.

EXECUTION-15M-001 freezes a **research-only** schedule: daily close 00:00 UTC, assumed available 00:05, ready 00:10, first strictly later 15-minute reference 00:15. Historical publication latency and venue spread/depth remain unmeasured. Costs remain hypothetical cross-venue assumptions, not calibrated Bitvavo USDC fills. The daily runner default remains unchanged; future registered runs explicitly select `--execution-interval-minutes 15` and the admitted execution directory. Historical active_variant remains null.

Validation: 92 tests passed, including prior 81 and 11 new collector/admission/zero-volume fixtures. Collection/spec commit 27f89fb; final audited-code commit 704ef77. All 25 pre-existing public artifact hashes unchanged. Three used signal hypotheses, 846 additional dependent rolling/stress/control evaluations, cap 18/multiplicity 18 and zero promoted candidates retained. No economic run, holdout access, new hypothesis, order or provider message. These are data/software checks, not economic replication. Full historical strategy ledgers remain absent.

Local data now retained at /workspace/work/execution-data-001/{daily,intraday}/{manifest,normalized}.json with raw page bodies and hash-bound sidecars. Check/reuse these before downloading; verify policy admission hashes. Full source data remain outside Git. The existing collector resumes verified captured pages without network access and rejects altered cache metadata/bytes.

## One next task

Register one distinct mechanism-driven hypothesis within S1/S2/S3 with a cost-survival rationale and causal falsifying controls, continuous chronology, joint execution/cost stresses, dependence-aware uncertainty and prospective validation rules before economic evaluation. A volume claim needs causal ablation and exposure/turnover-aware controls, not just more cash. Do not rerun unchanged S3, tune to overlapping windows or automatically expand families. Actual execution-cost/availability calibration remains unresolved.

Holdout **2025-11-13 inclusive to 2026-11-13 exclusive** stays sealed and retrospectively designated. No live/paper orders, leverage, borrowing, paid commitments or vendor messages. Capital/default costs: config/runner.json; admitted data and frozen research process: config/research-policy.json. User input needed: none for preregistration.

## Quant review, 14 November 2026

Reviewed GitHub main at `e20d1f68361373d88b6d24a3cc280e8139aa0905`, after identifying that the attached checkout was older (`6905d63`). Conclusion: useful, cautious exploratory research; current no-validated-edge/no-promotion decision is supported. No economic strategy reruns, new hypotheses, source downloads or holdout access in this review.

Validation actually performed: all 61 current software tests passed. Independently recomputed all three rolling summaries, friction/delay summaries, composition-control win counts/paired medians and every S3-004 summary field from committed per-window records; these reconcile. Cross-checked reused S3 returns/drawdowns against S3-002. This verifies aggregate arithmetic, not independent market-data/ledger replication: raw normalized data, full ledgers and prior private audit scripts were absent in this environment. Current fees, source licensing and the unverified paper catalogue were not independently recertified.

Confirmed implementation/measurement findings:
- Dormant `REVERSAL-5-2` cannot enter under its current formula. An observation standardized against its own n-point mean and sample standard deviation has absolute z bounded by (n-1)/sqrt(n); n=5 gives 1.788854, below the entry threshold 2. Synthetic [100,100,100,100,0.01] prices attain z=-1.788854 without entry. This affects the paused candidate/neighbor registry, not evaluated S3 (`REVERSAL-20-1`).
- Drawdown uses daily closing equity only. A synthetic held-ETH day with open/close 100 and low 50 reports zero daily-close drawdown despite a 50% intraday decline. Label the measurement frequency; current drawdowns are not intraday risk or future loss bounds.
- Suspended held assets are blocked from trading but still marked from supplied closes without a stale/impairment/inconclusive flag. A synthetic all-suspended ETH holding produced +150% marked return and zero fills without a valuation-quality warning. This is a latent contract gap, not evidence the admitted BTC/ETH results experienced suspensions.
- Baseline execution is one full day after the signal candle closes: close 00:00, ready 00:10, fill next day 00:00. This is causal and disclosed, but a materially different execution assumption from trading after ten minutes. It can change either direction of performance, especially reversal. No faster-fill profitability claim follows.

Methodological judgment:
- All 47 twelve-month starts are useful sensitivity observations; adjacent windows share roughly eleven months. Fresh USD1000 portfolios and explicitly inactive S2/S3 startup states answer a fresh-entry question, not continuous multi-year compounding. The current state resets are intentional, documented behavior, not an initialization defect.
- S1/S2/S3 and subsequent controls were developed adaptively on reused history. Three signals and 846 additional evaluations are an audit trail, not independent evidence or a statistical correction. The retrospective historical holdout and public-price familiarity need the existing contamination disclosure and future prospective validation.
- S1-003/S2-003/S3-003 controls deliberately use future realized average weights; retain their diagnostic-only interpretation. S3-004 fixes that implementability issue but does not match realized exposure/risk. S3's 17/47 paired return wins and -7.46-point median excess weaken its practical case; they do not prove zero alpha or general mean-reversion failure. S3 has higher drawdown than the 50% control in 23/47 windows, so marginal median drawdowns do not establish uniform paired dominance.
- Fixed BTC/ETH selection, Bitstamp-specific volume, hypothetical cross-venue USD/USDC costs, uncalibrated constant friction, separate rather than joint cost/delay stresses and absent prospective uncertainty evidence still limit external validity. Positive medians are not expected annual returns. S2's lower risk/cost may reflect less exposure/turnover; predictive value from its volume gate remains unidentified.
- Current controls and broader regime coverage address limitations of the old S1-only checkout. Do not repeat those as omissions of current main. The provisional 30% drawdown screen and wide/dormant neighbor definitions remain research design choices requiring justification, not statistical facts.

Proposed follow-up: incorporate these findings into the POC decision, resolve parameter-validity/valuation and measurement-contract gaps before relying on future promotion checks, and require one explicit economic mechanism plus a prospective validation plan before new research. Preserve historical artifacts and all trial history. No further unchanged-S3 evaluation, strategy expansion or live deployment is authorized by this review. User input needed for this review: none.

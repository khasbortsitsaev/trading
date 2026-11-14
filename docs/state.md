# Resume here

Updated 14 November 2026. No background work scheduled.

## Objective and conclusion

Seek repeatable positive trading returns after costs with acceptable risk. ETH/BTC/cash are diagnostic references, not mandatory outperformance hurdles. **No validated edge; no-go for deployment of S1/S2/S3.** S1 is cost-sensitive, S2's volume contribution is unidentified, unchanged S3 has no established incremental benefit. Go for execution/data validation, not further threshold refinement.

MODEL-001 responds to the quant review below. Impossible reversal settings now fail before scoring; REVERSAL-5-2 is disabled with its original definition retained and affected neighbor plans explicitly incomplete. S3's evaluated formula is unchanged. Optional independently sourced intraday execution can use a 00:15 reference after 00:10 readiness; the legacy daily default still fills next day 00:00. Missing designated intraday bars never substitute later/daily prices. Historical intraday data have not been admitted.

New results label daily-close within-run drawdown, add a conservative OHLC drawdown upper bound and flag held suspensions as valuation-inconclusive, with zero-recovery valuation bounds instead of invented exits. A synthetic 50% intraday fall/recovery now shows 0% daily-close drawdown and a 50% upper bound. Optional prior-completed-bar range stress and joint friction/daily-delay settings are supported software scenarios, not calibrated costs or historical performance evidence. One run retains balances, signal states and pending targets continuously; reset rolling windows cannot represent multi-year compounding. [Contract and POC decision](METHODOLOGY.md#quant-review-repair-contract-model-001).

## Evidence and validation

[Rules/comparisons](STRATEGIES.md), [experiment history](experiments.md). Historical S1/S2/S3 artifacts remain byte-identical. Three used signal hypotheses, 846 additional dependent rolling/stress/control evaluations, zero promoted candidates and cap18/multiplicity18 are preserved. Historical drawdowns are daily-close, within-window. The 47 overlapping twelve-month starts are not independent trials; profitable fractions are not future probabilities and medians are not expected annual returns.

MODEL-001 software validation: 81 passing tests including the original 61, plus a separate 12-case synthetic comparison with reviewed code d19725b. All original economic metrics, decisions, fills, balances and costs match under legacy daily settings. New fixtures cover impossible thresholds, independently hash-bound CLI intraday data, strict readiness, missing/duplicate/holdout references, future perturbations, crash/recovery risk, noncoincident asset extrema, held/unheld suspensions, continuous signal memory and causal/joint cost stresses. Synthetic results establish software behavior only. Committed-code CLI smoke results will be recorded in the MODEL-001 experiment entry.

No historical strategy run, new source download, new economic hypothesis or holdout access. Local normalized data/full historical ledgers remain absent; no claim of independent historical fill reconstruction. Actual execution timing, venue spreads/volume transferability, exposure/risk-matched controls, dependence-aware selection uncertainty and prospective returns remain unresolved.

## One next task

Specify and admit same-source/quote intraday development data, freezing intended execution cadence, publication/processing assumptions and cost calibration before a distinct mechanism-driven economic experiment. No further unchanged-S3 evaluation or automatic strategy-family expansion. A future S2 volume claim needs causal ablation and exposure/turnover-aware falsifying controls, not just more cash.

Holdout **2025-11-13 inclusive to 2026-11-13 exclusive** remains sealed and retrospectively designated. No live/paper orders, leverage, borrowing, paid commitments or vendor messages. Capital, execution grid and cost stress: config/runner.json; signals, invalid-neighbor annotations and trial history: config/research-policy.json. User input needed: none for the next research specification.

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

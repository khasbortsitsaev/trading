# Resume here

Updated 14 November 2026. No background work scheduled.

## Objective and conclusion

Seek repeatable positive trading returns after costs with acceptable risk. Existing ETH is available capital; ETH/BTC/cash are attribution references, not mandatory outperformance hurdles. The retired ETH hurdle is preserved only in historical reports. No validated edge or live authorization.

All three POC pipelines run end to end. Across 47 overlapping monthly-start 12-month windows: S1 median +6.66% / worst drawdown 55.03%; S2 +14.22% / 42.45%; S3 +21.86% / 58.27%. Costs weaken S1; S2/S3 retain positive stress medians but that alone does not establish an edge.

**Latest S3-004:** fixed ex-ante 25/50/100% crypto targets, equal BTC/ETH within crypto, rest cash. One initial delayed/costed rebalance then hold quantities; no future-informed weights, but not exact exposure/risk matching. At 50%, median return +21.32%, median drawdown 24.89% versus S3 +21.86% / 30.60%. S3 wins only 17/47 matched windows, median paired excess -7.46 points. All three references reported, no winner selection. Evidence weakens usefulness of unchanged S3; no promotion or general rejection of mean reversion.

## Evidence and implementation

[Strategy rules and full comparisons](STRATEGIES.md); [experiment commands/history](experiments.md). Results under research/artifacts/S1/, S2/, S3/, named sN-001 (original), -002 (rolling), -003 (hindsight composition/stress); S3-004 fixed-control results. Prior report bytes/decisions retained. Software correctness is separate from investment performance.

Latest published evidence checkpoint: `13d25fc` (S3-004 report). Latest executed code/configuration commit: `f0f93a4`; 61 software checks passed. S3-004 audit: 141 hashes, 51,501 daily equities, 282 fill cash/fee/timing checks; quantities fixed after initial rebalance. Total additional evaluations 846, original signal hypotheses three. Overlapping adaptive windows are dependent and not unseen final evidence.

Local data if retained: /workspace/work/s1-closeout/recovered-data; rolling baseline ledgers /workspace/work/rolling/ledgers; stresses /workspace/work/attribution/ledgers; fixed controls /workspace/work/fixed-controls/ledgers. Check before downloading, verify policy admission hashes. No raw/full source-derived ledgers in Git. Existing audits/collectors should be reused.

## One next task

Prepare a concise POC go/no-go recommendation, identifying what evidence is useful/missing and whether one distinct mechanism-driven hypothesis within S1/S2/S3 merits registration. Do not run more controls on unchanged S3, optimize thresholds or automatically expand families. No further experiment is pending.

Numerical risk screens remain provisional agent research assumptions, not user live limits. No active historical variant; three used hypotheses, cap18 unchanged. Holdout **2025-11-13 inclusive to 2026-11-13 exclusive** remains sealed, never move with calendar. No paper/live orders, leverage, borrowing, paid commitments or vendor messages authorized.

Capital/cost/timing: config/runner.json; signals/validation/scenario counts: config/research-policy.json. Keep docs concise, separate strategies, reuse implementation. Commit/push completed work and verify remote. User input needed now: none to prepare recommendation. Latest documentation sync checked result links, completed experiment statuses and scenario counts; no new simulations or evidence changes.

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

# Research decision criteria and experiment protocol

Version: 0.1, 13 November 2026. Covers original review points **3 and 5**. This is a concrete proposed first-batch protocol, not a validated strategy, a return forecast or live authorization. Agreed constraints come from [DECISIONS.md](DECISIONS.md); numerical research thresholds below are **proposals requiring confirmation before any real-data search**. Publishing this specification does not mark them accepted.

## Purpose and authority

The objective is capital growth from 0.5 ETH, without scheduled withdrawals. The agent performs research, implementation and reproducibility work. The user decides consequential changes: benchmark tradeoffs, research acceptance thresholds, paid commitments, borrowing, venue funding and live allocation. No personal time limit is imposed. A finite experiment budget controls selection bias and scope, not the user's willingness to spend time.

The agent may build and verify the independent synthetic accounting prototype while these proposals are reviewed. Real-data searches require frozen criteria, a completed dataset manifest, an execution specification and resolution of the applicable data-use conditions in [FEASIBILITY.md](FEASIBILITY.md). Do not request credentials merely to run public-data or synthetic work.

## Point 3: proposed research acceptance gate

### Agreed economic measurements

Initialize a ledger with exactly 0.5 ETH. Use USDC as primary research numeraire, with ETH-equivalent wealth and EUR reporting using timestamped conversion marks. Compare on identical dates with holding the original 0.5 ETH, a no-trade quote-cash benchmark with its necessary initial conversion, and the fixed simple strategy baseline. Report BTC holding diagnostically; do not silently substitute it as the success benchmark.

Compute returns on portfolio equity after commissions, spread/slippage and actual required conversions. Show fixed operating/data costs separately and also include them in economic net growth. Report gross and net returns, CAGR, maximum drawdown and time under water, daily return volatility, Sharpe/Sortino with disclosed conventions, turnover, capital utilization, costs, gross exposure and terminal wealth. Mark ratios undefined when denominators or sample sizes do not support them. Cash/stablecoins are not assumed risk-free or yield-bearing.

CAGR uses elapsed UTC seconds divided by 365.25 days; report nonannualized growth as well. Maximum drawdown is the largest decline from an equity high-water mark. Loss from initial capital is a separate metric. A promising risk-adjusted result that loses capital does not meet the current objective.

### Proposed numerical defaults, not agreed preferences

These values are deliberately specified before any strategy returns are examined. They are research screening choices, not values supported by a completed power analysis or guarantees against future losses. They must be confirmed or revised once before searches; do not relax them after seeing results.

| Test | Proposed gate | Meaning |
|---|---|---|
| Absolute growth | Net CAGR greater than 0 after declared execution and recurring costs | Reject losing capital even if a comparison asset lost more |
| ETH opportunity cost | Net CAGR at least **2 percentage points/year above ETH holding** | Proposed primary capital-growth hurdle; user choice between this and a defensive objective remains open |
| Drawdown | Maximum drawdown no greater than **30%** on stitched development OOS and final holdout separately | Research proposal only; it does not set a live stop or imply losses will be bounded |
| Consistency | Positive net return in at least **3 of 4** chronological development test folds | Avoid selecting solely on one favorable segment; not a claim of independence |
| Cost resilience | Positive net growth and positive terminal excess wealth versus ETH under commissions plus **30 bps total noncommission round-trip friction** | Stronger than the proposed 15-bps baseline friction; execution model allocates this by traded notional |
| Parameter stability | At least **3 of 4** predeclared neighboring variants retain positive net growth and positive ETH-relative terminal wealth on development OOS | The neighbors cannot be used to replace a failed champion or to tune after holdout |
| Concentration | Masking the best development month must leave positive net growth and positive ETH-relative terminal wealth | A sensitivity check, not the return series used for ranking |
| Dependence-aware uncertainty | A multiplicity-adjusted lower confidence bound for mean daily log growth in excess of ETH must exceed 0 on development OOS | If evidence is too weak or the method is invalid for the sample, label inconclusive rather than invent certainty |

A **defensive research result** may be reported separately if it grows capital but fails ETH outperformance while reducing drawdown. It does not automatically pass the capital-growth gate. Before searches, the user must choose whether that tradeoff is an acceptable alternative objective; no alternative defensive threshold has been silently approved. The provisional 20-50% live drawdown discussion is not used to justify the 30% proposal.

Missing data, insufficient independent information, unresolved financing or unverified execution assumptions can make an otherwise attractive result **inconclusive**. A confirmed accounting/look-ahead defect makes it **invalid**, not merely a poor strategy.

### Decision outcomes

- **Reject:** reliable evaluation fails a frozen economic or robustness requirement. Preserve the negative result; no automatic expansion into ML or new parameter searches.
- **Invalid:** a correctness, timing or reproducibility defect compromises the run. Fix the defect under a new artifact/version and rerun the affected registered analysis; retain the failed run and contamination record.
- **Inconclusive:** data, uncertainty or execution evidence is inadequate. State precisely what would resolve it. Do not open the holdout to compensate for weak development evidence.
- **Candidate for prospective paper validation:** all development gates and the single frozen holdout assessment pass, with feasibility conditions met. This is not permission for live trading or a declaration of profitability certainty.

## Point 5: bounded first research batch

### Search budget and representative families

Proposed batch cap: **18 selection variants**, at most six each for trend, reversal and cross-sectional momentum. Cross-sectional variants run only after point-in-time eligibility/data checks pass. If that family is infeasible, leave its six slots unused; do not silently redistribute them. The exact signal rules, six variants per family, parameter neighbors and allocator must be specified in the experiment entry before any real-data evaluation. No strategy parameters or paper reproductions are asserted here.

A variant means a complete selection-relevant pipeline: signal rules, parameter choice, universe, exchange, timeframe, allocation, cost assumptions and seed. Changing any of these after seeing returns is a new variant. Passive ETH/cash controls are not search variants; a tradable momentum baseline is. All failed, abandoned and unfavorable variants count. Fixing code is not a free new hypothesis: record the defect, affected reruns and any new information exposed.

Use one fixed execution venue/data route, one declared daily decision schedule and one simple fixed allocation rule for the first batch, chosen on feasibility before results. This does not narrow the long-term strategy catalogue or impose a position-count cap. No ML, RL, signal ensemble, risk-parity or ICVP search in this batch. Such methods later need separately budgeted incremental evidence.

### Chronological data partition

Proposed minimum usable history: **1,815 daily observations** after quality exclusions and indicator warmup: 730 initial training days, four nonoverlapping 180-day development test windows, and 365 final holdout days. Warmup and any boundary purging require additional history. These are minimum information requirements, not a guarantee of adequate statistical power. Do not compress the windows merely because a preferred USDC market has shorter history; narrow the evidence label or obtain an adequate permitted source.

Before loading strategy-dependent returns, use coverage metadata to assign exact half-open UTC boundaries and commit the split manifest. The final 365 observations are held aside from selection. On development data, each fold trains on all eligible preceding observations, chooses any fitted transformations/parameters using an inner chronological split, and evaluates only the next 180 days. Inner split: final 180 eligible days of that fold's training period serve as validation, the earlier part as fitting data; purge boundaries as required. Fixed-rule strategies still follow the same evaluation boundaries without pretending they require statistical fitting.

Outer folds contain no overlapping scored return periods. Carry the portfolio continuously across the development OOS windows; if the algorithm retrains or changes targets, charge actual rebalance costs. Do not reset each fold to fresh capital or hide boundary trading costs. Reset the holdout to the same declared initial endowment for its separate evaluation; separately report an optional continuous-path deployment simulation if preregistered.

Fit scalers, imputers, eligibility filters, liquidity thresholds and learned models using training information only. No shuffled K-fold. If labels, feature lookbacks or target holding events cross a boundary, record their information/label intervals. Purge training labels that overlap the held-out interval and remove any other future-dependent rows. A gap/embargo is derived from the largest declared relevant horizon, with a minimum one decision bar; expand it if the design requires it. In strictly forward expanding folds there is no later training block immediately after the test block, so do not apply a ceremonial symmetric embargo and claim it solved leakage.

### Selection, uncertainty and robustness

For each variant, stitch only genuinely outer-test daily equity returns. Rank variants that pass the basic development economic gates by net OOS CAGR; ties within 0.1 percentage point/year prefer lower turnover, then fewer fitted parameters, then the preregistered variant ID. Select **one champion**. Do not compare final-holdout outcomes across 18 variants to choose a winner.

Proposed uncertainty method: paired circular moving-block bootstrap of daily log strategy and ETH returns, 2,000 replicates, seed 20261113. Use block lengths **7, 30 and 90 days** as declared dependence sensitivities, preserving strategy/benchmark pairing. Require a lower bound above zero at each length with a conservative one-sided per-variant error level `0.05/18` for the development selection family. Blocks cannot manufacture independent regimes; evaluate stationarity, block adequacy and effective information. Two thousand replicates may be coarse in the adjusted tail; increase to 20,000 for the champion before a gate decision, retaining the first output. Numerical precision improvement is not a new parameter search. These are proposed heuristics, not a claim of exact finite-sample error control under changing markets. Report inconclusive if a valid uncertainty claim is not supported. Sharpe significance alone does not pass this gate.

For the champion, preregister the following **nine development robustness assessments**, with frozen selection and no replacement winner. Four reuse already budgeted neighboring-variant results; at most five require additional scenario evaluations:

1. 30-bps total friction beyond commissions (mandatory cost gate).
2. 50-bps total friction beyond commissions (severe diagnostic; failure is reported, not hidden).
3. One extra decision-bar execution delay beyond the baseline (must retain positive net growth and positive ETH-relative terminal wealth).
4-7. Four predeclared neighboring parameter configurations already included in the original 18 selection slots (the 3-of-4 stability gate; reuse those results, do not introduce four unbudgeted variants).
8. Mask the best development calendar month by setting both strategy and paired benchmark daily log returns to zero during that month, retaining the calendar denominator (mandatory concentration diagnostic gate; not an executable counterfactual strategy).
9. Remove the largest net-P&L-contributing asset through a declared position-exclusion counterfactual, retaining its would-be allocation in cash without reallocating it to other assets (diagnostic; if there is only one traded asset, report not applicable and do not claim diversification).

Also report month/asset P&L attribution and calendar-year or preregistered past-only regime breakdowns from the same return streams. These tables are not new fitted variants. Sensitivities overlap and are not independent confirmations. Do not sweep combinations of these scenarios unless a new budget is declared.

Maximum planned evaluation units: 18 outer-development pipelines plus five additional champion scenarios, each with four outer folds: **92 outer fold/scenario evaluations**. The four neighbor assessments reuse the original results and do not create new selection slots or independent evidence. Inner training evaluations and bootstrap replicates must also be counted explicitly in the run ledger; they are not additional independent evidence. This is a finite first batch, not a ceiling on future justified research.

### Holdout control

Before opening the final period, commit the selected algorithm/configuration, parameter-selection procedure, data/split hashes, fee/execution policy, failure criteria and champion ID. Record the access event in [experiments.md](experiments.md): who/what opened it, time, artifact hashes and results produced. Use a separate evaluation entrypoint; do not allow optimization code to read the final partition.

A frozen walk-forward algorithm may refit on earlier observations as time advances through the holdout only if the update rule was fixed before access; no human tuning on holdout results. Report this as sequential evaluation, not as training on future data. Open once for the declared evaluation bundle: one selected algorithm, its baseline and two already frozen cost/delay scenarios, not a candidate search. Apply the same absolute-growth, ETH-margin and research-drawdown gates to the aggregate 365-day period, and report the frozen 30-bps friction scenario and extra-delay sensitivity. Do not demand four-fold consistency or tune neighboring parameters on this one-year period.

Historical holdout means unaccessed by this project's strategy-selection process, not unknown to the world or immune to paper/publication contamination. Record prior awareness of prices, papers and outcomes. Prospective paper validation is still required. If holdout access leaks into development, reclassify the evidence and select genuinely fresh data or wait for future observations; renaming the same data does not restore independence.

### Batch stop and handover

If the champion fails a mandatory development sensitivity, close the batch with the failure; do not silently promote runner-up candidates. If it fails holdout, preserve that result and close the batch without holdout-driven fixes. A new batch needs a different predeclared rationale, retained trial history and a genuinely valid evaluation plan; increased complexity alone is not a rationale. No profitable candidate is a valid outcome.

All experiment records must include actual fit/run counts, dataset/execution versions, code commit, seeds, costs, exclusions, environment, exact commands and artifact paths. Commit executable code/configuration before running and commit resulting reports separately. Only code-backed executed checks may be marked passed; this document alone implements none of these controls.

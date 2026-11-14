# Current decisions

| Topic | Decision |
|---|---|
| Objective | Find a repeatable positive trading edge after costs with acceptable risk; no validated edge yet |
| Capital | Existing ETH is available capital, not an investment mandate; amount is configurable |
| Benchmarks | ETH/BTC/cash are diagnostic references, not mandatory outperformance hurdles |
| POC | S1/S2/S3 first; shared pipeline, separate experiment/results folders |
| Scope | Fully funded long/flat spot; no leverage, borrowing or fixed position-count cap |
| Currency/venue | USD/USDC-source research; Bitstamp prices and hypothetical execution costs remain distinct from actual fills; venue undecided |
| Risk | 30% drawdown and positive-fold rules remain provisional research screens; no user-approved numerical live risk limit |
| Evidence | Profitability, risk, exposure attribution, costs, robustness and prospective validation; positive backtests alone are insufficient |
| History | Old ETH-relative verdicts remain in frozen reports; no strategy is currently rejected solely for underperforming ETH or retroactively promoted |
| Validation | Chronological evaluation, all trials retained, overlapping windows dependent, sealed holdout untouched |
| Working style | Concise conclusions and editable assumptions; reuse code/tools, separate software correctness from economic evidence |
| Authority | Commit/push completed work; live orders, paid commitments, vendor messages and borrowing require separate authorization |

Objective corrected following the user's clarification: the mandatory two-point ETH CAGR margin is removed. Signals, dates, costs and old results are unchanged. No new simulation is needed to acknowledge this correction. The bounded control/robustness analyses are complete; results remain insufficient to establish an edge. Do not infer a reliable edge from positive returns or monthly-window win rates.

S3-004 fixed ex-ante passive controls completed: similar median return but higher drawdown than the 50% crypto/cash reference, only 17/47 paired wins. No clear incremental value established. Stop further evaluation of unchanged S3; prepare the POC recommendation before any new mechanism-driven hypothesis. This is an evidence assessment, not a reinstatement of a mandatory buy-and-hold hurdle.

Quant-review response, 14 November 2026: improve execution and risk measurement before any new strategy. Retain historical artifacts and the original daily default; add an optional independently admitted same-source/quote intraday reference path without claiming faster-fill profitability. Quarantine impossible REVERSAL-5-2 without changing the formula or selecting replacement neighbors. Report daily-close risk separately from conservative OHLC bounds; held suspensions block valuation eligibility. Joint cost/delay and prior-bar-range friction are available software scenarios, not newly observed economic evidence. No-go for POC deployment, go for measurement/data validation. Next admit intraday development data and freeze the intended execution process; no user input required for that research specification.

DATA-001 registers same-source BTC/ETH USD 15-minute development-data admission over the unchanged original dates. Freeze EXECUTION-15M-001 as a research-only cadence (close 00:00, assumed ready 00:10, reference 00:15 UTC), selected explicitly for later registered experiments. Keep the daily default and old results unchanged. This specifies timing; historical spread/slippage/publication latency remain uncalibrated. No strategy is activated by data admission.

DATA-001 completed: admit the full original-development 15-minute BTC/ETH USD source grid after exact traded-OHLC/volume reconciliation. Retain the initial failed all-bar aggregation audit and explicit post-observation zero-volume interpretation amendment. No raw row is removed or edited; zero-volume execution references expire unfilled. Daily recovered prices are identical and recapture metadata is versioned. No active strategy or new economic evidence. Next task supersedes data admission above: register a distinct mechanism-driven hypothesis and falsifying/continuous/prospective validation before any economic run.

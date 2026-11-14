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

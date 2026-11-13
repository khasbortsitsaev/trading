# Development roadmap

## Priority: close the six review items before strategy development
The original project review takes precedence over expanding the software platform. Complete a preliminary feasibility pass and freeze the research protocol before implementing real-data strategy experiments. Keep the broad catalogue; do not build every capability upfront.

| Priority | Required output | Gate |
|---|---|---|
| 1. Exchange and data feasibility | Dated primary-source comparison of a small venue shortlist: eligibility for the intended jurisdiction, spot products/pairs, order minimums/precision, liquidity, historical coverage and delistings | At least one plausible spot research route; unresolved access must remain explicit |
| 2. Market-specific costs | Venue + pair + order type + volume tier cost sheet; commission, spread, slippage and conversion provenance; break-even cost method | Original all-in scenarios alone cannot establish feasibility |
| 3. Project decision criteria | Capital-growth objective, benchmarks, economic success/rejection criteria and unresolved live-risk decisions | Numeric research criteria and a finite trial budget frozen before searches |
| 4. Shorting constraint | Fully funded spot as initial scope; separate feasibility and financing/collateral specification for any borrowed short | No short-dependent executable claims without feasibility and a separate decision |
| 5. Research protocol | Predeclared hypotheses/searches, chronological splits, holdout access rule, robustness checks and stopping rules | Registry entry before every experiment; no unlimited complexity escalation |
| 6. Data and execution specification | Point-in-time universe, timestamps, quality policy, data licensing, fills and independent-observation assessment | Data must support the claimed execution behavior |

These are required work products, not completed findings. See [methodology](METHODOLOGY.md) for their specifications. Verify the pasted review's fee and paper claims from primary sources before adopting them. An exclusion from the venue shortlist is a project choice, not independent evidence of a venue's regulatory or operating status. Keep personal eligibility details outside this public repository.

## Review outputs and remaining gates (2026-11-13)

| Point | Concrete artifact | Current status |
|---|---|---|
| 1 | [FEASIBILITY.md](FEASIBILITY.md) | Preliminary comparison complete; permissions, selected history and actual account availability open |
| 2 | [COSTS.md](COSTS.md) | Current public commissions and small book scenarios checked; realized slippage/account rates not calibrated |
| 3 | [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md), [research-policy.json](research-policy.json) | Numeric gates and benchmark tradeoff proposed, not yet accepted/frozen |
| 4 | [RISK_SCOPE.md](RISK_SCOPE.md) | Agreed spot-only initial scope formalized; any borrowed-short route separately gated |
| 5 | [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) | Concrete bounded search/splits/holdout protocol drafted; no experiment has executed it |
| 6 | [DATA_EXECUTION.md](DATA_EXECUTION.md) | Data/causal-fill contract specified; ingestion/backtester controls not implemented |

The six review items now have work products. This is not a claim that all admission gates have passed. Keep agent-proposed criteria distinct from user decisions and implementation checks distinct from written requirements.

## Phase 1: feasibility and protocol
Complete the six outputs above. Maintain the research catalogue and audit sources needed by the first selected hypotheses. Reject infeasible hypotheses or narrow their claims. Record a proceed, narrow-scope or stop decision with evidence and unresolved items. No exchange credentials or paid subscriptions are needed for the initial desk research. Paid commitments require an explicit decision.

## Phase 2: minimal accounting platform
After the preliminary review, create a Python scaffold with deterministic synthetic data, a transparent momentum baseline, ETH/cash benchmarks and reproducible reports. Test P&L, fee arithmetic, exposure limits and signal-to-fill timing. Synthetic results establish software behavior only. Add one verified historical dataset after its data specification passes. Do not add execution integration.

## Phase 3: bounded experiments
Predefine representative trend, reversal and cross-sectional momentum hypotheses that fit feasible data and fully funded spot. Start with one end-to-end baseline. Keep short-dependent methods gated. Record all trials and failures. Complex ML, regime selection and allocation methods must justify incremental out-of-sample value over simple baselines, including costs.

## Phase 4: validation and research decision
Use nested chronological walk-forward validation, purging/embargo where labels overlap, and a sealed final holdout. Test higher costs, delayed execution, nearby parameters, asset/month/regime concentration and dependence. Report absolute and risk-adjusted performance separately. End the bounded batch with proceed, reject or inconclusive; do not automatically expand complexity after negative results.

## Phase 5: prospective paper trading
Only after a research go/no-go decision: validate signals, operational reliability and modeled execution prospectively. Recheck venue eligibility, costs and data access. Paper fills remain estimates.

## Phase 6: optional live trading
Requires explicit separate authorization, firm loss/stop rules, capital allocation, monitoring and recovery procedures. Historical and paper profitability do not guarantee future profitability or prevent initial losses. No live authorization exists.

## Next concrete task
Confirm or revise the proposed point 3 research thresholds and benchmark tradeoff, then freeze the applicable protocol version before real-data searches. Independently prepare and preregister the synthetic multi-asset portfolio-accounting prototype required by DATA_EXECUTION.md. Implement and verify cash/inventory, fees, minimums, multiple positions, ETH/cash benchmarks and causal signal-to-fill timing. Do not ingest a strategy dataset or open a holdout until the remaining point 1/2/3/5/6 gates pass. No platform expansion into ML, borrowed shorts or exchange execution.

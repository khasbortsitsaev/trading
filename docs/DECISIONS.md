# Decision log

As of 2026-11-13. Decisions may change with evidence.

| Topic | Decision | Status |
|---|---|---|
| Purpose | Short-horizon systematic crypto trading research for possible eventual profits, not a 40-year passive portfolio | Agreed |
| Starting capital | 0.5 ETH | Agreed |
| Research currency | USDC / USD equivalent; compare against ETH hold and cash | Agreed |
| Universe | Data-driven, possibly 10-20+ coins; no fixed cap | Open selection |
| Position count | No fixed cap | Agreed |
| Long / short | Both may be studied | Agreed |
| Leverage | No leveraged portfolio exposure desired | Agreed |
| Trading frequency | Determined by signals and after-cost evidence; avoid uncompetitive HFT | Open |
| Fees | Original 0.15%/0.25%/0.50% all-in cases retained as legacy sensitivity cases; use verified venue/pair fees and explicit friction scenarios in COSTS.md | Current public fees verified; account rates and realized friction open |
| Execution venue | No final exchange; Bitvavo is the initial cost reference only. Compare fees, liquidity and available quote pairs | Open |
| AI role | AI-assisted research and development; trading decisions should be explicit and testable | Agreed |
| Validation | Chronological walk-forward, untouched holdout, cost and robustness tests | Agreed |
| Live trading | Only after research, forward paper trading and separate approval | Agreed |

## Clarifications
- Earlier suggestions of EUR 500 and a maximum of two positions were assistant assumptions explicitly rejected.
- ICVP (Independent Component Variance Parity) is a candidate **allocation** method, not a standalone prediction signal.
- The user does not want research to focus narrowly on one paper or pairs trading.
- Published best-performing pairs can be candidates, but selecting them based on their published out-of-sample performance creates selection bias for our own evaluation.
- We need not replicate every paper exactly; papers are starting points for well-defined, testable hypotheses. When modifying a published strategy, preserve a clear distinction between original and modified variants.

## Additional context (2026-11-12)
- Current objective: capital growth, with no planned withdrawals. Potential future passive operation remains unproven; live operation requires separate authorization.
- BTC dependence is an early research hypothesis, not a validated trading signal.
- See [Income objective and BTC research notes](OBJECTIVE_AND_BTC.md) for proposed tests, economics and open questions.

- Cost provenance clarified by the user on 2026-11-12: the initial estimates were based on Bitvavo. They must not be described as exchange-independent or replaced by another venue's fees without an explicit comparison. The venue remains undecided.

## Review priorities and clarified scope (2026-11-12)
- Agreed: tackle the six original review items in ROADMAP.md first, before real-data strategy development.
- Agreed: initial research allocation remains 0.5 ETH; additional capital may be discussed if evidence supports it. No automatic increase is authorized.
- Agreed: fully funded spot first, with no leverage. Borrowed shorts are acceptable in principle for investigation, but financing, collateral and liquidation risks need a separate feasibility assessment and decision. Gross exposure alone does not eliminate those risks.
- Agreed: the agent performs research/development; the user makes consequential decisions. No personal time budget currently blocks progress. Paid commitments require a decision; use public/free resources initially.
- Provisional: a broad 20-50% possible live drawdown tolerance was discussed. This is not a chosen risk limit, research acceptance threshold or authorization to lose 50%. Define drawdown from the equity high-water mark and separately define loss from starting capital before live allocation.
- Open: numerical research acceptance thresholds, finite trial budget and operational stop rules. Strong backtests cannot eliminate live losses.
- Venue selection remains open; apply privately supplied jurisdiction and venue exclusions during feasibility research. Do not place personal eligibility information in this public repository.

## Cost review and publication workflow (2026-11-13)
- The user instructed that completed project work must always be committed and pushed to GitHub. This is now a standing rule in AGENTS.md; do not confuse a local file or cloud snapshot with repository publication.
- Current primary-source evidence supports prioritizing Bitvavo crypto/USDC for a low-cost baseline, subject to unresolved feasibility conditions. This is a research recommendation, not final exchange selection.
- Published entry-tier taker fees per execution: Bitvavo Category B 0.05%, Category A 0.25%; Kraken regular spot tier 1 0.80%, following the documented July 2026 change. Spread/slippage must be added or represented in bid/ask fills, without double counting.
- The small deterministic calculator uses a synthetic quote-fee convention; it does not establish actual fee currency, account rates or maker fills. Six checks passed; no strategy profitability result exists.

## Remaining review specifications (2026-11-13)
- Point 3: capital growth, 0.5 ETH and ETH/cash comparisons remain agreed. RESEARCH_PROTOCOL.md proposes a 2-point annual net growth margin above ETH, a 30% research drawdown ceiling and associated evidence/robustness gates. Numerical values and the defensive-versus-growth benchmark tradeoff remain unapproved; no live limit is chosen.
- Point 4: RISK_SCOPE.md implements the already agreed fully funded long/flat spot scope as explicit ledger/allocation constraints. Borrowed shorts remain investigable in principle, but require separate product, collateral, financing and liquidation evidence plus a user scope decision. No borrowing or leveraged product belongs to the initial batch.
- Point 5: proposed finite batch of at most 18 selection variants, four chronological outer folds, one champion and one sealed holdout access bundle. Four neighboring-parameter checks reuse existing variants rather than expanding the search. These values remain proposed until frozen before experiments; no runs have occurred under them.
- Point 6: DATA_EXECUTION.md defines provenance/availability schemas, point-in-time eligibility, gaps/delistings, causal delayed fills and portfolio acceptance fixtures. These are implementation requirements, not implemented capabilities.
- The six topics are specified at planning/preliminary-evidence level. Real-data permissions, complete history, actual execution calibration and numerical policy confirmation remain admission gates. Synthetic development is the next independent coding task; no real-data strategy search or live deployment is authorized by these documents.

## Resolution of open research settings (13 November 2026)
This entry supersedes earlier "pending numerical defaults" status for research operation, not the user's financial preferences. Under the instruction to resolve remaining items, the agent selected and froze research-only screens and exact initial variants/splits in config/research-policy.json. Primary growth screens remain positive absolute growth, 2 annual percentage points above ETH and <=30% research drawdown; defensive outcomes are measured/reported separately without automatic promotion. The user has not selected a firm live limit, and no live activity is authorized.

The data audit selects a fixed limited BTC/ETH **EUR** historical route because the much shorter crypto/USDC data cannot support the evaluation. Use EUR commissions and actual USDC/EUR valuation, without inventing a cheap synthetic execution venue. Cross-sectional confirmation and six budget slots stay deferred, rather than filling them with today's survivors. This is a research route, not account funding or final exchange commitment.

Source-use scope remains a precise external clarification rather than an assumed vendor permission. The complete request is in the feasibility evidence report and was not sent. Public entry-tier fees are deliberately used for simulation; actual account entitlement is checked before funding, not requested prematurely.

Consolidated the working rules into METHODOLOGY.md and the plan into ROADMAP.md. Detailed historical reports/JSON moved to research/ and configurations to config/. Earlier standalone protocol, risk and execution documents were removed after integrating their active rules; prior versions remain in Git history.

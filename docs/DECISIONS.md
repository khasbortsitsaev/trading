# Decision log

As of 2026-11-12. Decisions may change with evidence.

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
| Fees | 0.25% baseline round trip, 0.15% low, 0.50% stress; provisional all-in estimates based on Bitvavo | Assumption |
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

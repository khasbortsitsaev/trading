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
- Broader user objective: relatively passive supplementary income from a side business. Small ongoing VM costs are acceptable in principle; live operation remains subject to separate authorization.
- BTC dependence is an early research hypothesis, not a validated trading signal.
- See [Income objective and BTC research notes](OBJECTIVE_AND_BTC.md) for proposed tests, economics and open questions.

- Cost provenance clarified by the user on 2026-11-12: the initial estimates were based on Bitvavo. They must not be described as exchange-independent or replaced by another venue's fees without an explicit comparison. The venue remains undecided.

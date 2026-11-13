# Project plan

## The six review items

| Item | Resolution and remaining boundary |
|---|---|
| 1. Exchange/data feasibility | Audited long EUR development history and USDC conversion coverage. Initial route is fixed BTC/ETH on Bitvavo EUR; USDC crypto history is too short for the same evaluation. Standalone research-data permission still needs vendor clarification; no raw redistribution is assumed. |
| 2. Realistic costs | Public commissions verified. Use venue/pair taker fees plus explicit friction/delay stress; no unverified discounts. Sampled books are not realized slippage calibration. Actual account fees are checked before funding. |
| 3. Success criteria | Research-only working defaults are frozen in config: positive growth, at least 2 annual percentage points above ETH, <=30% historical drawdown, and robustness/evidence gates. Defensive outcomes are reported separately; no live preference is presumed. |
| 4. Shorting | First batch is owned long/flat spot only. Any borrowed-short product is separately gated by financing/collateral/liquidation evidence and a user decision. |
| 5. Research protocol | Twelve exact initial variants within an 18-slot cap; four chronological folds, one champion, predeclared sensitivity and sealed holdout dates. No adaptive search after failures. |
| 6. Data/execution | Daily history audit and offline controls are implemented and tested. No missing-day fill invention, overdrawn cash/inventory or same-information-time fill. A full strategy runner is not yet implemented. |

The authoritative concise rules are in [METHODOLOGY.md](METHODOLOGY.md); exact parameters/variants/splits are in [research-policy.json](../config/research-policy.json). Detailed source reports and machine evidence are outside docs under [research](../research).

## Next work

1. Resolve the exact source-use clarification in the feasibility report before retaining a strategy research dataset. There is no need for trading keys or a funded account to build offline code.
2. Implement a deterministic, auditable strategy runner around the tested accounting/data primitives; preregister the first run. Reconcile initial ETH, quote cash and USDC reporting, with correct delayed fills and source-specific costs. Synthetic fixtures precede any strategy result.
3. Run only the frozen development batch on an admitted dataset. Preserve negative, invalid and inconclusive results. Do not open the holdout until champion selection, correctness and source access conditions pass.
4. If development and holdout pass, propose prospective paper validation. Only afterward consider a separate user decision on venue funding, exact live limits, monitoring, restart and stop procedures.

The broad strategy catalogue remains in scope for later justified batches. No ML, derivative, borrowed-short, autonomous scheduling or real-order system is needed for the first batch. No numerical live return or loss guarantee exists.

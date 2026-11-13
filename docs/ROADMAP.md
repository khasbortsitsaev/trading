# Project plan

## The six review items

| Item | Resolution and remaining boundary |
|---|---|
| 1. Exchange/data feasibility | Bitstamp BTC/USD and ETH/USD development data are now captured and quality-audited through supported public endpoints. Bitvavo USDC remains a separate cost candidate. Source/USDC execution-basis and volume/capacity limitations remain explicit; no EUR constraint. |
| 2. Realistic costs | Public commissions verified. Use venue/pair taker fees plus explicit friction/delay stress; no unverified discounts. Sampled books are not realized slippage calibration. Actual account fees are checked before funding. |
| 3. Success criteria | Research-only working defaults are frozen in config: positive growth, at least 2 annual percentage points above ETH, <=30% historical drawdown, and robustness/evidence gates. Defensive outcomes are reported separately; no live preference is presumed. |
| 4. Shorting | First batch is owned long/flat spot only. Any borrowed-short product is separately gated by financing/collateral/liquidation evidence and a user decision. |
| 5. Research protocol | Twelve exact initial variants within an 18-slot cap; four chronological folds, one champion, predeclared sensitivity and sealed holdout dates. No adaptive search after failures. |
| 6. Data/execution | Daily runner, collector and offline controls are implemented; 40 tests passed. Synthetic replay and the first development ledger reconcile. Fills remain delayed candle proxies, not exchange executions. |

The authoritative concise rules are in [METHODOLOGY.md](METHODOLOGY.md); exact parameters/variants/splits are in [research-policy.json](../config/research-policy.json). Detailed source reports and machine evidence are outside docs under [research](../research).

## Next work

1. Continue the already frozen development batch: eleven registered variants remain untested after the TREND-20 pilot failed the growth/drawdown screens. Do not change its parameters or invent a new search because the first result was negative.
2. Build/audit bounded comparison, uncertainty and robustness orchestration before declaring a champion. Retain continuous fold accounting, all failed results and actual evaluation counts. No holdout read while selecting candidates.
3. Address source-versus-USDC price/volume and executable-liquidity assumptions with permitted overlap evidence; no historical USD candle is claimed to be a Bitvavo fill. Keep current fee/friction/minimum scenarios explicit.
4. Only if development produces a passing frozen champion, evaluate the single declared holdout bundle, then consider prospective paper validation. Venue funding, exact live limits, monitoring and paid commitments remain separate later decisions.

The initial runner and source-audit milestone is complete. Its first historical pilot is USD-source proxy evidence, not an independent final or prospective profitability result. The broad strategy catalogue remains for later justified batches; no unbudgeted ML, derivative or borrowed-short expansion.

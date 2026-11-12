# Experiment registry

## Status
No experiments have been run as of 2026-11-12. No profitability findings are available.

## Recording rules
Create an entry before running an experiment. Preserve failed, negative, invalid and inconclusive outcomes. Separate software/accounting checks on synthetic data from economic evidence on historical or prospective market data. Never silently replace an earlier result after changing parameters or data.

## Entry template
- ID and date:
- Status: planned / running / complete / failed / invalid / inconclusive
- Evidence type: synthetic software check / historical replication / out-of-sample / paper traded / live
- Hypothesis and economic mechanism:
- Primary-source references and deviations from published rules:
- Predeclared success/failure criteria:
- Dataset source, version/hash, availability timestamps and quality exclusions:
- Venue, universe selection rule, symbols, timeframe and dates:
- Signal, allocation and execution timing:
- Parameters, random seed and number of variants/trials:
- Initial 0.5 ETH valuation, conversion, numeraire and benchmarks:
- Gross exposure, collateral, short/borrow assumptions:
- Costs: entry/exit commissions, spread, slippage, conversion and borrow/funding where applicable; identify all-in versus component accounting:
- Chronological splits, purging/embargo if needed, and final holdout policy:
- Git commit, environment/dependencies, exact command and configuration path:
- Result artifact paths and metrics, gross/net and benchmark-relative:
- Checks actually run and their outcomes:
- Limitations, failures and interpretation:
- Decision and next step:

For the final code-commit field, record the commit containing the code/configuration actually executed. Commit the resulting report separately so the run remains traceable.

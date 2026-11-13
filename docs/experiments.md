# Experiment registry

## Status
As of 2026-11-13, COST-001 completed a deterministic software/accounting audit and small public-book cost scenarios. No strategy backtest, economic experiment or profitability finding exists.

## Recording rules
Create an entry before running an experiment. Preserve failed, negative, invalid and inconclusive outcomes. Separate software/accounting checks on synthetic data from economic evidence on historical or prospective market data. Never silently replace an earlier result after changing parameters or data.

## Entry template
- ID and date:
- Status: planned / running / complete / failed / invalid / inconclusive
- Evidence type: synthetic software check / historical replication / out-of-sample / paper traded / live
- Hypothesis and economic mechanism:
- Primary-source references and deviations from published rules:
- Predeclared success/failure criteria and batch stopping decision:
- Feasibility/cost evidence and unresolved execution limitations:
- Trial budget, selection procedure and holdout access record:
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

## COST-001: deterministic cost-accounting audit
- Date: 2026-11-13.
- Status: complete.
- Evidence type: synthetic software/accounting check plus observed public-book feasibility samples; no strategy experiment or profitability test.
- Hypothesis: explicit per-side commissions and fee-reserved depth sweeps can quantify costs without inventing fills or double-counting spread.
- Plan: verify the quote-fee break-even identity against hand arithmetic; use a two-level synthetic book to check sweep cost, insufficient depth, fee reserve and quantity rounding; reject malformed/crossed books; then analyze the small captured public-book samples under the frozen current-tier model.
- Success criteria: numeric identities hold within Decimal arithmetic tolerance; insufficient data is reported, not extrapolated; model spends no more than its fee-inclusive quote budget; input hashes match. A zero-sample run must fail.
- Budget: one deterministic audit, no parameter search or holdout access. Public rounds are observations, not independent trials.
- Inputs: docs/cost-model.json; timestamped source metadata and response hashes in the cost source manifest; raw public responses outside git.
- Costs and scope: fully funded spot only; quote-denominated fee convention is synthetic and explicitly unconfirmed for actual fills; no financing or market orders submitted.
- Executed code/model/tests commit: `cb5b894542de4826f6aa69f62d9862d8cb977ba3`.
- Commands (repository root): `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; `PYTHONDONTWRITEBYTECODE=1 python3 scripts/analyze_costs.py --responses /tmp/cost-analysis --model docs/cost-model.json --output docs/cost-observations.json`.
- Outcomes: all six deterministic checks passed. First observed-book run processed 20 snapshots; after a third sampling round, rerun processed 30 snapshots and 90 size scenarios. None lacked displayed depth at the modeled sizes; every response hash matched. These are correlated observations, not independent strategy trials.
- Results: [COSTS.md](COSTS.md), [cost-observations.json](cost-observations.json), [cost-sources.json](cost-sources.json). Results recorded separately from the frozen executed code commit.
- Limitations: synthetic quote-fee convention; account rates/fee currency unverified; snapshots within minutes; no realized fills, historical execution calibration or maker-fill evidence. Raw responses remain outside git, so exact market replay requires those bodies. Point 1 permissions/coverage conditions remain open.
- Decision: reject a venue-independent 0.25% cost baseline; prioritize Bitvavo USDC for further research, then resolve point 3 criteria and remaining review gates. No investment-edge conclusion.

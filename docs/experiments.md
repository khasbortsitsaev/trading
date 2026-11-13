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
- Accepted protocol/policy version and commit, or explicit draft status:
- Variant IDs, neighboring-variant IDs, actual fits/evaluations and reused outputs:
- Exact split-manifest hash, information/label horizons, purge/gap policy:
- Holdout access event time, selected algorithm/configuration hashes and contamination disclosures:
- Data/execution contract version, availability-time assumptions and unresolved admission gates:
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
- Results: [COSTS.md](../research/reports/costs.md), [cost-observations.json](../research/artifacts/cost-observations.json), [cost-sources.json](../research/artifacts/cost-sources.json). Results recorded separately from the frozen executed code commit.
- Limitations: synthetic quote-fee convention; account rates/fee currency unverified; snapshots within minutes; no realized fills, historical execution calibration or maker-fill evidence. Raw responses remain outside git, so exact market replay requires those bodies. Point 1 permissions/coverage conditions remain open.
- Decision: reject a venue-independent 0.25% cost baseline; prioritize Bitvavo USDC for further research, then resolve point 3 criteria and remaining review gates. No investment-edge conclusion.

## READY-001: resolve readiness with executed acceptance checks
- Date: 2026-11-13. Status: complete at the stated synthetic/control and development-audit scope.
- Evidence: synthetic accounting/control checks and a development-history quality audit; no real-data strategy or profitability experiment.
- Plan: test owned-spot inventory and cash, quote/base fees, atomic rejection, multiple positions/rotation, minimums/precision, causal delayed references, missing/delisted prices, stale marks, holdout rejection and page overlaps. Audit fetched EUR and USDC daily coverage and FX without returns, signals or holdout retrieval.
- Preflight metadata already observed: crypto/USDC begins July 2024 and contains two missing early days; EUR history is longer. Download page-size and timestamp-boundary truncations were diagnosed and additional boundary pages fetched. Full quality/invariant checks follow the code freeze.
- Success: exact fixture arithmetic; no negative balances/unauthorized fills; invalid/stale/holdout inputs rejected; raw hashes verified; full missing-day counts exposed rather than filled. Gaps are reported failures of coverage, not suppressed.
- Executed source/tests/auditor commit: `c181e5cc1d97df35e93a80369b3f46b4d7168b91` (results recorded afterward).
- Commands from repository root: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_history.py --responses /tmp/readiness-resolution --output research/artifacts/readiness-history.json`.
- Outcomes: all 24 tests passed (18 new offline-control fixtures, six existing cost fixtures). Full EUR development audit found 2,143 rows each with zero missing days; USDC/EUR has zero missing days in the 2021-onward accounting period. Crypto/USDC failed the long-history requirement and has two early gap days; it was not padded or substituted.
- Artifacts: [readiness history](../research/artifacts/readiness-history.json), [source records](../research/artifacts/readiness-sources.json). No raw records in git; exact replay needs temporary captured bodies. No returns, strategy signals or final holdout candles were evaluated.
- Decision: candidate historical route is BTC/ETH EUR with EUR fees and actual FX marks. Synthetic/control implementation passes its current fixtures; a full runner is not built. Vendor confirmation of research-use scope remains an external prerequisite, not a passed test. No paper/live activity or profitability claim.

- READY-001 revalidation after consolidation and timestamp/trade-ID hardening: executed code `d7c933f397b33b0a3141c23258585cd49b80a8fe`. All 24 tests passed again; rerunning the history auditor and the relocated cost helper against the same temporary bodies reproduced the stored JSON artifacts exactly. [Validation record](../research/artifacts/readiness-validation.json). No strategy/holdout data were added. This rerun was justified by code/path changes, not an additional independent experiment.

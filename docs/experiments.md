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

## RUNNER-001: end-to-end synthetic runner and USD-source audit
- Date: 2026-11-13. Status: complete at the stated software/source-audit scope.
- Evidence: synthetic software check and development-only source-quality audit, not strategy-profitability evidence.
- Frozen implementation plan: separate completed-bar trend/reversal signals, fixed-universe allocation, prior-information target quantities, future-open proxy execution, quote-fee spot accounting and ETH/cash benchmarks. All price/quantity scenarios remain synthetic until a separately admitted data run.
- Synthetic inputs: deterministic artificial BTC/ETH candles, seed 20261113; one TREND-20 smoke run, 2021-01-01 through 2021-07-19, no tuning or strategy search on artificial returns.
- Acceptance: cash and inventory never negative, quote-fee budget respected after adverse moves, no input at/after holdout, no future-feature effects on earlier decisions, reproducible ledger, no invented fill on invalid data, correct initial ETH/cash accounting, exact single-side costs and sell-before-buy rotation. Synthetic returns must not be interpreted economically.
- USD source preflight: Bitstamp official public OHLC API; six bounded requests returned the expected counts for BTC/USD and ETH/USD, 2020-01-01 through 2025-11-12. No final holdout request. API docs establish 1,000-row limit and that end takes precedence over start. Full source/coverage/hash audit will run after the collector code is frozen.
- Source-use scope: private research via supported public API, no raw redistribution/data product. API page has a separate commercial-company licensing notice; no unrestricted commercial license is claimed or accepted. Terms page returned an interstitial, which is not treated as successful terms verification or bypassed. No paid commitment, account or key is needed for offline implementation/source QA.
- Executed source/initial tests: `b84ed9b67ada50c14c35e95bacccb7632f6bd5f3`. Initial 38 tests passed; after two additional collector-boundary fixtures, all 40 passed at `29405ff` (no strategy-calculation change).
- Commands: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_research.py --synthetic --variant TREND-20 --output /tmp/usd-research/synthetic-run.json --summary research/artifacts/synthetic-run-summary.json`; identical replay to a second private output; `PYTHONDONTWRITEBYTECODE=1 python3 scripts/fetch_usd_history.py --output-dir /workspace/research-data/bitstamp-usd-development-v1`.
- Outcomes: full synthetic ledger/metrics replayed identically. Collector verified both USD series have 2,143 unique valid daily candles and zero missing days. No final holdout retrieval. Dataset hash 5d1d450f98b2ba61c8b956b53a113f8b03f3a1a5fb1cd51b309cd83c611b26f0.
- Artifacts: [synthetic summary](../research/artifacts/synthetic-run-summary.json), [USD source audit](../research/artifacts/usd-source-audit.json), [source context](../research/artifacts/usd-source-context.json), [runner validation](../research/artifacts/runner-validation.json). Full artificial and source-derived ledgers stay outside Git; artificial data are regenerable from the frozen generator.
- Interpretation: software/source-QA readiness passed for this limited runner. It does not implement actual exchange fills, volume-dependent capacity, source/USDC basis calibration or the full selection/uncertainty orchestrator. No synthetic return is economic evidence.

## DEV-001: first development-only trend pipeline pilot
- Date: 2026-11-13. Status: complete; specification committed before results. Outcome: fails the initial working economic screen; not promoted.
- Evidence: historical USD-source proxy experiment, not Bitvavo replication, prospective OOS, paper trading or live performance.
- Hypothesis: frozen TREND-20, a transparent long/flat 20-day momentum rule, can be evaluated through the complete signal/allocation/execution/accounting/reporting pipeline. A negative or inconclusive economic result is valid; no retuning in this pilot.
- Variant budget: one of the twelve registered initial variants (one of the 18 total slots). No cross-sectional slots, alternative venues or parameter variants are substituted after results. This pilot is not champion selection.
- Data: Bitstamp public BTC/USD and ETH/USD daily OHLC, 2020-01-01 through 2025-11-12; 2,143 candles each, no missing days, valid OHLC/volume and recorded hashes. Normalized SHA-256: 5d1d450f98b2ba61c8b956b53a113f8b03f3a1a5fb1cd51b309cd83c611b26f0. Raw/normalized bodies remain outside git. Source volume is Bitstamp's; no OBV signal is used.
- Selection limitation: fixed BTC/ETH survivor-selected limited universe. No claim of broad-crypto generalization. USD/USDC price basis is not measured or assumed identical.
- Scored window: 2023-11-24 inclusive through 2025-11-13 exclusive, the four 180-day development folds stitched continuously. Fixed-rule TREND-20 has no fitted model; only past closes produce signals. Earlier data is warmup, not scored capital performance.
- Initial inventory: 0.5 ETH at the first scored source open; no forced strategy sell/rebuy. Benchmarks: original ETH holding and cash after its required initial sale. Same initial quote equity and dates. No EUR leg or final liquidation.
- Signal/weights: close[t]/close[t-20]-1 > 0; active assets target 1/N, inactive allocation remains cash. Quantities fixed from prior available closes and fee-reserved equity; filled against a designated future daily-open proxy after publication/computation delay. Sell reductions before buys; resize unaffordable buys down, skip below-minimum orders.
- Cost scenario: hypothetical current Bitvavo USDC-like execution on USD references, 0.05% per side and 15 bps total round-trip noncommission friction, adverse price/tick rounding and static minimums from config/runner.json. This is a prospective-cost proxy, not observed historical fees/fills or actual USDC P&L. Report actual USD ledger and ETH-equivalent wealth; do not claim measured USDC wealth.
- Outputs: total net growth, ETH/cash comparison, drawdown, turnover/fees, order/rejection counts and full deterministic ledger outside git. Public report stores aggregate research summary/provenance, not source candles or full source-derived fills.
- Economic screen: use frozen research gates for descriptive comparison, but do not declare a pass without remaining robustness, dependence-aware uncertainty and source/execution evidence. Missing controls yield inconclusive rather than invented confidence. Holdout stays sealed regardless of the result.
- Command: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_research.py --data-dir /workspace/research-data/bitstamp-usd-development-v1 --proxy-usd --variant TREND-20 --start 2023-11-24 --end-exclusive 2025-11-13 --output /workspace/research-data/dev-001-ledger.json --summary research/artifacts/dev-001-summary.json`.
- Executed source/configuration commit: `ce4219ae285fbbd7e142ff6e810fe724155af38a`. The result was not used to change the parameters, fees, windows or thresholds.
- Evidence label: historical **out-of-sample development** evaluation relative to the preregistered fixed rule, with no fitted parameters. The period is development/selection data, not a sealed final or prospective independent assessment.
- Net USD-source proxy growth: **62.3168%** (CAGR 27.8544%); original ETH holding: **65.5186%** (CAGR 29.1276%). Maximum drawdown: **44.8946%**, versus ETH **63.8043%**. Final ETH-equivalent wealth: approximately 0.49033 ETH versus holding 0.5 ETH. Cash benchmark includes its one required initial conversion.
- Ledger: 720 scored daily points, 425 modeled fills and 410 skipped targets for cash/rounding/minimums; these are not real exchange orders or rejections. Modeled strategy commissions: about USD 62.15; adverse price/tick cost: about USD 93.77. No EUR leg, borrowing or leverage.
- Verification: every daily equity and ETH benchmark mark reconciled to cash/inventory/source prices; all 425 fills passed causal timing checks. Fold results use the same continuing portfolio, not four resets. Report and result hashes are in [DEV-001 summary](../research/artifacts/dev-001-summary.json) and [validation](../research/artifacts/runner-validation.json). No independent rerun or new strategy trial was added by ledger checks.
- Decision: the rule underperforms ETH and exceeds the 30% working research drawdown screen. Reject promotion of this pilot; lower drawdown than ETH alone does not satisfy the primary growth screen. This does not establish that other predeclared rules work or fail. No retuning or holdout access.
- Limitations: fixed survivor-selected two-asset universe; historical USD-source/USDC-cost proxy, not actual USDC wealth or Bitvavo fills; current rule/minimum scenarios, not reconstructed historical venue rules; no full robustness or bootstrap result. Additional planned variants remain untested and must stay inside the existing frozen budget.

- Final data-admission hardening at `bfbf9f6`: the runner now binds source manifest bytes/provider/quote/completeness as well as normalized price bytes, preventing accidental USD-to-USDC relabeling. All 40 tests passed; the actual admitted manifest passed the same checks. No economic rerun, parameter change or additional strategy trial followed this metadata validation.

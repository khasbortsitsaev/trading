# Current project state

Updated: 2026-11-13.

## Confirmed status
Preliminary venue feasibility and spot-cost comparisons exist, along with a small standard-library cost calculator and six passing deterministic accounting tests. No strategy platform/backtest, validated edge, chosen execution venue or live authorization exists. COST-001 is software/accounting evidence only.

## Publication and continuity
The user requires completed work to be committed and pushed. Prior planning and feasibility work was published to GitHub main in `127c949625d06ec3cee1ff9c2b6e3a1900862b8a`; the standing workflow is recorded in AGENTS.md. Never describe local files or a cloud snapshot as GitHub publication. Personal eligibility/account information and raw exchange datasets remain outside git.

## Point 1: feasibility
[FEASIBILITY.md](FEASIBILITY.md) retains the primary-source venue/data comparison. Network access works. General register/catalogue evidence supports examining Bitvavo and Kraken; Coinbase remains a reserve due to current data-use restrictions. Data permissions, selected-history validation, historical universe coverage and actual account/product eligibility remain unresolved. See [feasibility-sources.json](feasibility-sources.json) and [feasibility-audit.json](feasibility-audit.json) for provenance and diagnosed pagination/count limitations.

## Point 2: cost analysis completed at preliminary scope
[COSTS.md](COSTS.md) verifies market-specific public commissions, distinguishes maker/taker and conversion markets, records observed book costs, and defines explicit stress and break-even methods. Current entry-tier taker commissions sum to about 0.10% round trip for Bitvavo crypto/USDC, 0.50% for Bitvavo crypto/EUR and 1.60% for Kraken regular spot. Kraken's rates were independently confirmed in its documented July 2026 tier change. These are not all-in costs or authenticated account rates.

Research recommendation: prioritize Bitvavo USDC for a low-cost baseline while retaining alternatives. No final exchange decision. Original 0.15%/0.25%/0.50% all-in cases remain legacy comparisons rather than universal calibration.

## Validation actually performed
Registered COST-001 before accounting checks. Executed calculator/model/tests from commit `cb5b894542de4826f6aa69f62d9862d8cb977ba3`. Six deterministic tests passed, including hand-calculated fee/sweep arithmetic, reserves/rounding, insufficient depth and invalid/zero-sample rejection. Thirty book snapshots in three rounds produced 90 frozen-book size scenarios; no observed depth insufficiency at those sizes. The first 20-snapshot run was repeated only after new input observations arrived. Forty-four response hashes were verified. Synthetic tests are replayable from git; exact snapshot replay needs temporary response bodies outside git.

No account credentials, private endpoints, orders, strategy searches or large historical downloads were used. Same-session samples do not calibrate future slippage or establish profitability. Funding/conversion, actual fee assets and rounding, dynamic tiers, data-use permissions and full-history audit remain conditions for future work. Documentation links, JSON consistency and diff formatting checked before publication.

## Next concrete task
Point 3: define predeclared economic acceptance/rejection criteria and a finite initial trial budget. Keep the capital-growth objective, 0.5 ETH allocation, fully funded spot first and provisional live-risk tolerance distinct. Complete shorting constraints, statistical protocol and data/execution specifications (points 4-6) before real-data strategy development. Any strategy experiment must be preregistered; paid commitments and live trading still require a separate decision.

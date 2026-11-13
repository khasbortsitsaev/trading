# Current project state

Updated: 2026-11-12.

## Confirmed status
Documentation/specifications only. No platform, dataset, independent backtest, validated edge, selected exchange or live authorization exists. No experiments have run. Paper and fee claims from the review remain pending primary-source verification.

## Completed this session
Recorded capital-growth objective, 0.5 ETH initial allocation, fully funded spot first, conditional future capital and the division of agent/user decisions in [DECISIONS.md](DECISIONS.md). Preserved borrowed shorts as a separately gated possibility. Recorded provisional drawdown tolerance without treating it as an approved limit. Personal eligibility information is kept outside this public repository.

Reordered [ROADMAP.md](ROADMAP.md) around all six original review priorities before real-data strategy development. Expanded [METHODOLOGY.md](METHODOLOGY.md) with feasibility evidence, calibrated and break-even costs, bounded research protocol, holdout handling, data/execution requirements and stopping rules. Updated README, objective notes and experiment template for consistency.

## Validation and limitations
Reviewed all existing documentation before editing. Documentation links and diff formatting checked after editing. No software tests, trading experiments, external fee verification or venue eligibility checks were performed in this session. The six review work products are specified, not completed.

## Point 1 investigation: access restored, preliminary comparison completed
Updated [FEASIBILITY.md](FEASIBILITY.md) using fresh public requests and official exchange/regulatory sources. ESMA register entries support general Belgium service scope for Bitvavo, Payward Europe Solutions and Coinbase Luxembourg; no individual account access was established. Kraken and Bitvavo remain primary research candidates, Coinbase a reserve because current market-data terms restrict the intended AI-assisted use. The recommendation is narrow scope, not final selection or approval to ingest a production dataset.

All three previously blocked market-data requests now returned HTTP 200. Runtime status confirmed current/enforced policy. No environment configuration was modified or published during the retry. [feasibility-sources.json](feasibility-sources.json) contains pinned SDK references and 62 HTTP observation records/hashes; raw responses remain outside git. [feasibility-audit.json](feasibility-audit.json) records small candle, pagination and order-book checks. No orders, account activity, large dataset download or strategy experiment occurred.

Important findings: Bitvavo served 2020 ETH/EUR candles with missing intervals; its two half-day pages matched a complete recent-day request. Kraken served 2020 trades but its old-since OHLC request returned recent data only; the response contained 721 records including the forming candle, differing from the documented 720 maximum. A strict-disjointness trade-page check failed because the cursor boundary repeated one trade ID; the raw outcome is preserved and the deduplication requirement diagnosed. Sample candle invariants passed. Six order-book snapshots were only same-session observations, not durable liquidity or fill evidence.

Unresolved: applicable data-use/publication permissions, full selected-history validation, repeated liquidity sampling, point-in-time universe and actual account/product availability. Official Kraken archives are documented and their checksum-list link is accessible; the large archives were not downloaded or verified. No raw exchange data or personal account information were placed in git.

## Open decisions
Numerical research acceptance criteria, finite trial budget, final venue/data route and firm live risk/stop rules. Strong research cannot guarantee live profitability. No paid commitments or exchange credentials are authorized or required for the initial desk research.

## Next concrete task
Prepare point 2's source-backed venue/pair/order-type cost sheet for Kraken and Bitvavo, verifying commissions, tier, spread/slippage and conversion assumptions. Carry forward the data-permission and ingestion conditions in FEASIBILITY.md; no real-data strategy search or final dataset approval yet. Apply the privately supplied venue exclusion. Complete the remaining review items before platform expansion.

# Venue and data feasibility: preliminary assessment

Research date: 2026-11-12. Scope: fully funded spot, initial 0.5 ETH. Evidence is **observed public API behavior**, **official documentation**, or **research judgment**, as identified below. No strategy backtest, account action, exchange selection or live authorization occurred.

## Recommendation and decision

**Proceed with a narrow research scope; retain Kraken and Bitvavo as primary candidates. Keep Coinbase Advanced as a reserve because its current data terms conflict with the intended AI-assisted workflow.** This is a research recommendation, not a final venue decision.

- **Kraken:** strongest documented historical-data route in this comparison: official trade/candle archives plus an independently observed old-trade API response. Its short OHLC REST window must not be mistaken for full history.
- **Bitvavo:** retain as the original cost-reference venue and a plausible spot route. Old ETH/EUR candles were retrieved successfully. EUR and USDC markets have different fee categories; compare total costs in point 2 rather than choosing on commission alone.
- **Coinbase Advanced:** live spot metadata is accessible, but the current market-data terms restrict AI-related use and external dissemination of derived research. Do not adopt it as the default dataset for this project without resolving that scope.

The preliminary comparison establishes plausible technical and jurisdictional routes, not a production-ready dataset. Complete data rights clarification, a full selected-dataset audit and repeated liquidity observations before approving real-data experiments. A broad historical cross-sectional universe is not yet feasible on the evidence collected; start with a predeclared limited-universe study if the subsequent gates pass, explicitly disclosing survivor and selection limitations.

## Access restored and evidence retained

After publication, the new runtime reported current observations and an enforced network policy. Fresh requests to all three previously blocked APIs returned HTTP 200. The earlier CONNECT 403 blocker is resolved. No environment draft or publication changes were made during this retry.

[feasibility-sources.json](feasibility-sources.json) retains the earlier pinned SDK sources and 62 timestamped HTTP observations, including response hashes, redirects, failures and successful replacements. [feasibility-audit.json](feasibility-audit.json) records the small data checks and their limitations. Raw responses remain temporary local material under `/tmp/feasibility-retry`, outside git; no redistribution rights are asserted. Hashes identify inspected versions but do not guarantee that a URL will return identical content later.

## 1. Jurisdiction and products

The [ESMA MiCA register page](https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica) linked the [CASP CSV inspected here](https://www.esma.europa.eu/sites/default/files/2024-12/CASPS.csv). The retrieved file contained 407 rows. The rows below had no populated authorization-end date. These are observed register entries, not a guarantee of financial safety, individual onboarding or every asset/product being available.

| Candidate/entity | Home authority and authorization-notification date in register | Belgium scope observed | Qualification |
|---|---|---|---|
| Bitvavo B.V. | Netherlands AFM; 26 June 2025 | `BE` in service countries; custody, platform operation and transfers | General jurisdictional basis supported; individual onboarding remains untested |
| Payward Europe Solutions Limited / Kraken | Ireland CBI; 25 June 2025 | `BE`; custody, exchange, execution and other listed services | Kraken's separate trading-platform entity must not be conflated with this client-services entity |
| Coinbase Luxembourg S.A. | Luxembourg CSSF; 20 June 2025 | `BE`; custody, exchange, execution and other listed services | Register evidence does not settle Advanced account/product access or data-use permission |

Kraken's [licensing/restrictions page](https://support.kraken.com/articles/where-is-kraken-licensed-or-regulated) explicitly includes Belgium in its EEA list and identifies the Irish entities. The register row for Payward Global Solutions Limited, the separate platform operator, listed `CY | IE`, not Belgium; do not claim all Kraken entities are passported identically. The legal/execution chain needs rechecking before opening or funding an account. Current EEA asset exclusions are material; an accessible global catalogue is insufficient.

Bitvavo's [country page](https://bitvavo.com/en/countries) lists Belgium and payment methods but directs Belgian readers to `bitvavo.be`. The `.be` root redirected to `bitvavo.com/nl`; its `/terms` redirected successfully to the Dutch terms. Appending `/en` produced 404s. [English terms](https://bitvavo.com/en/terms) describe the EEA scope and AFM license, but do not replace confirmation of the actual terms shown during Belgian onboarding. Do not assume payment-method listings guarantee a particular bank/account is accepted.

No personal account, KYC, tax, funding eligibility or stablecoin entitlement was tested. These are later account-level checks. The privately supplied venue exclusion was respected; no claim about that excluded venue's operating status was adopted.

## 2. Spot catalogue and order constraints

Observed at approximately 16:07 UTC on 12 November 2026:

- Bitvavo returned 437 catalogue entries. BTC/EUR, ETH/EUR, BTC/USDC and ETH/USDC were all marked `trading`.
- Kraken's four-pair request with `country_code=BE` returned all four, each marked `online`, with no API errors.
- Coinbase Advanced's public request with `product_type=SPOT&user_country_code=BE` returned 925 entries and metadata for all four seed markets. This is catalogue evidence, not independently verified account access; no further Coinbase price/history probes followed the terms review. USDC products exposed USD aliases, so do not presume independent USD/USDC order books.

[Bitvavo market-field documentation](https://docs.bitvavo.com/docs/rest-api/get-markets/) distinguishes base and quote minimums, tick size and quantity/notional decimals. Numeric snapshot below; re-fetch before using constraints in any implementation.

| Venue / pair | Minimum base amount | Minimum quote amount | Price tick | Quantity decimals |
|---|---:|---:|---:|---:|
| Bitvavo ETH/EUR | 0.00276562 ETH | 5 EUR | 0.010 EUR | 8 |
| Bitvavo ETH/USDC | 0.00247844 ETH | 5 USDC | 0.010 USDC | 8 |
| Bitvavo BTC/EUR | 0.00007662 BTC | 5 EUR | 1 EUR | 8 |
| Bitvavo BTC/USDC | 0.00006985 BTC | 5 USDC | 1 USDC | 8 |
| Kraken ETH/EUR | 0.002 ETH | 0.45 EUR | 0.01 EUR | 8 |
| Kraken ETH/USDC | 0.002 ETH | 0.5 USDC | 0.01 USDC | 8 |
| Kraken BTC/EUR | 0.00006 BTC | 0.45 EUR | 0.1 EUR | 8 |
| Kraken BTC/USDC | 0.00006 BTC | 0.5 USDC | 0.01 USDC | 8 |

Both applicable base/notional constraints, precision, fees and order mode must be respected. A small quote minimum alone does not establish the smallest executable order. At the first ETH/EUR book midpoints, 0.5 ETH was approximately EUR 914 before costs; a EUR 5 floor is about 0.55% of that illustrative endowment. This supports small spot experiments, not an arbitrary position-count cap. Initial ETH conversion, residual balances, EUR/USDC conversion and fees still require explicit accounting. This snapshot is not the start-date valuation for a future backtest.

Bitvavo returned fee category A for the EUR seed markets and B for USDC. **Point 2 must verify the actual schedule, tier and applicable market rules; no calibrated all-in cost was established here.** Kraken's returned fee arrays were empty, so they cannot substantiate zero fees.

## 3. Preliminary liquidity observations

Read-only 20-level ETH books were sampled for EUR and USDC on Bitvavo and Kraken at about 16:09 UTC, with a second EUR observation less than a minute later. All six books were uncrossed with positive displayed sizes. These are same-session indications, not independent sessions, historical spreads or fill tests.

| Initial book | Quoted spread, basis points | Displayed 20-level bid / ask notional, quote currency | Illustrative 0.5 ETH immediate sweep |
|---|---:|---:|---|
| Bitvavo ETH/EUR | 0.55 | 288,905 / 233,109 EUR | Within observed depth; buy used more than the best ask level |
| Bitvavo ETH/USDC | 5.15 | 68,878 / 99,580 USDC | Within best displayed levels |
| Kraken ETH/EUR | 3.67 | 298,059 / 206,239 EUR | Within best displayed levels |
| Kraken ETH/USDC | 1.48 | 145,438 / 108,568 USDC | Within best displayed levels |

Spread = `(best ask - best bid) / midpoint * 10,000`; displayed notional sums price times size over the returned levels. Sweep calculations consume displayed sizes only. They exclude fees, cancellation, latency and adverse selection and are not executable quotes or realized fills. Do not rank total costs from these four snapshots. Repeated sessions, market regimes and size-dependent execution checks belong in cost calibration. BTC depth, altcoin liquidity and a portfolio-wide liquidity screen were not validated.

## 4. Historical coverage and small data audit

### Bitvavo

[Official candle documentation](https://docs.bitvavo.com/docs/rest-api/get-candlestick-data/) allows up to 1,440 candles per call, start/end in milliseconds aligned to the interval, and states that no-trade intervals have no candle.

- ETH/EUR hourly request for 1 January 2020 returned 21 unique, hour-aligned candles covering 00:00 through 23:00 UTC, descending in time. Three hours were absent. This is consistent with the documented omission rule, but the cause of each missing hour was not independently verified; do not fill it with a fabricated trade.
- Request for 11 November 2026 returned all 24 hourly candles, descending, unique and aligned. Two separate 12-hour requests had no overlap and matched the full-day response exactly.
- A one-day request for 1 January 2018 returned an empty list. This does not establish an exact listing date or earliest retained observation.
- Observed candles passed positive-price, OHLC range and non-negative-volume checks. No continuous multi-year audit, alternate-pair audit, historical spread archive or delisted-market backfill was established.

### Kraken

[Official OHLC documentation](https://docs.kraken.com/api-reference/market-data/get-ohlc-data) says up to 720 most recent records and warns the last entry is the uncommitted current interval. A request with `since=2020-01-01` returned recent hourly data from 13 October to 12 November 2026, not 2020. **Observed count was 721, including the forming hour**, a count discrepancy against the stated 720 limit. Do not hard-code an exact response count; exclude forming candles by timestamp and verify boundaries.

A recent `since=2026-11-11` request returned 41 records through the current 16:00 UTC hour. Unique timestamps, hourly alignment, OHLC ranges and non-negative volumes passed; this is not 41 completed hours.

The [Trades endpoint](https://docs.kraken.com/api-reference/market-data/get-recent-trades) returned three ETH/EUR trades from 1 January 2020. Following its returned cursor produced three more rows with **one overlapping trade ID**, giving five distinct trades across six rows. The initial strict-disjointness audit failed. This is a diagnosed ingestion requirement: preserve raw pages and deduplicate by venue, pair and trade ID; do not advance or round timestamps blindly. Small successful retrievals do not prove complete multi-year tick history.

Official [trade archive documentation](https://support.kraken.com/articles/360047543791-downloadable-historical-market-data-time-and-sales-) describes all-pair history through 30 September 2026, multipart downloads and quarterly updates. The [OHLCVT archive page](https://support.kraken.com/articles/360047124832-downloadable-historical-ohlcvt-open-high-low-close-volume-trades-data) describes candle archives at 1, 5, 15, 60, 240, 720 and 1,440-minute intervals and excludes no-trade intervals. A linked 1,344-byte [part-checksum list](https://assets.kraken.com/marketing/institutions/Trades_Full_PARTS_SHA256SUMS.txt) was retrieved successfully. No large archive was downloaded or independently checked. Trade documentation describes 14 parts of approximately 2 GB, so full tick ingestion is deliberately deferred; prefer the required pair/timeframe and a verified candle archive if sufficient.

### Coinbase

[Official public-candle documentation](https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/public/get-public-product-candles) states a 350-bucket maximum. Historical retention, earliest dates, page boundaries and old/delisted retrieval were not tested because data-use suitability failed the initial workflow screen below. No assumption that Exchange API and Advanced Trade are interchangeable is justified.

## 5. Delistings and point-in-time eligibility

Kraken's [official XMR notice](https://support.kraken.com/articles/support-for-monero-xmr-in-europe), last updated 31 March 2025, states that EEA XMR trading/deposits ended on 31 October 2024 at 15:00 UTC, with later withdrawal/conversion steps. It demonstrates that a globally existing symbol or historical archive does not imply contemporaneous eligibility for an EEA strategy.

Reconstruct market availability using dated listing, migration and jurisdictional delisting events; preserve announcements and their effective times. The notice is an example, not a completed universe. Historical retrieval for delisted symbols, complete event coverage and a survivorship-free multi-asset panel remain unverified for all three candidates. Archive claims of “all pairs” alone do not settle these questions. Defer broad cross-sectional strategy claims until that panel is established.

## 6. Data-use and publication constraints

This is a practical source/terms screen, not a legal clearance or an assumption that public APIs imply open licensing.

| Candidate | Primary terms inspected | Consequence for research scope |
|---|---|---|
| Bitvavo | [Developer agreement](https://bitvavo.com/en/developer-agreement), sections 2-3: authorized use is tied to facilitating own/users' use of Bitvavo services; storage is limited to permitted purposes, and benchmarking/competitive uses are restricted | Own-service research may need clarification of intended use, caching and public reports. Do not treat the SDK's ISC license as a dataset license or publish raw data by default |
| Kraken | [EEA terms](https://www.kraken.com/legal/eea-terms), Intellectual Property: own-benefit/approved-purpose permission, third-party distribution and automated-extraction restrictions. Official archive pages expressly describe downloading data for code/spreadsheet use; [API overview](https://docs.kraken.com/exchange/guides/overview) expressly supports public market-data and algorithmic-trading workflows | There is a documented intended technical route, but clarify applicable API/archive permissions against the broad terms before persistent automated ingestion or publication. No unrestricted redistribution grant was established |
| Coinbase | [Market Data Terms of Use](https://www.coinbase.com/legal/market_data), retrieved version dated 7 August 2026: personal/research permission alongside explicit restrictions on AI-related use and dissemination of data and derived research outside the organization | Do not choose this as the default AI-assisted research dataset without explicit compatible permission or a separately licensed route. No further historical or order-book probes were performed after review |

No raw exchange data were added to git. This repository records the project assessment, source references and limited factual observations; it does not offer a redistributable market dataset or claim permission for future data products. Resolve applicable permissions before persistent data ingestion or distributing substantial datasets/derived reports. No venue was contacted and no paid data agreement was accepted. A separately licensed source can be investigated later, but its candles still would not establish fills at a different execution venue.

## Completion boundary and next work

**Preliminary point 1 decision: narrow scope and continue with Kraken/Bitvavo comparisons.** Network access is fixed; no user credentials or additional environment changes are needed for the next desk-research work. This comparison does not clear the final real-data gate.

Remaining conditions before selecting and ingesting an experiment dataset:

1. Resolve intended own-service research, automation, retention and publication permissions for the chosen source, with an explicit compatible permission path if current terms do not cover the intended use. No automatic support message or account creation is authorized.
2. Select a pair/timeframe and sample/validate its archive or complete bounded history, including gaps and forming candles. Preserve provenance, checksums and exclusions. Determine actual coverage before freezing evaluation dates.
3. Gather multiple-session liquidity evidence during point 2 and verify market-specific commissions and conversion costs. No final maker-fill assumptions or all-in cost estimate exists yet.
4. Confirm actual Belgian onboarding entity/product/pair availability before any funded account use. Treat public register/catalogue observations as general evidence only.
5. Keep historical universe reconstruction gated; do not substitute today's surviving coins for a point-in-time universe.

Update on 13 November 2026: the **point 2 cost comparison** is now recorded in [COSTS.md](COSTS.md), including current commissions, limited book observations and explicitly uncalibrated friction scenarios. Points 3-6 now have concrete specifications in [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md), [RISK_SCOPE.md](RISK_SCOPE.md) and [DATA_EXECUTION.md](DATA_EXECUTION.md); numerical criteria and implemented data/execution admission checks remain open. The synthetic strategy-accounting prototype remains subsequent work. Nothing in this assessment establishes an investment edge or authorizes live trading.

# Data and execution specification

Version 0.1, 13 November 2026. Covers original review **point 6**. This is an implementation contract and acceptance checklist, not a claim that a dataset, ingestion service or execution simulator has already passed it. Related documents: [feasibility](FEASIBILITY.md), [costs](COSTS.md), [research protocol](RESEARCH_PROTOCOL.md), [spot scope](RISK_SCOPE.md).

## Dataset admission and provenance

Before persistent ingestion or real-data experiments, create a versioned manifest outside raw-data checkout paths. Required fields:

| Group | Required contents |
|---|---|
| Identity | Dataset ID/version, source venue/provider, record types, raw instrument IDs, base/quote assets, asset/migration mappings and source versus proposed execution venue |
| Coverage | Requested and returned half-open UTC ranges, candle intervals, earliest/latest observed records, expected/observed counts and exclusions by instrument |
| Source and integrity | Official URLs/endpoints and parameters without credentials, retrieval time, raw object byte counts and SHA-256 hashes, archive/checksum source, collector code commit/version and transformation lineage |
| Rights | Applicable terms/version/retrieval date; separate status for access, storage, automated/AI-assisted research and redistribution; permitted storage location and retention policy. A missing decision is unresolved, not permission |
| Eligibility | Point-in-time market/jurisdiction availability events, listing/delisting notices, trading modes and timestamped rule changes; no personal account information in git |
| Quality | Duplicate/conflict/gap/out-of-order reports, page-boundary audit, forming-bar exclusions, observed versus assumed availability times and unresolved anomalies |
| Use | Proposed hypotheses/timeframe, limitations, frozen split-manifest hash and whether claims are restricted to a predeclared limited universe |

Raw data are immutable, separate from credentials and kept outside git unless redistribution is explicitly permitted. Derived normalization retains raw-file/record references. Use a new version for corrections; never silently replace a dataset used by a prior run. TLS, published checksums and rate limits remain enabled. A source license for its SDK is not a market-data license.

## Canonical records

All timestamps are UTC with explicit precision and unit; retain original precision where available. Document whether endpoints use milliseconds, seconds or a nanosecond cursor; never parse all integer timestamps as one unit. Price, quantity, fees and cash use exact decimal representations until statistical calculations. Missing values remain missing, not zero by default.

| Record | Minimum schema |
|---|---|
| Instrument/rules | Venue + immutable source instrument ID + base/quote identities; rule `effective_from`/`effective_to`, `known_at`, status, tick/quantity precision, base/notional minimums, fees and fee-asset convention with provenance |
| Trade | Venue/instrument, source trade ID, event timestamp, price, base quantity, optional aggressor metadata, received timestamp, source object/hash |
| Candle | Venue/instrument, interval start inclusive/end exclusive, open/high/low/close, base volume, optional quote volume/trade count, complete flag, availability time and whether observed or assumed, received time, quality flags and lineage |
| Book | Venue/instrument, snapshot event/receipt times, sequence/nonce if present, bid/ask price-size levels, source hash, sequence-gap/staleness flags; current depth is not historical depth |
| Feature | Feature/version, observation interval, publication/availability time, revision/vintage ID, source hash and transformation/fitting version |
| Lifecycle event | Listing, suspension, delisting, quote/product restriction or migration; announcement time, effective time, source and confidence/status |

Historical retrieval time is not the time information became available to a historical trader. If actual publication/availability latency is unknown, keep it unknown in raw/normalized data and use a clearly tagged conservative **model assumption** for simulation. Do not present an assumed bar-end timestamp as a measured publication timestamp. On-chain metrics require actual vintage/publication delays; revised present-day values cannot be used as if known in the past.

## Quality and completeness policy

1. Check source hash, schema, units, instrument identity, interval alignment, positive prices, `low <= open/close <= high`, nonnegative volumes and monotonic ordering. Normalize descending source rows explicitly. Reject conflicting duplicate records pending diagnosis; identical overlaps are deduplicated with provenance.
2. Deduplicate trades by venue + source instrument + trade ID. Kraken's observed cursor boundary repeated one trade ID; preserve both raw pages and retain one normalized trade. Do not deduplicate solely by timestamp: multiple legitimate trades may share it. Do not round the opaque pagination cursor to float.
3. Audit adjacent pages and a complete bounded reference window. Detect cursor nonprogress, boundary overlap/gaps and truncated responses. API HTTP 200 is not evidence of a valid body or complete history. Distinguish documented limits from observations; Kraken's OHLC probe returned 721 rows including a forming bar despite the stated 720 cap.
4. Exclude the forming interval based on timestamps/availability rather than dropping the last row by position. Use actual returned coverage, not requested dates, in experiment manifests. A request with an old `since` value may return only recent data.
5. A missing candle can mean no trades, source outage, omitted history or a delisting. Diagnose from permitted finer data/metadata when possible. Record an explicit gap; never manufacture a tradable candle or silently carry forward an execution price.
6. For portfolio marking, a last observed price may be carried as a **stale mark** with its age, not as a new tradable quote. Do not silently exclude those holding periods or report a falsely smooth return series. An unresolved stale mark during scoring prevents a passing result; provide bounds/scenarios or label inconclusive until resolved.
7. No automatic winsorization, hindsight exclusion of crashes, survivor selection or fixing suspicious prices to improve returns. Quarantine anomalies under a predeclared quality rule, report capital exposure during exclusions and rerun the registered sensitivity if correction is justified.
8. Observe rate/retry policy and do not fabricate a successful batch after partial downloads. Published archive checksums must pass before dependent results can be used. Record inaccessible archives and unavailable delisted data as limitations.

## Universe and admissible hypotheses

A fixed limited-universe study must preregister instruments and dates for an economic/feasibility reason before return inspection. It does not demonstrate an unbiased broad-crypto edge. Choosing today's BTC/ETH is an explicit limited/survivor-selected design, not a historical all-asset universe.

Dynamic selection requires reconstructable past listing status, jurisdictional eligibility, delistings, symbol migrations and lagged liquidity/history filters, all known by decision time. Define universe review frequency and any minimum-history/liquidity threshold in the experiment record before running. Preserve assets that later failed; never replace them with survivors. If the panel cannot be built, defer cross-sectional confirmation rather than relabeling a current-coin sample as point-in-time.

Data needs depend on the strategy claim:

| Claim | Required evidence and permitted limitation |
|---|---|
| Slow trend/reversal screening | Completed candles may support a delayed-fill cost scenario, not observed fills; sufficient continuous history and valuation/execution assumptions still required |
| Cross-sectional ranking | Contemporaneous multi-asset observations and past-only eligibility, including failed/delisted assets; correlated asset returns are not independent trials |
| Intrabar stops/targets | Trades/finer events capable of determining event order; candles alone require adverse ambiguity bounds and cannot support a precise fill claim |
| Maker/limit edge | Historical quotes/trades and a defensible queue/partial-fill model; a candle touching a limit price is insufficient |
| On-chain predictive feature | Timestamped vintage/publication availability and revisions; observation date alone is insufficient |

## Causal event ordering and execution baseline

The first strategy batch is daily, long/flat, fully funded spot. The **daily frequency and execution defaults are proposed operational research choices**, frozen in the experiment specification before real-data evaluation. No claim that any venue guarantees these fills is implied.

For every action, enforce `all input available_at <= decision_at < order_ready_at <= fill_event_at`. An independent timestamp/lineage audit must prove this; an extra day in an array index is not enough.

Baseline candle-only scenario:

- Use only completed daily candles available by the decision cutoff. Set a modeled publication/computation allowance of **5 minutes** after the final required candle boundary, tagged assumed. If observed latency is longer, use the longer value or reject that data assumption.
- Fill against a future candle's open reference only when that candle's **start is strictly after order_ready_at**. Thus a signal from the day ending at Tuesday 00:00 UTC is not filled at Tuesday's opening trade; the earliest daily-open reference is Wednesday 00:00 UTC. This full-bar buffer avoids assuming an opening trade at the signal boundary was available after computation.
- A candle open reference means the first observed trade in that future interval, not a guaranteed trade at its boundary. Record modeled execution granularity and uncertainty. No reference candle/no market availability means no modeled fill. A pending order is cancelled at the end of that designated fill interval, with no automatic later fill; a future signal creates a new decision.
- Apply taker commissions and the declared noncommission allowance adversely to buy/sell reference prices. The proposed baseline allowance is **15 bps round trip**, split 7.5 bps per side; stress at 30 and 50 bps. These allowances are scenarios, not calibrated execution distributions. A future quote/book model replaces the portion represented by observed spread/depth rather than adding the same spread twice.
- The mandatory extra-delay test moves the designated fill reference one further decision bar, keeping signals and policy otherwise frozen. Never retune lookbacks because the delayed result is worse.

If finer licensed observations are available, use the first eligible event at or after the declared ready time with explicit latency; that is a different registered execution model. Report both models consistently rather than choosing whichever produces more favorable P&L.

## Portfolio and order rules

Separate signal generation, target allocation, order generation, fills and accounting. At each event: update known market/rule state, mark inventory, settle eligible prior fills/fees, generate targets using past information, sell only available inventory, reserve cash/fees and submit modeled buys. An actual exchange's settlement availability must be modeled before treating proceeds as spendable.

Validate long-only weights, gross exposure no greater than equity, nonnegative holdings, available cash, lot/tick precision and both applicable minimum size/notional rules. Round quantities down. A below-minimum order is skipped with its reason and residual cash retained, not rounded up beyond budget. Conflicting open orders must reserve cash/inventory; a new target cancels the previous pending target before reusing its reserve. No fixed position count is imposed. Fees charged in a different asset must debit that asset; the small cost helper's quote-fee convention is not authenticated accounting evidence.

A source/execution venue mismatch must be explicitly labeled and evaluated; another venue's price does not create a fill on the proposed execution venue. Historical rule/fee gaps must be tagged assumptions or prospective-cost scenarios, not backfilled as measured history. Stablecoin/FX marking is separate from physical conversion. Initial and final conversions follow the actual portfolio path; starting with ETH does not require selling it if it is already the target holding.

Do not infer stop/target ordering from OHLC bars. For a later stop strategy, specify whether a trigger creates a market order, use the first eligible subsequent executable event, and evaluate adverse plausible paths if sequencing is unknown. A stop is not a guarantee of a maximum loss. These features are outside the first simple baseline unless separately registered.

For suspension/delisting, prohibit new orders once known restrictions apply. Follow known exit deadlines using modeled liquidity; do not grant a last-price cash liquidation after trading is unavailable. If the required exit cannot be valued or executed, report impairment/loss bounds and an inconclusive or failed feasibility outcome, including locked assets. Do not drop the asset's loss from the portfolio.

## Required implementation acceptance checks

Before real-data performance results, implement and execute deterministic fixtures for:

- Fee arithmetic and fee assets, partial fills, cash reserves, turnover, no leverage and no selling unowned inventory.
- Multiple concurrent positions, asset rotation, residual cash, minimums/precision and reservations for pending orders.
- Signal/feature availability, revision vintages, strict ready-to-fill ordering and delayed execution.
- Gaps, stale valuation, overlapping pages, multiple trades at one timestamp and conflicting duplicates.
- Trading suspension/delisting, unavailable exits and an adverse intrabar ambiguity case if stops are added.
- Initial 0.5 ETH valuation/conversion and ETH/cash benchmarks over exactly matching periods.
- Repeated execution from the same code/configuration/data hashes, producing the same ledger and reconciled equity.

Existing six cost-calculator tests cover only a small subset. None of the other controls is marked implemented or passed. Register the synthetic prototype plan in [experiments.md](experiments.md) before executing it. Store auditable order/fill/rejection records with signal time, input hashes, quantities, reference prices, applied costs and post-fill cash/positions, without secrets or personal identifiers.

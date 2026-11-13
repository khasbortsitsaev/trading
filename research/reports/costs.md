# Market-specific spot cost analysis

As of 13 November 2026. Scope: fully funded spot on the proposed Bitvavo/Kraken shortlist, with 0.5 ETH initial capital. No account fees, orders, realized fills, strategy backtests or profitability findings are claimed. Fees are **verified public schedule values**; book statistics are **observed samples**; execution scenarios and stress levels are **explicit model assumptions**.

## Finding and recommendation

**Prioritize Bitvavo crypto/USDC for the first cost-aware baseline, subject to the unresolved data/account feasibility conditions.** Its entry-tier commission is materially lower than Bitvavo crypto/EUR and the current Kraken Pro entry tier. Keep EUR and Kraken as explicit alternative-cost cases, not interchangeable venues. This is a research recommendation; the execution venue remains undecided.

The original 0.25% all-in round-trip assumption is plausible as a scenario for some Bitvavo USDC markets, but cannot serve as a universal baseline. It is below entry-tier Bitvavo EUR commission alone and far below the current Kraken entry-tier commission. The original 0.50% “stress” assumption only approximates Bitvavo EUR taker commissions before spread and slippage.

## 1. Verified commissions and applicable tiers

Primary sources retrieved on 13 November 2026:

- [Bitvavo fee schedule](https://bitvavo.com/en/fees): Category A crypto/EUR, B crypto/USDC, C stablecoin conversion including USDC/EUR. The public market catalogue returned matching categories for the seed pairs.
- [Kraken Pro schedule](https://www.kraken.com/pro/fees): regular spot versus stablecoin-base/FX schedules. The older [Kraken fee URL](https://www.kraken.com/features/fee-schedule) now describes app services and links to Pro; do not substitute app/Instant Buy pricing for exchange API trading.
- [Kraken cross-platform changes](https://support.kraken.com/articles/cross-platform-fee-tier-changes), updated 30 October 2026, states an effective change on **9 July 2026** and independently repeats the new spot rates below.

All percentages in this table are **per execution**, except the final three columns. The round-trip columns sum entry/exit commission percentages for comparable notionals; they are approximate, exclude execution friction and do not assert maker fills.

| Venue / actual market group | Entry tier | Maker | Taker | Maker/maker round trip | Maker/taker round trip | Taker/taker round trip |
|---|---|---:|---:|---:|---:|---:|
| Bitvavo BTC/EUR, ETH/EUR (A) | EUR 0 qualifying 30-day volume | 0.15% | 0.25% | 0.30% | 0.40% | 0.50% |
| Bitvavo BTC/USDC, ETH/USDC (B) | EUR 0 | 0.05% | 0.05% | 0.10% | 0.10% | 0.10% |
| Bitvavo USDC/EUR (C) | EUR 0 | 0.10% | 0.10% | 0.20% | 0.20% | 0.20% |
| Kraken BTC/EUR, ETH/EUR, BTC/USDC, ETH/USDC | Spot tier 1, USD 0 | 0.40% | 0.80% | 0.80% | 1.20% | 1.60% |
| Kraken USDC/EUR | Stablecoin-base/FX entry tier | 0.20% | 0.20% | 0.40% | 0.40% | 0.40% |

**Crypto quoted in USDC is not a stablecoin-base pair.** Do not assign Kraken's cheaper USDC/EUR schedule to ETH/USDC or BTC/USDC. The current Pro page exposed 634 discounted spot pairs in its embedded list; none of the four BTC/ETH seed pairs were present. No discount was applied. Promotions, negotiated rates and authenticated account entitlements remain unverified.

### Tier sensitivity and historical applicability

Kraken's regional support page describes qualification by the better of rolling spot volume and assets on platform. Global Pro documentation also discusses futures qualification; no futures activity or leverage is assumed for this project.

| Kraken regular spot tier | Qualifying 30-day spot volume OR assets | Maker / taker per execution | Approximate taker/taker commissions |
|---|---|---|---:|
| 1 | USD 0 / no asset qualification | 0.40% / 0.80% | 1.60% |
| 2 | USD 2,500 / no asset qualification | 0.30% / 0.60% | 1.20% |
| 3 | USD 10,000 OR USD 20,000 assets | 0.22% / 0.38% | 0.76% |
| 4 | USD 25,000 OR USD 50,000 assets | 0.20% / 0.35% | 0.70% |
| 5 | USD 50,000 OR USD 100,000 assets | 0.15% / 0.30% | 0.60% |

For Bitvavo, the next Category A threshold is EUR 100,000 qualifying 30-day volume, with 0.10% maker / 0.20% taker. Category B remains 0.05%/0.05% at that threshold. Do not assume such volume for this capital allocation or trade merely to earn a discount. On both venues the inspected documents exclude stablecoin/FX conversion volume from qualifying crypto volume. Ordinary crypto/USDC trades must not be confused with stablecoin conversion volume.

A future backtest must track rolling qualifying notional, FX conversion for tier valuation, the timing of tier changes and any effective-date rules. Do not retroactively apply the final tier to all past trades. Current-tier stress applied to historical prices estimates prospective economics; it is not a reconstruction of historical costs. The current calculation deliberately keeps the public entry tier fixed and does not claim the user's actual tier.

[Bitvavo account-fee documentation](https://docs.bitvavo.com/docs/rest-api/get-account-fees/) identifies the default Category A account endpoint; [market-fee documentation](https://docs.bitvavo.com/docs/rest-api/get-market-fees/) is needed for market-specific confirmation. Both require account authentication. No key was requested or private endpoint called. Empty fee arrays from Kraken public metadata do not mean zero fees.

## 2. Spread and size-dependent depth observations

Thirty public order-book snapshots were collected: three rounds for five markets at two venues, about **11:04:55, 11:05:46 and 11:08:30 Brussels time** on 13 November (10:04-10:08 UTC). Requests were not simultaneous; these cannot establish an executable cross-venue arbitrage. The prior day's small ETH samples remain in [FEASIBILITY.md](feasibility.md) and were not pooled with these different-depth observations.

The calculator treats 0.5 ETH marked at each venue's same-round ETH/quote midpoint as a hypothetical quote budget, then sizes at 10%, 50% and 100% of that budget. It reserves the taker fee, consumes displayed asks and rounds base quantity down before evaluating the corresponding sale against displayed bids. This is **90 frozen-book scenarios**, not 90 executed trades or independent observations. The initial liquidation of the actual ETH endowment is not included; see section 4.

| Venue / pair | Spread range, bps | Maximum extra buy+sell depth cost beyond best quotes, bps, 100% budget | Frozen-book taker round-trip loss, 100% budget | Gross proportional price rise needed to break even under that book model |
|---|---:|---:|---:|---:|
| bitvavo BTC-EUR | 0.16-0.16 | 0.000 | 0.5003-0.5003% | 0.5029-0.5029% |
| bitvavo BTC-USDC | 1.30-2.17 | 0.135 | 0.1129-0.1222% | 0.1131-0.1223% |
| bitvavo ETH-EUR | 0.06-0.74 | 0.041 | 0.4993-0.5061% | 0.5018-0.5087% |
| bitvavo ETH-USDC | 3.08-4.27 | 0.996 | 0.1380-0.1431% | 0.1381-0.1433% |
| bitvavo USDC-EUR | 1.11-1.11 | 0.000 | 0.2108-0.2108% | 0.2113-0.2113% |
| kraken BTC-EUR | 0.02-0.06 | 0.000 | 1.5875-1.5879% | 1.6131-1.6136% |
| kraken BTC-USDC | 0.42-0.80 | 0.004 | 1.5915-1.5951% | 1.6172-1.6210% |
| kraken ETH-EUR | 0.06-0.80 | 0.841 | 1.5940-1.5961% | 1.6198-1.6220% |
| kraken ETH-USDC | 0.05-2.16 | 0.000 | 1.5878-1.6086% | 1.6134-1.6349% |
| kraken USDC-EUR | 1.11-1.11 | 0.000 | 0.4102-0.4102% | 0.4119-0.4119% |

All 90 scenarios fit within the returned 50 levels. This verifies depth in those responses, not reliable capacity, historical liquidity or fills. Quantity and market minimums are documented in [FEASIBILITY.md](feasibility.md); the calculator enforces base precision and budgets, but does not implement every venue-specific minimum, partial-fill fee rounding or actual fee-asset rule. Do not submit its quantities as orders.

Definitions:

- Spread = `(best ask - best bid) / midpoint`, expressed in basis points; 1 bp = 0.01%.
- Additional depth cost is buy VWAP above best ask plus sell VWAP below best bid. Best-quote spread is separate from this number, but already included in the VWAP round-trip calculation.
- The modeled round-trip loss is the cash loss from buying and immediately selling the same rounded quantity against a frozen book, including the explicit fee convention below.
- The final column is a model hurdle, not a forecast: it assumes the future bid side shifts proportionally while other book conditions remain unchanged.

**Do not add spread again to VWAP-based fills.** The reported losses exclude latency, cancellations, hidden liquidity, queue position, adverse selection, changing depth, outages, initial/final asset conversion and fixed expenses. Three rounds within minutes are correlated and cannot calibrate a slippage tail or justify a confidence interval. Some quoted spreads differ from the previous day's examples; a favorable snapshot is not a stable cost assumption.

## 3. Fee accounting, makers and stress scenarios

The executable [model](../../config/cost-model.json) uses a clearly labeled **synthetic quote-currency fee convention**. For quantity `q`, buy VWAP `A`, sell VWAP `B`, and per-side rates `f_buy`, `f_sell`:

```
buy cash outlay = q * A * (1 + f_buy)
sell cash receipt = q * B * (1 - f_sell)
round-trip cash loss fraction = 1 - B * (1 - f_sell) / (A * (1 + f_buy))
gross price-return hurdle at equal execution reference = (1 + f_buy) / (1 - f_sell) - 1
```

Actual venues can charge fees in different assets and round by fills. Before an exchange-specific accounting implementation, confirm the fee asset, rounding and quote-budget semantics from actual permitted account evidence. The formulas here must not be mistaken for an authenticated venue accounting rule.

At equal execution prices, the exact quote-fee **gross-return hurdle** is approximately 0.10005% for Bitvavo USDC takers, 0.50125% for Bitvavo EUR takers and 1.61290% for Kraken tier-1 takers. These differ from both the simple summed commissions and the cash loss at unchanged prices; keep those quantities distinct.

A limit order is not automatically a maker order. Marketable limits pay taker fees; post-only orders can be cancelled or remain unfilled. [Bitvavo order documentation](https://docs.bitvavo.com/docs/rest-api/create-order/) and [Kraken maker/taker guidance](https://support.kraken.com/articles/360000526126-what-are-maker-and-taker-fees-) document this distinction. No private order endpoint was called. Use taker fills for a conservative initial baseline; maker cases require a separate fill/queue and adverse-selection model. Bitvavo's equal USDC maker/taker entry rates offer no commission incentive to assume favorable maker fills.

### Proposed sensitivity ladder, not measured execution quantiles

Approximate full round-trip cost = entry/exit commissions plus the **total noncommission friction allowance** below. The allowance represents spread, depth and execution uncertainty together. It replaces a guessed friction value; it is not an extra spread charge on top of simulated bid/ask fills.

| Taker regime | Commission only | +5 bps friction | +15 bps friction | +50 bps friction |
|---|---:|---:|---:|---:|
| Bitvavo crypto/USDC | 0.10% | 0.15% | 0.25% | 0.60% |
| Bitvavo crypto/EUR | 0.50% | 0.55% | 0.65% | 1.00% |
| Kraken regular spot tier 1 | 1.60% | 1.65% | 1.75% | 2.10% |

These are research scenarios, not calibrated low/median/tail costs or a guarantee of sufficient stress. Extend the ladder for illiquid assets, small fragmented fills, exceptional volatility or poor availability. Preserve the original 0.15%, 0.25%, 0.50% all-in cases as **legacy comparisons**, not universal low/base/stress labels. A strategy that only survives a frictionless commission floor is fragile.

## 4. Initial ETH, EUR/USDC conversion and funding

Reporting in USDC does not require every position or transaction to execute in USDC.

- Start with the actual 0.5 ETH inventory. If the first desired position is ETH, do not sell and rebuy it just to simplify the simulator. If the strategy needs quote cash or another asset, charge the actual required ETH sale and subsequent trade once. The ETH-hold benchmark need not incur a conversion it does not make.
- Within a USDC-quoted universe, sell asset A to USDC and buy asset B with USDC. This rotation has two executions; do not charge two additional abstract round trips on top of those fills. Cash holding creates no commission by itself.
- USDC/EUR is a distinct conversion market: entry-tier fees are 0.10% **per conversion** at Bitvavo and 0.20% at Kraken, plus the observed spread/depth and execution uncertainty. The table's USDC/EUR round-trip results contain two conversions, not one. Repeatedly returning to EUR can erode the USDC-market fee advantage.
- An EUR-book strategy reported in USDC can use timestamped FX valuation without physically converting every trade. Physical conversion, when actually required for funding, withdrawals or execution, must be modeled separately. USDC/USD deviations are not automatically zero.
- External transfer costs depend on where the initial ETH is held, the supported network and any actual deposit/withdrawal route. No account or wallet details were requested; no transfer fee is invented. Centralized spot fills do not each incur an Ethereum transaction fee.
- Bitvavo's inspected schedule lists SEPA deposits at zero platform fee and some card/wallet methods at 1%; eligibility and the final funding quote require confirmation. This is not a reason to assume the endowment must be sold externally and deposited as EUR. Kraken app Instant Buy and small-balance conversion pricing are separate from Pro order-book fees; do not silently route dust through them.
- Keep fixed hosting/data expenses and taxes outside execution friction, then show their effect on net economic results separately. For illustration only, EUR 5 monthly fixed expense on EUR 1,000 capital is 0.5% of capital per month; neither is an actual project expense or capital valuation.

## 5. Turnover and strategy break-even costs

With flat prices and no spread, 30 hypothetical full-capital round trips at unchanged entry-tier quote fees reduce cash by approximately:

| Fixed-fee illustrative scenario | Commission-only capital reduction |
|---|---:|
| Bitvavo crypto/USDC | 2.96% |
| Bitvavo crypto/EUR | 13.93% |
| Kraken regular spot tier 1 | 38.12% |

Calculation: `1 - ((1 - f) / (1 + f)) ** 30`. This is arithmetic, not a performance forecast; it assumes fixed fees, full turnover, reinvested remaining cash, no spread or edge. Kraken tier improvements can materially change the path; the fixed-tier example is deliberately not a tier-aware prediction. Partial allocations reduce fee drag; a favorable Sharpe or classification score cannot substitute for portfolio P&L after this turnover.

**No strategy's break-even cost can be reported yet because no strategy was tested.** For each future frozen candidate, rerun its accounting across a per-executed-notional cost grid, with frozen signals and declared allocation/sizing policy. Report both zero absolute net-growth and zero excess-growth thresholds versus ETH/cash, with units and uncertainty. If costs alter available cash, rounding or order feasibility, recompute those consequences; do not keep infeasible fills. Do not optimize strategy parameters or choose the best venue retrospectively to rescue an unfavorable result. Include initial conversion and fixed expenses in the economic decision while preserving their separate attribution.

## 6. Validation and reproducibility

The **COST-001** plan was registered before the accounting audit. Calculator, model and hand-calculated tests were frozen at code commit `cb5b894542de4826f6aa69f62d9862d8cb977ba3`; results were recorded afterward. Six deterministic tests passed, covering fee break-even identity, multi-level sweep arithmetic, insufficient depth, fee reserves/rounding, double-count prevention, malformed books and a zero-sample rejection. This validates the small calculator only, not an exchange integration or backtester.

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/analyze_costs.py --responses /tmp/cost-analysis --model config/cost-model.json --output research/artifacts/cost-observations.json
```

The second command needs the temporary raw responses used in this session. A fresh checkout alone can run the synthetic tests, but cannot replay the exact market observations without those response bodies. This is an explicit limitation, not a claim of a fully archived dataset. [cost-sources.json](../artifacts/cost-sources.json) stores 44 HTTP observation records and hashes, including a failed obsolete support URL; [cost-observations.json](../artifacts/cost-observations.json) stores limited derived scenario results, not raw books. All response hashes used by the calculator matched; 30 snapshots and 90 size scenarios were processed, none insufficient at the sampled sizes. No software dependency installation, credential, real order, paper trade or strategy performance trial occurred.

## Decision and remaining uncertainty

The preliminary cost comparison is complete enough to **reject a venue-independent 0.25% baseline** and prioritize Bitvavo USDC for research. Current public commissions are verified and pair-specific; maker fills, actual account fee currency, dynamic tiers and realized execution costs are not verified. No final exchange or live allocation decision is made.

Carry forward the data-use/account/coverage conditions in [FEASIBILITY.md](feasibility.md). Before interpreting backtest economics, collect permitted multi-session observations across volatility regimes and the actual universe, confirm applicable account/market fees and model initial/final conversions and minimum orders. Do not expand into ML to compensate for weak net returns.

Review continuation: [RESEARCH_PROTOCOL.md](../../docs/METHODOLOGY.md) specifies proposed point 3 criteria and point 5 trial/holdout controls; [RISK_SCOPE.md](../../docs/METHODOLOGY.md) formalizes point 4; [DATA_EXECUTION.md](../../docs/METHODOLOGY.md) specifies point 6. Numerical policy confirmation and implemented data/execution checks remain required before real-data strategy evaluation. Live limits remain separate.

## Subsequent route correction
The fuller development-history audit found crypto/USDC history too short for the frozen evaluation. The initial historical route is now BTC/ETH EUR with the appropriate higher EUR fees, while USDC remains the reporting numeraire through actual USDC/EUR marks. The cheaper USDC recommendation remains relevant to later properly scoped or prospective research; it must not be transplanted as the fee model for EUR historical fills. See the follow-up in [feasibility.md](feasibility.md).

## User correction: EUR is not a binding trading route
On 13 November 2026 the user explicitly clarified that research/execution should use USD/USDC or the cheapest suitable route, with EUR only for actual funding/cash-out if needed. The earlier EUR-route selection and specific Bitvavo-permission blocker in this historical report are superseded by docs/METHODOLOGY.md and config/research-policy.json version 0.3. Keep the audited observations as evidence; obtain suitable longer data elsewhere rather than requiring higher-fee EUR trades. External USD-source results still need source/volume/quote-basis disclosure and do not prove Bitvavo USDC fills.

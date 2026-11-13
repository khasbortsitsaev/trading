# Spot scope and the shorting decision

13 November 2026. Covers original review **point 4**. This records the agreed initial scope and a separate future borrowed-short gate; it does not authorize account access, orders or borrowing.

## Initial research scope: fully funded spot

- Trade owned inventory against available cash only. No negative asset balances, borrowing, margin accounts, perpetuals, futures, options, leveraged/inverse tokens or synthetic short exposure.
- Target weights in risky spot assets are nonnegative. Their sum must not exceed one after reserving required execution costs; cash is the residual. Multiple concurrent assets and dynamic universes remain supported, without a fixed position-count cap.
- Mark equity as cash plus owned inventory at the declared valuation policy. Check gross exposure and cash/inventory feasibility after fills, fees and rounding, not just at target generation. Cancel or resize unaffordable orders deterministically; never create negative cash through fee deductions.
- Rebalancing sells available holdings before buying replacements; do not spend unsettled or unavailable proceeds unless the venue behavior is verified. A sell that reduces a positive holding is not shorting.
- Keep cash when signals are negative. A long/flat version of a published long/short strategy is a distinct hypothesis; it cannot be called an exact replication of the original.
- No staking, lending, yield products or collateral reuse is assumed. Ordinary spot still has price, venue/custody, stablecoin, liquidity and operational risks; the absence of leverage does not eliminate drawdowns.

## Borrowed shorts: retained in principle, excluded from batch 1

The user is open in principle to investigating shorting that involves borrowing, while rejecting extra leverage risk. Those wishes cannot be translated automatically into an executable product. Shorting an asset that is not owned generally requires borrowing or an instrument outside fully funded spot. A 50% long / 50% short portfolio has 100% gross exposure but still carries borrow, recall, collateral and liquidation risk. A short's loss is not capped at its initial notional.

Before any later short-dependent experiment is presented as executable, prepare a separate product/venue assessment:

| Required evidence | What must be specified |
|---|---|
| Eligible product | Current official availability for the target jurisdiction/account class, actual borrowable asset and permitted order route; no assumption from a global symbol list |
| Financing | Borrow-rate history or explicit stress scenarios, accrual clock, rate resets, minimum charges and availability/locate failures |
| Collateral | Initial/maintenance requirements, eligible assets, haircuts, currency mismatch, segregation and collateral reuse |
| Liquidation/recall | Trigger rules, fees, gaps, forced covering and inability to roll or locate; loss beyond deposited collateral if applicable |
| Portfolio accounting | Separate sale proceeds, cash collateral, borrowed quantities, funding liability, equity and gross/net exposure; no counting locked collateral or short proceeds twice |
| Scenario evidence | Adverse jumps, illiquidity, correlated collateral falls, borrow-rate spikes, recall and withdrawal/venue failure; no guarantee of a hard loss cap |
| User decision | Explicit acceptance or rejection of residual borrowing/liquidation risk and the exact scope; existing willingness in principle is not authorization |

If the intended meaning is **no possibility of margin liquidation or borrowing liability**, conventional borrowed shorts are outside scope. Do not substitute derivatives or leveraged products to bypass that preference. Synthetic research may explain a mechanism but must be labeled non-executable until its actual product gate passes.

## Research drawdown versus live controls

The user discussed roughly 20-50% possible live tolerance but did not choose a firm limit. [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) proposes a separate 30% historical screening limit; it remains a proposal and cannot set the live limit by implication. Historical drawdown is not a forecast or maximum possible future loss.

Before any live proposal, define an exact high-water-mark drawdown threshold, an initial-capital loss threshold, monitoring frequency, data/valuation failure behavior, cancellation/flattening policy and conditions for restart. Any stop can be delayed by gaps, outages or unavailable markets. No live value or stop order is selected here, and no live trading is authorized.

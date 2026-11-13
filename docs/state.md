# Current state

Updated 13 November 2026.

## What changed
The six review items now have research working decisions, source evidence and executed offline checks, rather than only specifications. The concise plan is ROADMAP.md and the single methodology is METHODOLOGY.md. Detailed reports/artifacts moved to research/, configurations to config/; eight working documents remain in docs/. Completed work is committed and pushed to main, never confused with cloud snapshot publication.

## Verified outcomes
- Bitvavo BTC/EUR and ETH/EUR each have 2,143 valid daily development candles from 2020-01-01 through 2025-11-12, with no missing days after page/boundary reconciliation.
- USDC/EUR covers the accounting period from 2021-01-01 without missing days. Raw EUR prices before that are warmup; no missing FX was invented.
- Crypto/USDC only returned July 2024 onward in the audited windows and has two early gap days. It fails the long-history requirement. The initial historical research route is therefore EUR, with EUR fees, not discounted USDC fees applied to EUR data.
- Eighteen new offline accounting/data-control tests and the six prior cost tests all passed. They cover fee assets, multiple positions, cash/inventory, rounding/minimums, causal fills, missing/delisted/stale prices, page conflicts and holdout rejection. Source/tests commit: c181e5cc1d97df35e93a80369b3f46b4d7168b91. They are not a full backtester or exchange integration.
- No strategy returns/signals or final holdout data were evaluated. The development audit ends before 2025-11-13; the final assessment window is 2025-11-13 through 2026-11-12. Prior public spot snapshots remain disclosed in the evidence.

## Research choices now fixed
config/research-policy.json contains agent-selected research-only defaults under the instruction to resolve the open review. Twelve exact long/flat trend/reversal variants, fixed BTC/ETH universe, four chronological folds and one champion; six cross-sectional slots remain unused. Primary growth screens include positive net growth, 2 annual points above ETH and <=30% research drawdown. Defensive outcomes are reported separately, not silently promoted. These are not claims about the user's live preferences or guarantees of loss control. Borrowing/leverage remain outside scope.

## The actual external boundary
Bitvavo's official API terms tie retention/use to its own-service authorized-use scope; no explicit vendor confirmation covering standalone historical/AI-assisted research was found. A precise clarification request is prepared in research/reports/feasibility.md but was not sent because external messaging was not authorized. No agent can grant that permission. Coin Metrics was checked as an alternative: its archive license is CC BY-NC, not an unrestricted commercial-use substitute. No raw market data was published.

Conservative public entry-tier rates resolve simulated fee assumptions. Actual account eligibility/rates/fee currency are later funded-use checks, not a reason to request keys now. Slippage stress is modeled, not a claim of realized execution calibration. Real strategy evaluation remains gated by source-use clarification and a correctly implemented/reviewed runner.

## Next concrete action
Obtain the source-use clarification recorded in the feasibility report, while completing a deterministic synthetic strategy runner around the tested primitives. Preregister each run; retain failed and inconclusive results. Do not inspect holdout strategy results, accept paid commitments, contact a venue, borrow or trade live without the appropriate distinct authority. No alpha or profitability has been established.

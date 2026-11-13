# Current state

Updated 13 November 2026.

## Latest user correction
EUR is not a trading constraint. Research can use long USD/USDC history from a suitable source independently of execution. Choose low total-cost spot execution; Bitvavo crypto/USDC is the current fee-based candidate. EUR conversion is only modeled when actually needed for funding/final cash-out, not inserted into routine trades. Primary reporting remains USDC with ETH benchmarks.

This supersedes the earlier choice of EUR execution based solely on historical coverage, and the project-wide Bitvavo-permission blocker. No specific Bitvavo permission request or further user input blocks development. Select another suitable source as needed, using supported access methods and its applicable terms. No vendor has been contacted.

## Verified work retained
The historical EUR coverage audit, public commission comparison and small-book scenarios remain evidence, not a mandate for future execution. The offline accounting/data primitives passed 24 tests at d7c933f397b33b0a3141c23258585cd49b80a8fe. No strategy backtest, alpha, realized fill calibration or exchange integration is established. Historical artifacts remain under research/, not the working docs folder.

## Current policy
config/research-policy.json version 0.3 separates source quotes, execution candidate, reporting and EUR cash-out. Twelve exact first-batch trend/reversal variants and research-only working criteria remain defined; they do not set the user's live loss tolerance. Source data is not yet selected/admitted. Existing split dates are planned windows that need coverage/contamination validation for the selected source, not permission to inspect holdout results.

Long USD-source studies must disclose the source/execution mismatch, including volume provenance and USD/USDC price-basis risks. Do not apply one venue's fees while claiming another venue's observed fills. Shorting/leverage remain outside the initial fully funded spot scope.

## This correction's validation
Checked policy values, source/route separation, local document links and diff formatting. No accounting code changed, so the earlier tests were not unnecessarily rerun and no new test/market result is claimed. Changes are committed and pushed under the standing workflow.

## Next concrete task
Continue the deterministic strategy runner and select a suitable long USD/USDC historical source. Validate coverage, provenance and source-versus-execution limitations before registering a real-data run. No credentials, funded account or additional preference is needed now. Paid commitments, contacting others and all live trading remain separate decisions.

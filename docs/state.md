# Current state

Updated 13 November 2026.

## Completed milestone
A working offline daily research runner and bounded public USD-history collector now exist. The runner separates completed-bar signals, fixed-universe allocation, prior-information target quantities, delayed candle-proxy fills, fees/minimums, portfolio accounting and ETH/cash reporting. No live order or exchange-account integration exists. USD/USDC remain the research/trading direction; no EUR leg is imposed.

## Verified data and software
Bitstamp public BTC/USD and ETH/USD daily development data cover all 2,143 days from 2020-01-01 through 2025-11-12, with valid OHLC/nonnegative volumes, zero gaps and recorded hashes. Raw/normalized bodies live outside git at /workspace/research-data/bitstamp-usd-development-v1. Admission hash and public metadata are in config/research-policy.json and research/artifacts/usd-source-audit.json. The collector rejects holdout overlap before networking and will not store raw data inside the checkout.

Forty tests passed. The synthetic runner replayed the same entire ledger and metrics. All 720 scored daily points and all 425 modeled fills in the first development pilot reconciled and passed causal timing checks. Source code/tests were frozen before execution; results were committed separately. See experiments.md and research/artifacts/runner-validation.json for commands, hashes and source commits.

## First actual development result: DEV-001
The registered TREND-20 baseline was evaluated over 2023-11-24 through 2025-11-12, using 0.5 ETH and a continuously funded portfolio across four development windows. Net USD-source proxy growth: 62.3168%, versus ETH holding 65.5186%. Maximum drawdown: 44.8946%, versus ETH 63.8043%. Final ETH-equivalent strategy wealth was approximately 0.49033 ETH versus holding 0.5 ETH.

This fails the current working ETH-growth-margin and 30% drawdown screens. No parameter, fee or date tuning followed it; no champion was declared. One of twelve registered initial variants is now evaluated; eleven remain untested. A positive USD return is not evidence of an investable edge. This is historical development out-of-sample relative to a fixed preregistered rule, not sealed final/prospective evidence.

## Limitations that remain explicit
Bitstamp USD-source candles are not Bitvavo USDC executions. The model uses current hypothetical USDC-like fee/minimum settings and adverse friction, with no measured USD/USDC basis, historical depth or real fills. USD results are not labeled actual USDC wealth. Fixed BTC/ETH is a limited survivor-selected universe, not broad-crypto validation. The API page distinguishes commercial-company data licensing; no unrestricted commercial-data/redistribution license is claimed or accepted. No raw market dataset or full source-derived ledger is published, and the terms-page interstitial was not bypassed.

The final holdout remains 2025-11-13 through 2026-11-12, not fetched or evaluated. Actual account fees/product eligibility, live limits and prospective execution validation are later distinct requirements. No credentials or further preference is needed for the next offline research work.

## Next concrete task
Continue only the remaining predeclared development variants, with auditable comparison/robustness/uncertainty orchestration and retained negative results. Keep signals/selection away from holdout data. Do not expand parameters, add ML or select a favorable source/venue after seeing returns. No live trading, borrowing, vendor messages or paid commitments are authorized by these results.

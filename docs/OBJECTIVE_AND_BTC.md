# BTC dependence and side-income objective

Recorded 2026-11-12. These notes distinguish user goals from untested research proposals.

## User objective
The broader purpose is a side business producing relatively passive supplementary income. The user is open to a small recurring infrastructure cost and envisages eventual operation on a VM available 24/7. This is a possible future deployment, not authorization to deploy or trade live. Initial research capital remains 0.5 ETH.

Income target, future capital contributions, acceptable drawdown and maintenance time budget remain unspecified.

## BTC dependence: hypothesis to test
The user's observation is that other cryptocurrencies often move with Bitcoin. Treat BTC as a candidate market-context variable and risk benchmark, without assuming that every asset follows BTC or that BTC causes all common movement.

Distinguish contemporaneous correlation, sensitivity to BTC returns (beta), and predictive lead-lag relationships. Only a relationship observable before an executable trade can support a predictive trading rule. A common market move alone does not establish alpha.

Proposed early tests:
- Measure rolling return correlations, rolling BTC betas and explained return variance across assets and bull, bear, sideways and volatile periods. Use synchronized returns, not correlations of trending price levels.
- Test whether lagged BTC returns and volatility improve subsequent altcoin-return predictions over each asset's own-history baseline. Fit transformations and parameters using past data only.
- Compare strategies with and without BTC trend/volatility filters under chronological walk-forward evaluation and realistic costs.
- Add BTC hold as a diagnostic benchmark alongside the agreed ETH hold and USDC hold benchmarks. Assess market-adjusted performance as well as actual net P&L.
- Check whether apparent multi-asset diversification mostly concentrates common crypto-market exposure. Correlation and beta can vary across periods.
- Record all tested variants and account for multiple testing. Do not assume BTC-neutral positions are risk-free or compatible with the project's gross-exposure constraint.

Primary-source background, author-reported findings only:
- Che, Copestake, Furceri and Terracciano (2023), *The Crypto Cycle and US Monetary Policy*, IMF Working Paper 2023/163: a common factor explains approximately 80% of crypto price variation in their sample. This is not a claim that BTC explains 80% of each asset's future returns or proof of causation.
  https://www.imf.org/en/publications/wp/issues/2023/08/04/the-crypto-cycle-and-us-monetary-policy-534834
- Liu, Tsyvinski and Wu (2022), *Common Risk Factors in Cryptocurrency*, Journal of Finance, DOI 10.1111/jofi.13119: market, size and momentum factors capture cross-sectional expected returns in their study.
  https://www.nber.org/papers/w25882

No project replication or predictive edge has been established.

## Fit with a relatively passive income objective
An automated strategy could eventually reduce routine manual execution. Research, initial development, operational monitoring and periodic reassessment still require work. Cheap continuous hosting does not establish profitability or eliminate strategy decay, exchange/API failures or losses.

Proposed evaluation criteria, not yet agreed numerical thresholds:
- Net economic profit after execution, conversion, borrow/funding where relevant, infrastructure and data costs. Distinguish trading returns from fixed business costs and after-tax disposable income.
- Capital required for a meaningful income target; 0.5 ETH is an experimental endowment, not evidence of adequate income-generating scale.
- Drawdowns, loss periods and variability of potential withdrawals, rather than a promised monthly yield.
- Ongoing maintenance hours and frequency of urgent interventions.
- Incremental value over ETH/BTC holding and cash, assessed with risk and operational effort in view.

Illustration only: EUR 500/month is EUR 6,000/year. At a hypothetical 10% annual net return, it corresponds arithmetically to EUR 60,000 of capital before tax if that return excludes no further costs. This is not a forecast or sustainable-withdrawal estimate; returns can be negative and irregular.

If research succeeds, a later operational design should consider monitoring, alerts, reconciliation, recovery and stop controls. Continuous service availability does not require frequent trading. A simple strategy with low maintenance and modest turnover may fit the objective better, but this must be evaluated rather than assumed.

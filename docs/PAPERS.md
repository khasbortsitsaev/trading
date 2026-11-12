# Academic research catalogue (candidate reading list)

**Important:** This is a handover of papers discussed during exploratory conversations, **not a completed primary-source verification audit**. Before implementing a paper, verify authorship, DOI, peer-review status, exact parameter definitions, data coverage, backtest costs, and whether code/data are actually accessible. Do not treat any historical performance figure below as an independently reproduced result.

| Topic | Candidate paper / source | Research value / audit question |
|---|---|---|
| Technical trading rules | Deprez & Frömmel (2024), *Are Simple Technical Trading Rules Profitable in Bitcoin Markets?* https://doi.org/10.1016/j.iref.2024.05.003 | Large rule search, data snooping and OOS risk-adjusted vs absolute returns |
| Event-driven ML | Grądzki et al. (2025), *Financial Innovation* https://doi.org/10.1186/s40854-025-00866-w | CUSUM, triple barriers, long/short and fee/slippage assumptions |
| Trend ensemble | *Catching Crypto Trends: A Tactical Approach for Bitcoin and Altcoins* https://www.sfi.ch/en/publications/n-25-80-catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins | Donchian ensemble, dynamic universe, volatility sizing, possible leverage |
| On-chain signals | *On-Chain Data and Strategy in Cryptocurrency Markets* https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5848549 | Data sourcing, on-chain factors, stability filtering, clustering and risk parity |
| Copula arbitrage | Tadi & Witzany (2025), *Financial Innovation* https://doi.org/10.1186/s40854-024-00702-7 | Copula dependence, cointegration, futures/shorts, transaction assumptions |
| Cointegration / pairs | Lorette et al. (2026), *Quantitative Finance* https://doi.org/10.1080/14697688.2026.2653663 | Pair formation, OOS and costs; dataset reportedly available |
| Selected profitable pairs | Palazzi (2025), *Trading Games: Beating Passive Strategies in the Bullish Crypto Market* https://doi.org/10.1002/fut.70018 | 13/37 OOS-positive pairs reported; need full list and selection-bias check |
| Hourly reversal | Xue & Zhou (2026) https://doi.org/10.1016/j.jedc.2026.105416 | Predictability versus implementable net trading profits |
| Cost-aware ML | *Machine Learning-Based Bitcoin Trading Under Transaction Costs* https://arxiv.org/abs/2606.00060 | Predicted-return threshold relative to fees; preprint status |
| Crypto momentum | *Momentum in the Cryptocurrency Market: A Comprehensive Analysis under Realistic Assumptions* https://doi.org/10.1093/rapstu/raag011 | Time-series vs cross-sectional momentum and realistic constraints |
| Factor interactions | Mercik et al. (2025), *International Review of Financial Analysis* https://doi.org/10.1016/j.irfa.2024.103809 | Liquidity/risk/return factors, long-short constraints |
| Factor zoo | *Crypto Factor Zoo* https://doi.org/10.1016/j.irfa.2026.105137 | Factor redundancy and incremental predictive information |
| Dynamic predictability | *Predictability on the Move: The Cryptocurrency Cross-Section* https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7556359 | Time-varying signals, multiple-testing and regime effects |
| ICVP allocation | Lassance et al. https://doi.org/10.1287/opre.2021.2140 | Independent component risk allocation; validate original title and formulas |
| Overfitting | Bailey et al., *The Probability of Backtest Overfitting* https://doi.org/10.21314/JCF.2016.322 | Selection bias and model search |
| Validation | López de Prado, *Advances in Financial Machine Learning* | Purged/embargoed time-series CV |

### Historical author-reported claims discussed, pending audit
- Donchian ensemble: around 18% annualized return for selected diversified configurations, with paper-specific cost and leverage assumptions.
- Event-driven ML: positive after modeled fees, with slippage reportedly excluded.
- Palazzi selected LTC/DOGE example: 71% annualized, Sharpe 2.12, 14% drawdown; selected outcome is not an expected return.
- Copula pairs: best selected configuration 75.2% annualized, Sharpe 3.77; futures, capital and leverage assumptions are materially different from this project.
- Hourly reversals: evidence of predictability is not equivalent to positive net trade P&L.
- Some recent microstructure studies find predictive features but no net profits at retail execution costs.

These are **claims to verify**, not endorsement or a ranking. Keep negative and mixed papers in the catalogue.

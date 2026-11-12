# Strategy families in scope

All are research candidates, not validated profitable strategies.

| ID | Family | Plain-English hypothesis | Potential role |
|---|---|---|---|
| S1 | Trend following | Price trends persist long enough to exploit | Standalone alpha |
| S2 | Volume/technical signals | Price plus volume may reveal stronger moves | Signal or filter |
| S3 | Mean reversion | Extreme moves sometimes partially reverse | Standalone alpha |
| S4 | Cointegration/pairs | A stable relative-price relationship may revert after divergence | Relative-value alpha |
| S5 | Copula-based pairs | Nonlinear dependence may identify relative mispricing | Relative-value alpha |
| S6 | Event-driven ML | Triggering analysis on meaningful market events improves decisions | Event detection + prediction |
| S7 | Cost-aware forecasting ML | Only predictions large enough to exceed costs should trigger trades | Signal filtering |
| S8 | On-chain factors | Blockchain activity can add information beyond price | Signal/feature |
| S9 | Cross-sectional factors | Liquidity, volatility, momentum and risk characteristics help rank assets | Multi-asset signals |
| S10 | Regime selection / RL | Different market states favor different rules | Adaptive selection, exploratory |
| A1 | ICVP, risk parity, volatility targeting | Better dependence-aware sizing may improve portfolio outcomes | Allocation, not alpha |

Combinations are explicitly in scope: signal ensembles, ML filters for other signals, regime switching, and independent alpha sleeves allocated by ICVP/risk parity. Evaluate marginal value relative to simpler baselines, and account for extra turnover and overfitting.

**Deprioritized:** sub-minute market-making/microstructure scalping that requires professional latency or fee advantages.

## Comparison criteria
- Economic mechanism and complete trading decision rule
- Historical data and frequency, exchange, universe, tradability
- Long/short/borrow requirements and capital constraints
- Published net versus gross results and exact modeled costs
- Reproducibility of rules/code/data
- Out-of-sample design and multiple-testing corrections
- Performance under current, common, constrained assumptions

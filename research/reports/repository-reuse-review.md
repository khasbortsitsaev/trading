# Repository reuse review

Checked 13 November 2026. Quick primary-source review of public READMEs, documentation and selected source; no installation, dependency/security audit, engine parity test or economic replication. Recommendations are provisional. No claimed trading returns were reproduced or ranked.

## Fit with this project

We already have a small offline Python daily runner, Decimal spot accounting, initial 0.5 ETH inventory, ETH/cash benchmarks, delayed fills, cost scenarios and holdout/data-admission guards. The immediate missing work is bounded comparison, robustness and dependence-aware uncertainty orchestration. External frameworks can save engineering, but none reviewed establishes the full project protocol automatically. We should avoid rebuilding commodity infrastructure while retaining explicit ownership of the research policy and accounting checks.

| Repository | Reusable capability | Fit / limitation | Observed license |
|---|---|---|---|
| [freqtrade/freqtrade](https://github.com/freqtrade/freqtrade) | Python crypto framework: data tools, candle backtesting, strategy interfaces, reports, dry-run; lookahead and recursive-indicator analysis | Closest overall match. First framework to evaluate. Reconcile initial ETH, cash reservation, concurrent positions, position sizing, delayed fills, costs and benchmarks before using its results interchangeably with ours. Framework availability does not establish support for our eventual venue/pairs. | GPL-3.0 |
| [freqtrade/freqtrade-strategies](https://github.com/freqtrade/freqtrade-strategies) | Existing entry/exit implementations and indicator combinations | Best immediate source of inspectable strategy examples. Upstream calls these educational starting points. Existing optimized thresholds/ROI/stop rules are not evidence of transferable profitability. | GPL-3.0 |
| [ccxt/ccxt](https://github.com/ccxt/ccxt) | Unified Python market-data and exchange API interfaces | Prefer an adapter over bespoke exchange integrations when expanding providers. Not a backtester or a complete historical dataset; venue retention, delistings, pagination, timestamps and terms remain our responsibility. Current Bitstamp collector need not be replaced just to add a dependency. | MIT |
| [pmorissette/bt](https://github.com/pmorissette/bt) | Composable scheduling, asset selection, weighting and rebalancing; portfolio trees and comparison | Good allocation/research reference and possible secondary checker. Crypto precision, minimums, initial inventory and execution timing need a parity audit. Allocation components do not supply alpha. | MIT |
| [QuantConnect/Lean](https://github.com/QuantConnect/Lean) | Multi-asset engine, Python/C# algorithms, portfolio and brokerage infrastructure | Credible broader platform alternative. Larger runtime/integration commitment than our daily prototype needs. Open-source engine does not imply all datasets, brokerage integrations or hosted services are free or licensed for our use. | Apache-2.0 engine |
| [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | Rust/Python event-driven backtesting; multiple instruments/venues and richer market-data simulation | Revisit if realistic event/order simulation becomes a bottleneck. Considerable integration work for a daily spot study; detailed engines cannot replace missing historical quotes/books. | LGPL-3.0 |
| [polakowo/vectorbt](https://github.com/polakowo/vectorbt) | Fast array-oriented signal/portfolio research | Useful possible cross-check, but broad parameter sweeping conflicts with our finite trial budget unless bounded. Current upstream README specifies Apache 2.0 with Commons Clause, so do not assume unrestricted Apache licensing. Verify the exact selected release before reuse. | Apache 2.0 + Commons Clause |
| [kernc/backtesting.py](https://github.com/kernc/backtesting.py) | Simple single-instrument signal backtests and interactive reports | Useful educational/single-asset reference. Its official guide says multi-asset portfolio rebalancing/arbitrage is not really supported, making it a poor primary fit for our concurrent portfolio. | AGPL-3.0 |

Licenses are a screening observation, not a compatibility conclusion. Before copying/distributing code, pin a commit/release, check its actual license and file notices, preserve attribution, and assess resulting obligations for our public repository. No third-party source was copied in this review. Maintenance and install compatibility were not audited; popularity is not an acceptance criterion.

## Concrete algorithms and strategy reuse

- The Freqtrade strategy collection supplies complete signal examples. [SwingHighToSky.py](https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/SwingHighToSky.py) uses CCI and RSI entry/exit conditions and declares a 15-minute timeframe, ROI exits and a stop loss. It is a source-code example, not a recommended parameter set or a replicated result. Moving it to our daily data or taking only its entry rule would create a new hypothesis, not reproduce the original strategy.
- The [bt README](https://github.com/pmorissette/bt#readme) demonstrates scheduled equal-weight rebalancing and points to momentum and risk-allocation examples. These are reusable portfolio building blocks, with no assurance of beating ETH after costs.
- Freqtrade's [lookahead analysis](https://www.freqtrade.io/en/stable/lookahead-analysis/) and [recursive analysis](https://www.freqtrade.io/en/stable/recursive-analysis/) are particularly relevant validation tools: future-information leakage and indicator warmup can inflate backtests. A clean diagnostic is not proof of profitability or complete absence of bias.
- Our frozen trend/reversal rules are already short and implemented. Replacing those formulas alone saves little work. The larger potential savings are data adapters, reporting, comparison infrastructure and later paper-trading operations.

## Recommendation and bounded next step

Prioritize Freqtrade as the framework candidate, its strategy collection as a later hypothesis source, and CCXT when a second data provider is needed. Keep bt as an allocation reference. Do not commit to a full migration from a README comparison.

Before building more general infrastructure, perform one offline synthetic parity spike with a pinned Freqtrade release: identical candles and fixed signal events, owned initial ETH, cash benchmark conversion, fees/friction, precision/minimums, simultaneous positions, rotation and delayed fills. Compare actual transactions and ending cash/inventory with our hand-audited ledger; explicitly record unsupported semantics and adaptation cost. Use synthetic data only so this does not become another economic search. If the mismatch is expensive to bridge, keep our small ledger as the reference and reuse components selectively. No exchange credentials or order execution are needed.

The remaining eleven preregistered economic variants, selection budget and sealed final holdout remain unchanged. Repository discovery does not authorize testing dozens of community strategies or expanding the current batch. New strategy families belong to a separately registered later batch. No external strategy is promoted by this review.

## Primary sources

- Freqtrade [README](https://github.com/freqtrade/freqtrade), [strategy collection README](https://github.com/freqtrade/freqtrade-strategies/blob/main/README.md), [strategy collection license](https://github.com/freqtrade/freqtrade-strategies/blob/main/LICENSE), and the two official diagnostics linked above.
- CCXT [README](https://github.com/ccxt/ccxt) and [Python package metadata](https://github.com/ccxt/ccxt/blob/master/pyproject.toml).
- bt [README/license](https://github.com/pmorissette/bt).
- LEAN [README](https://github.com/QuantConnect/Lean) and [engine license](https://github.com/QuantConnect/Lean/blob/master/LICENSE).
- NautilusTrader [README](https://github.com/nautechsystems/nautilus_trader/blob/develop/README.md).
- vectorbt [README](https://github.com/polakowo/vectorbt/blob/master/README.md) and [current license](https://github.com/polakowo/vectorbt/blob/master/LICENSE.md).
- Backtesting.py [official quick-start guide](https://kernc.github.io/backtesting.py/doc/examples/Quick%20Start%20User%20Guide.html) and [license documentation](https://github.com/kernc/backtesting.py/blob/master/backtesting/__init__.py).

These links track mutable upstream branches. Pin exact versions and recheck source and license before implementation. No market-data, return, strategy trial or holdout inspection was performed.

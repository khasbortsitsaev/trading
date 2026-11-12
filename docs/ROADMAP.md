# Development roadmap

## Phase 1: research catalogue
Verify primary sources, DOI, peer-review status, rules, data, performance, fee assumptions and code availability. Keep all major strategy families in scope.

## Phase 2: reusable Python research platform
- Historical market data ingestion with provenance and quality checks
- Standardized signal/target-weight interfaces
- Multi-asset portfolio accounting, optional shorts and gross-exposure constraints
- Configurable cost model, first using documented placeholder scenarios
- Benchmarking against ETH hold and USDC hold
- Deterministic experiment registry and performance reports
- Automated unit tests for P&L, fees, fills and look-ahead safeguards

## Phase 3: experiments
Implement simple interpretable baselines, then representative published methods and combinations. Compare equal weight, volatility targeting, risk parity and ICVP where meaningful.

## Phase 4: validation
Nested chronological walk-forward, final untouched holdout, multiple-testing awareness, sensitivity to realistic execution costs and regime changes. Explicit research go/no-go decision.

## Phase 5: feasibility
Compare exchange-specific market volumes, spreads, API/data coverage, minimum trade sizes, short availability, funding/borrow costs, and account restrictions. Consider cross-exchange signal data versus execution venue.

## Phase 6: paper trading
Prospective, real-time forward validation of signals, fills, operational reliability, risk and costs.

## Phase 7: optional live trading
Only after explicit authorization, safety review, limited permissions, exposure limits, monitoring, circuit breakers and a clear stop procedure.

## Immediate first development task
Create the Python project scaffold and one minimal reproducible backtest with synthetic test data and one transparent momentum baseline. Validate fee arithmetic and benchmark reporting before loading large historical datasets. Do not add exchange credentials or live order placement.

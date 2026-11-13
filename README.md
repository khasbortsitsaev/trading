# Crypto Quant Research

A research project to test whether systematic crypto strategies can grow an initial **0.5 ETH** after realistic costs. No profitable strategy or live system has been established.

## The plan

Start with fully funded spot, no leverage, and simple trend/reversal baselines. Use auditable accounting, chronological validation and one protected final holdout. Record failures as carefully as successes. Report USDC, EUR and ETH-equivalent wealth against ETH holding and cash. No arbitrary position-count cap.

The six original review items are summarized in [the project plan](docs/ROADMAP.md). The [methodology](docs/METHODOLOGY.md) is the single source of research rules; [decisions](docs/DECISIONS.md) distinguishes agreed objectives from agent-selected working defaults. See [current state](docs/state.md) for actual results and the next task.

## What is actually verified

- Public venue/pair fee schedules and small-book cost scenarios, not realized trading costs.
- Development-only Bitvavo daily coverage: 2,143 BTC/EUR and ETH/EUR candles each, without missing days; USDC/EUR conversion data covers the chosen accounting period. Crypto/USDC history is shorter and is not substituted into a five-year test.
- Offline accounting, temporal/data guards and synthetic acceptance fixtures. These do not prove profitability and are not a full backtester.

Source evidence lives in [research/reports](research/reports/) and [research/artifacts](research/artifacts/), not in a growing set of working documents. Raw exchange data and credentials are not committed. Research-data permission remains a specific external clarification; account-specific fees/eligibility are confirmed before funded use. No vendor was contacted automatically.

## Run checks

Python 3.12; standard library only. From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The [cost helper](scripts/analyze_costs.py) and [history auditor](scripts/audit_history.py) consume local response bodies outside git. Their exact market observations cannot be replayed from hashes alone. All experiment plans/results are in [experiments](docs/experiments.md); source/code commits are recorded there.

## Durable context

[Agent rules](AGENTS.md), [strategy catalogue](docs/STRATEGIES.md), [candidate papers](docs/PAPERS.md) and [BTC/objective context](docs/OBJECTIVE_AND_BTC.md). Papers are hypotheses, not independently reproduced results. Paid commitments, new borrowing risk and all live trading require separate decisions. Completed project work is committed and pushed to GitHub.

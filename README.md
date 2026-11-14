# Trading research POC

Find a repeatable investment edge after costs. Phase 1 covers **S1 trend following, S2 volume/technical signals and S3 mean reversion**, one at a time. Finish S1 end to end first. Lower trading frequency is welcome if the evidence supports it.

**Objective:** repeatable trading profits after costs with acceptable risk. Existing ETH is simply available capital. Beating ETH is not required; holding/cash comparisons help explain risk and where returns come from.

**Current conclusion:** no validated trading edge. S3 produced a similar median return to a simple 50% crypto / 50% cash portfolio, with higher observed drawdown, and beat it in only 17 of 47 matched windows. Stop refining this unchanged baseline; review the POC before another mechanism-driven hypothesis. [Comparison and limitations](docs/STRATEGIES.md#fixed-passive-controls-s3-004).

- Results: [S1-001](research/artifacts/S1/s1-001-summary.json) · [S2-001](research/artifacts/S2/s2-001-summary.json) · [S3-001](research/artifacts/S3/s3-001-summary.json)
- [Current state and next step](docs/state.md)
- [Strategy logic, including when to sell](docs/STRATEGIES.md)
- **Editable assumptions:** [config/runner.json](config/runner.json) for starting inventory, per-side fee, round-trip friction, timing and market minimums. Decimal rates: `0.0005` = 0.05%, while `0.005` = 0.5%. `15` bps = 0.15% round-trip friction, added separately to commissions.
- [Research policy](config/research-policy.json) for signal lookbacks, validation screens and protected dates. [Methodology](docs/METHODOLOGY.md) explains the rules. Changes affect new runs; historical results remain tied to their original commit.
- [Decisions](docs/DECISIONS.md) and [experiment evidence](docs/experiments.md). Detailed source evidence stays under `research/`.

Capital is a configurable example, not a project limit. The anticipated live starting inventory is 0.5 ETH; value it using the experiment's actual starting price. A USDC amount used in discussion is illustrative, not a fixed exchange rate. Minimum orders and costs mean results need not scale perfectly.

Python 3.12, standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_research.py --synthetic --output /tmp/trading-synthetic.json
```

Reuse the current runner, accounting, collector and tests. Use the existing [reuse review](research/reports/repository-reuse-review.md), which identifies Freqtrade, CCXT and bt, before building additional infrastructure. Live execution requires separate authorization.

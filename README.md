# Trading research POC

Find a repeatable investment edge after costs. Phase 1 covers **S1 trend following, S2 volume/technical signals and S3 mean reversion**, one at a time. Finish S1 end to end first. Lower trading frequency is welcome if the evidence supports it.

**Current conclusion:** the offline pipeline works, but the first S1 development test underperformed ETH holding: +62.32% versus +65.52%, with 44.89% drawdown. S1 baseline review is closed without promotion; [buy/sell examples and cost findings](docs/STRATEGIES.md#s1-baseline-conclusion-do-not-promote). S2 entry/exit rules are specified; next is implementation and synthetic checks. No validated edge or live system exists.

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

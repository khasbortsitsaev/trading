# Current project state

Updated: 2026-11-12.

## Confirmed status
- The repository contains project specifications and research documentation only.
- No Python platform, dataset, independent backtest, validated edge or selected execution venue exists.
- Existing papers and historical performance claims remain candidates pending primary-source verification.
- Agent rules and session continuity are defined in [AGENTS.md](../AGENTS.md).
- Decisions remain in [DECISIONS.md](DECISIONS.md); research sources in [PAPERS.md](PAPERS.md), strategy hypotheses in [STRATEGIES.md](STRATEGIES.md), and validation/cost rules in [METHODOLOGY.md](METHODOLOGY.md).
- [experiments.md](experiments.md) is the experiment registry. No experiments have run.

## Completed in this setup
Inspected all existing project documentation. Preserved its constraints and added explicit session startup, handover and experiment-recording instructions. No strategy research or software implementation was performed.

## Validation
Documentation consistency reviewed against the existing README, decisions, methodology and roadmap. No software tests or trading experiments were run.

## Open questions
- Verified venue/pair-specific execution costs. Existing all-in scenarios are provisional.
- Data source, point-in-time universe and shorting feasibility.
- Income target, acceptable drawdown and ongoing maintenance budget.
- Numerical research go/no-go thresholds, to be specified before final evaluation.

These questions do not block a synthetic accounting prototype.

## Next concrete task
Follow the immediate development task in [ROADMAP.md](ROADMAP.md): create a minimal Python research scaffold, deterministic synthetic data, a transparent momentum baseline and ETH/cash benchmarks. Test P&L, fee arithmetic, exposure limits and signal-to-fill timing. Register the experiment plan before running it. Synthetic results validate software only.

Before economically interpreting any real-data strategy, audit its primary sources and replace provisional cost assumptions with documented venue-specific estimates.

## Handover
At the end of each session, replace stale status, record actual checks and failures, and specify the next concrete task. Keep historical experiment outcomes in the registry rather than overwriting them here.

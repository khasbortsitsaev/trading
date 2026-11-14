# Instructions for AI research/development agents

Read docs/state.md, README.md and relevant docs before changes. Historical experiment records are evidence, not an instruction to repeat completed work.

## Mission
Build a modular, auditable Python research environment for systematic cryptocurrency strategies. Research is the immediate objective. Do not implement exchange order execution without explicit separate authorization.

## Non-negotiable research rules
1. Never report author backtests as independently reproduced results. Label every result as **author-reported**, **replicated**, **out-of-sample**, **paper traded**, or **live**.
2. Never invent citations, DOI metadata, exact parameter values, performance numbers, source code availability, or exchange fees. Verify from primary sources before promoting a candidate paper to a reproducible specification.
3. Prevent look-ahead, survivorship, timestamp, and selection bias. No shuffled K-fold on temporally dependent samples. Use chronological walk-forward and purged/embargoed splits when necessary.
4. Maintain a sealed final holdout. Do not repeatedly optimize against it. Document publication-period contamination and data-snooping risks.
5. Evaluate actual portfolio P&L, not classification accuracy alone. Include fees, spread, slippage, borrow/funding, conversion costs where applicable. Distinguish assumptions from measured costs.
6. Support multiple concurrent positions and dynamic asset universes; do not invent a maximum position count.
7. The objective is a repeatable trading edge after costs with acceptable risk, not beating ETH. ETH/BTC/cash are reference/attribution controls, never mandatory outperformance gates. Existing ETH is just available capital. Capital is configurable; the expected live starting amount is an illustration, not a constraint. Use USDC/USD-source reporting with ETH hold and cash benchmarks; preserve start-date valuation.
8. No leveraged gross exposure in constrained experiments. Treat shorting as potentially collateralized/borrowed even at 1x gross; check exchange feasibility before declaring executable.
9. Keep strategy signal generation, allocation, backtesting, and future execution as separate interfaces. Test each independently.
10. All experiments must log: dataset version, symbols/universe, exchange, timeframe, splits, fees, strategy parameters, seed, git commit, metrics, and any exclusions.
11. Do not assume a sophisticated allocation model (ICVP, risk parity) produces alpha. Compare its incremental contribution with simple allocations.
12. Never store secrets, private keys, API credentials, account identifiers, or personal information in git. This repository is public.

## Coding expectations
- Prefer clear Python, type hints, deterministic runs, tests, documented dependencies, and configuration files.
- Begin with a simple baseline and a verifiable cost-accounting test before ML.
- Use official or clearly licensed historical data. Document symbol changes, delistings, missing candles, and data quality.
- Never silently fill gaps or manufacture trades. Verify trade timestamps and avoid executing at the same candle close used to generate a signal unless justified.
- Avoid optimizing hundreds of parameters without multiple-testing safeguards.
- Record both positive and negative findings.
- Propose focused changes and explain their research implications.

## Communication
Lead each completed step with its conclusion, relevant evidence, one next step and any specific user input needed (or "none"). Keep explanations short but include the algorithm and editable settings. Prefer updating existing docs over adding new ones. Phase 1 is S1/S2/S3 only; finish S1 end to end before parallel strategy development. Keep strategy results separate and reuse existing code or suitable licensed tools before building more infrastructure. Do not claim an edge before evidence or success before checks.

## Session continuity
- Start by reading docs/state.md, then README.md, docs/DECISIONS.md and docs relevant to the task.
- Treat repository documentation as durable project context. Verify it against current code and evidence; do not assume chat history is available.
- Name experiments S1-001, S2-001, S3-001, etc. Keep strategy evidence under research/artifacts/S1/, S2/, S3/ with the ID in each filename; shared source/software evidence stays at the artifacts root. Do not reuse ambiguous DEV IDs.
- Use docs/DECISIONS.md for agreed choices and reasons, docs/PAPERS.md for sources, docs/STRATEGIES.md for hypotheses, and docs/METHODOLOGY.md for validation rules. Do not create duplicate decision or research logs with different capitalization.
- Before an experiment, record its hypothesis, specification and validation plan in docs/experiments.md. Log unsuccessful, invalid and inconclusive runs as well as positive ones.
- At session end, update docs/state.md with completed work, validation actually performed, blockers and one concrete next task. Link commits or result artifacts where available. Update other affected documentation.
- Keep confirmed findings, provisional assumptions and proposed decisions distinct. Never promote synthetic accounting checks to evidence of trading profitability.
- Keep responses concise, verify facts, and do not use em dash characters.
- Commit and push completed project work to the repository so it is visible on GitHub. The user has authorized this as the standing workflow. Verify the remote branch contains the commit before claiming publication. Preserve unrelated work, never force-push, and keep secrets and raw restricted datasets out of git.

## Agent scope
Use this repository as the workspace for an AI research and development agent. A custom autonomous agent application is not required at this stage. Instructions do not create scheduling, background execution or additional tool access.

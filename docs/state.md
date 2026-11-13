# Handover: resume here

**Paused on 13 November 2026 to conserve AI credits.** No background work is scheduled. This file is the single entry point for the next session; it contains the stopping point, decisions and next action. Do not restart the project or repeat the completed feasibility work.

## Goal and user instructions

Research whether systematic crypto strategies can grow **0.5 ETH after costs**. The objective is capital growth, not regular withdrawals. No validated edge, passive-income claim, paper-trading system or live authorization exists.

- Start with fully funded long/flat spot. No leverage or borrowed shorts in the initial batch. Borrowed shorts are only a possible later, separately evaluated decision.
- **EUR is not a trading constraint.** Use suitable USD/USDC research data and the cheapest suitable execution route. EUR conversion belongs only to actual funding/cash-out when needed.
- Data source and execution venue can differ. Bitstamp supplies current research prices; Bitvavo USDC is a low-fee execution candidate, not a final venue choice. Do not label external USD prices as actual Bitvavo/USDC fills.
- Keep the broad strategy catalogue. The first fixed BTC/ETH study is deliberately limited, with survivor/selection limitations; do not impose a permanent asset/position-count cap.
- The agent handles implementation/research; the user makes consequential decisions. No new preference, API key or funded account is needed to continue offline research. Do not revive the earlier project-wide Bitvavo-permission blocker; use suitable supported sources and respect their terms.
- **Commit and push completed work to GitHub `main`, then verify the remote.** Local files and cloud snapshots are not GitHub publication. Keep docs concise; do not add another handover or duplicate decision log.
- No live orders, leverage, vendor messages, paid commitments or deployments without separate authority.

## What is implemented and verified

Repository: `/workspace/trading`; remote: `khasbortsitsaev/trading`. Published implementation/results checkpoint before this handover: **`2b0bdf8ec8587cec1874c5fcecb38d828ccc4013`**.

Python 3.12, standard library only. **40 tests passed**; the complete synthetic run replayed identically.

| Component | Location / capability |
|---|---|
| Spot accounting/data primitives | `src/trading_research/core.py`: cash/inventory, fees, minimums/precision, timing, stale/gapped data and holdout guards |
| Daily backtest runner | `src/trading_research/engine.py`: trend/reversal signals, equal-universe allocation, delayed target quantities, adverse candle-open fill proxies, fees and ETH/cash reports |
| USD collector/loader | `src/trading_research/data.py`, `scripts/fetch_usd_history.py`: bounded official API requests, OHLC/coverage/hash checks and provider/quote identity binding |
| Run entry point | `scripts/run_research.py`: synthetic or specifically admitted development data; explicit `--proxy-usd` acknowledgement for USD-source experiments |
| Frozen settings | `config/research-policy.json` (version 0.4), `config/runner.json`; current fee evidence also in `config/cost-model.json` |
| Tests | `tests/`: future-price perturbation, delayed fills, affordability, fees, multiple positions, source corruption, raw-data storage and pre-network holdout rejection |

This is a working **offline screening runner**, not an exchange integration or a finished comparison/robustness/uncertainty orchestrator. Candle fills and current venue-like rules are assumptions, not measured historical executions.

## Admitted dataset and recovery

**Source:** official Bitstamp public daily BTC/USD and ETH/USD OHLC API. Each series has **2,143 valid, gap-free daily candles**, from **2020-01-01 through 2025-11-12**. Only development data was fetched.

Local files outside Git:

- `/workspace/research-data/bitstamp-usd-development-v1/manifest.json`
- `/workspace/research-data/bitstamp-usd-development-v1/normalized.json`
- Original captured responses in that directory.
- Full first-pilot ledger: `/workspace/research-data/dev-001-ledger.json`.

Admission hashes are in `config/research-policy.json`. Public provenance/quality is in `research/artifacts/usd-source-audit.json` and `usd-source-context.json`. Raw source records/full source-derived ledgers are not committed. Source API access is for private research; no unrestricted commercial-data or redistribution license is claimed.

**On resume, check whether these files survived before downloading anything.** If missing, use the collector command below, without expanding its dates. Compare normalized data against the admitted hash. A new capture changes retrieval metadata, so the manifest-byte hash can differ even with identical prices: review/version that metadata explicitly rather than silently bypassing admission checks. If prices changed, preserve the old result and record a new dataset version; do not present a rerun as independent evidence. Hashes alone cannot restore missing raw bodies.

## Exact stopping point: first historical pilot completed

**DEV-001**, preregistered **TREND-20** on the fixed BTC/ETH universe, was evaluated over **2023-11-24 inclusive to 2025-11-13 exclusive**. Four 180-day development windows used one continuing portfolio, not four fresh capital resets. Initial inventory was 0.5 ETH.

Cost scenario: 0.05% per execution, 15 bps total round-trip noncommission friction, static candidate minimums/ticks and delayed daily-open proxies. It is **USD-source historical development evidence under hypothetical USDC-like execution costs**, not actual USDC wealth, Bitvavo replication, final holdout performance or prospective evidence.

| Metric | TREND-20 | ETH holding |
|---|---:|---:|
| Total growth | +62.32% | +65.52% |
| CAGR | 27.85% | 29.13% |
| Maximum drawdown | 44.89% | 63.80% |
| Final ETH-equivalent wealth | approximately 0.49033 ETH | 0.5 ETH |

**Outcome: failed the current working growth/drawdown screens; no candidate was promoted.** Positive USD growth alone is not an investment edge. No parameters, costs or dates were changed after seeing this result.

All 720 daily equity points and 425 modeled fills reconciled. There were 410 skipped targets due to cash/rounding/minimums, not real exchange rejections. See:

- [Experiment registry](experiments.md): plans, actual commands, source commits, results and limitations.
- [DEV-001 summary](../research/artifacts/dev-001-summary.json).
- [Validation record](../research/artifacts/runner-validation.json).

The evaluated code/configuration commit was **`ce4219ae285fbbd7e142ff6e810fe724155af38a`**. Later source-admission metadata hardening passed the tests without rerunning or changing the economic result.

## Frozen research rules to preserve

These are agent-selected **research working defaults**, not the user's agreed live risk preferences:

- Positive net growth, at least **2 annual percentage points above ETH**, no more than **30% historical drawdown**, plus consistency, cost, parameter-stability and evidence gates. The user has not chosen a firm live loss limit.
- Twelve exact initial variants are already specified in `config/research-policy.json`: trend lookbacks **20, 40, 60, 120, 240, 365**; reversal lookbacks **5, 10, 20** crossed with entry z-scores **1 and 2**.
- **One evaluated; eleven untested.** Do not count TREND-20 again as a fresh hypothesis. Total selection budget is 18; six cross-sectional slots remain disabled, not reassigned, because there is no defensible historical universe panel.
- Neighbors, costs, allocation, folds and uncertainty settings are preregistered. Do not tune them because the first pilot failed. Report defensive lower-growth outcomes separately, without silently changing the objective.
- **Final holdout: 2025-11-13 inclusive through 2026-11-13 exclusive. It has not been fetched or evaluated.** Do not advance these dates with the calendar, download it during routine collection, or inspect it while selecting candidates. Earlier public price awareness is disclosed; do not claim the historical period was unknown to the world.
- Freeze one champion and its evaluation bundle before any holdout access. Failed results stay in the registry. No ML/ensemble expansion to rescue a negative baseline.

## Next concrete task

**Implement and audit the bounded development-batch comparison/robustness/uncertainty orchestration, then evaluate only the remaining eleven preregistered variants.**

Start with `AGENTS.md`, this handover, the policy and `docs/experiments.md`. Verify the checkout/data and run the tests in the resumed environment. Preregister the next run and commit executable changes/configuration before running it; commit reports afterward. Retain continuous fold accounting, all variant results and actual evaluation counts. No holdout read or unbudgeted search. Source/USDC execution-basis and liquidity calibration remain limitations, not reasons to force EUR trading.

Use [METHODOLOGY.md](METHODOLOGY.md) for detailed rules and [DECISIONS.md](DECISIONS.md) for settled choices. Existing reports are under `research/`; do not produce another stack of planning documents. The user wants progress with minimal repeated discussion and credit use.

## Useful commands

From `/workspace/trading`:

```sh
# Existing checks; no package installation required.
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v

# Independent synthetic smoke run; no market-data access.
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_research.py --synthetic --output /tmp/trading-synthetic.json

# Only if the admitted local data is missing: development-only source recovery.
PYTHONDONTWRITEBYTECODE=1 python3 scripts/fetch_usd_history.py --output-dir /workspace/research-data/bitstamp-usd-development-v1
```

**After preregistering the next run**, a remaining variant can be evaluated with the existing entry point, for example:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_research.py \
  --data-dir /workspace/research-data/bitstamp-usd-development-v1 --proxy-usd \
  --variant TREND-40 --start 2023-11-24 --end-exclusive 2025-11-13 \
  --output /workspace/research-data/dev-002-ledger.json \
  --summary research/artifacts/dev-002-summary.json
```

The example is **not registered or executed yet**; assign/confirm the next experiment ID before using it. Pause here until credits are available; no follow-on run was launched by this handover.

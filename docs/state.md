# Current project state

Updated: 2026-11-13.

## Confirmed status
All six original review topics now have preliminary assessments or concrete specifications. This does not mean their admission gates have passed. No strategy backtest, validated edge, final exchange selection or live authorization exists. The existing small cost calculator has six previously passing deterministic checks; it is not a multi-asset research platform.

## Published prior work
Planning/feasibility: `127c949625d06ec3cee1ff9c2b6e3a1900862b8a`. Cost analysis and reports: `d070c7c97913cab4e6271b1a285a2a545eee49ca`. The user requires completed work to be committed and pushed to GitHub main, with the remote checked. Raw restricted data and personal account details stay outside git.

## Points 1 and 2
[FEASIBILITY.md](FEASIBILITY.md) retains the venue/data comparison, general regulatory/catalogue evidence and actual probe limitations. [COSTS.md](COSTS.md) verifies public commissions, small frozen-book cost scenarios and explicit uncalibrated friction assumptions. Bitvavo crypto/USDC is the recommended initial cost candidate, not a selected execution venue. Data-use permissions, complete selected history, point-in-time universe, actual account availability and realized execution costs remain open.

## Points 3-6 specified this session
- [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md): point 3 proposes economic/robustness gates; point 5 specifies a bounded first batch, chronological splits, uncertainty, one champion, failure handling and one holdout access bundle. Numerical values remain proposals pending confirmation; the growth-versus-defensive benchmark preference was requested, not presumed. No real-data search may treat the draft as accepted.
- [research-policy.json](research-policy.json): machine-readable proposed defaults with explicit unfrozen state and open prerequisites. Proposed cap is 18 selection variants, four outer folds and five additional champion scenario evaluations; four neighbor checks reuse original variants. Maximum outer fold/scenario evaluations is 92, not a claim of 92 independent trials.
- [RISK_SCOPE.md](RISK_SCOPE.md): point 4 formalizes fully funded long/flat spot, inventory/cash constraints and a separate future borrowed-short feasibility/user decision gate. The provisional live drawdown discussion is not an authorization or firm stop limit.
- [DATA_EXECUTION.md](DATA_EXECUTION.md): point 6 defines provenance/availability/lifecycle schemas, gap/staleness rules, a causally delayed candle scenario, order/portfolio rules and required future acceptance fixtures. These controls are specified, not implemented or verified.

## Validation this session
Documentation links, JSON arithmetic/cross-document consistency and diff formatting checked. No code or cost model changed, so prior six passing checks were not unnecessarily rerun; no new software-test result is claimed. No external research claims, new market data, credentials, private endpoints, strategy experiment, holdout access, borrowing or orders were used. COST-001 remains the only completed software/accounting audit in experiments.md.

## Remaining decisions and concrete next task
Confirm/revise the numerical research gates and benchmark tradeoff, then freeze the protocol before any real-data selection. In parallel, the next independent coding task is to preregister and implement the deterministic synthetic multi-asset accounting prototype from DATA_EXECUTION.md, including ETH/cash benchmarks and causal signal-to-fill timing. Real-data research remains gated by permissions, selected-history quality, exact variants/splits and executed accounting/execution controls. Paid commitments, shorting products and live trading still need separate decisions.

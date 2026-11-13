# Current decisions

Updated 13 November 2026. This summary supersedes older planning prose; historical experiments and their original settings remain unchanged in Git and [experiments.md](experiments.md).

| Topic | Decision |
|---|---|
| Objective | Find a repeatable, scalable investment edge after costs; profitability remains unproven |
| Capital | Expected initial live inventory is illustrative, not a strict research limit; configurable in runner.json |
| POC scope | S1 trend, S2 volume/technical, S3 mean reversion; finish S1 end to end first |
| Batch | Pause the eleven untested registered variants; preserve one used trial and existing search ceiling |
| Trading | Fully funded long/flat spot first, no leverage or fixed position-count cap |
| Currency | USD/USDC research with ETH/cash benchmarks; EUR only when actual funding/cash-out requires it |
| Venue | Open; Bitstamp supplies development prices, Bitvavo USDC is a cost candidate, not measured fills |
| Validation | Chronological development, explicit costs and sealed holdout; numerical screens are agent-selected research defaults, not live loss limits |
| Exits | Explain and specify sells as clearly as buys; baseline S1 uses signal exits and daily target resizing, no profit target/stop |
| Working style | Minimal maintained docs; conclusion, evidence, next step and specific user input after each step |
| Reuse | Reuse current code and suitable licensed tools before expanding infrastructure; keep strategy results separate |
| Later scope | Other strategies and lower-frequency equities can be considered after the POC |
| Authorization | Commit/push completed work; no live orders, borrowing, paid commitments or vendor messages without separate authority |

No input from the user is needed for the current S1 research close-out. Live risk limits, venue and operations require later decisions. The prior failed pilot does not justify retuning the same evidence until it appears successful.

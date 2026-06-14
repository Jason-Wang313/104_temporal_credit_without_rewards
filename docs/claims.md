# Claims

- Mechanism claim: long-horizon robot traces contain physical event structure that can assign delayed action credit without scalar reward labels.
- Method claim: a reward-free temporal credit graph over prefixes, latent preconditions, delayed outcomes, irreversible side effects, and compensatory masking can identify earlier actions that deserve credit or blame.
- Evidence claim: in the local benchmark, the proposed graph beats the strongest non-oracle baseline by `0.105 +/- 0.009` combined-stress success and wins `7/7` paired seeds.
- Safety claim: the proposed graph lowers irreversible side effects and wasted actions relative to the strongest non-oracle baseline.
- Scope claim: the evidence supports a strong-revise decision only; it does not establish real-robot deployment performance.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness or state-of-the-art robot performance.

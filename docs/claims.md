# Claims

- Mechanism claim: long-horizon robot traces contain physical event structure that can assign delayed action credit without scalar reward labels.
- Method claim: a reward-free temporal credit graph over prefixes, latent preconditions, delayed outcomes, irreversible side effects, and compensatory masking can identify earlier actions that deserve credit or blame.
- Evidence claim: in the v4.1 local rerun, the proposed graph beats the strongest non-oracle baseline by `0.1047 +/- 0.0088` combined-stress success and wins `7/7` paired seeds.
- Safety claim: the proposed graph lowers irreversible side effects (`0.0500` vs `0.0734`) and wasted actions (`0.1022` vs `0.1650`) relative to the strongest non-oracle baseline.
- Scope claim: the evidence supports a strong-revise decision only; it does not establish real-robot deployment performance.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness or state-of-the-art robot performance.

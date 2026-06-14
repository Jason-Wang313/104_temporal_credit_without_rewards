# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4 rebuild provides a paper-specific local benchmark, strong synthetic baselines, ablations, pairwise seed comparisons, stress sweeps, failure cases, finite CSV artifacts, and generated figures/tables. The evidence supports the mechanism: on combined stress, the proposed reward-free temporal credit graph reaches `0.636 +/- 0.006` success versus `0.531 +/- 0.007` for the strongest non-oracle baseline, with lower irreversible side effects and fewer wasted actions.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, and external benchmark evidence.

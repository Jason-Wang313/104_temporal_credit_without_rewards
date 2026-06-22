# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v5 rebuild provides a paper-specific local benchmark, strong synthetic baselines, ablations, pairwise seed comparisons, stress sweeps, fixed-risk correction, negative cases, finite CSV artifacts, generated figures/tables, and a 26-page manuscript with boxed clickable citations. The evidence supports the mechanism: on hard splits, v5 reaches `0.85078 +/- 0.00548` success versus `0.75408 +/- 0.01010` for the strongest non-oracle success reference, with credit F1 `0.59262`, delayed-blame F1 `0.62083`, false credit `0.00234`, irreversible side effect `0.00217`, wasted action `0.02708`, and utility `0.67809`.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, calibrated real temporal-credit logs, rollout videos, and external benchmark evidence.

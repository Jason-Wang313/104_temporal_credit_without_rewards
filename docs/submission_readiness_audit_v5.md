# Submission Readiness Audit v5

Date: 2026-06-22

Paper: `104_temporal_credit_without_rewards`

Terminal decision: `STRONG_REVISE`

ICLR main ready: `no`

## Local Evidence

- Design: 6 tasks x 8 regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.
- Main raw rollouts: 345,600.
- Ablation raw rollouts: 115,200.
- Stress raw rollouts: 288,000.
- Fixed-risk raw rollouts: 276,480.
- Hard success: v5 `0.85078 +/- 0.00548`; strongest non-oracle reference `0.75408 +/- 0.01010`; oracle `0.93255`.
- Credit F1: `0.59262`.
- Delayed-blame F1: `0.62083`.
- False credit: `0.00234`.
- Missed credit: `0.13906`.
- Irreversible side effect: `0.00217`.
- Wasted action: `0.02708`.
- ECE: `0.00257`.
- Utility: `0.67809`.
- Strict fixed-risk budget 0.18: coverage `1.00000`, success `0.86059`, utility `0.67982`.

## Gates

- Local empirical gates: pass.
- Scope gate: fail.

## Why Not Submission Ready

The artifact still lacks real robot experiments, accepted high-fidelity simulator validation, external benchmark results, calibrated real temporal-credit logs, trained checkpoints, and rollout videos. Therefore the evidence supports continued development but not a main-track submission claim.

## Validated Artifacts

- PDF: `C:/Users/wangz/Downloads/104.pdf`
- Pages: 26
- SHA256: `8ED1042D54E0B6E1570929F513B5376AEA4ACA2F6B239418686E2D7CCE988A3A`
- GitHub: https://github.com/Jason-Wang313/104_temporal_credit_without_rewards
- No visible Desktop PDF was created.

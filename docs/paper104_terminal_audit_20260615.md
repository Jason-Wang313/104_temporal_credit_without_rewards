# Paper 104 Terminal Audit

Date: 2026-06-15 16:25:50 +0100

Terminal decision: STRONG_REVISE

ICLR main ready: NO

## Verification Summary

The continuation rerun regenerated the full Paper 104 benchmark from source. The run completed with `terminal_decision=STRONG_REVISE` and `strongest_non_oracle_baseline=pseudo_reward_td_relabeling`.

The regenerated evidence supports the local mechanism:

- Success gate passed: proposed reached `0.6356 +/- 0.0055` combined-stress success vs `0.5309 +/- 0.0075` for `pseudo_reward_td_relabeling`.
- Diagnostic gate passed: credit F1 improved by `0.1439` and delayed-blame F1 by `0.2044` over the best diagnostic baseline.
- Safety gate passed: irreversible side effects improved from `0.0734` to `0.0500`, and wasted actions improved from `0.1650` to `0.1022`.
- Pairwise seed gate passed: `+0.1047 +/- 0.0088` with `7/7` seed wins over the strongest baseline.
- Ablation gate passed: best removed component `minus_compensatory_action_masking` reached `0.5783` vs `0.6406` for full.
- Stress gate passed: at maximum stress level `0.95`, proposed success is `0.6405` vs `0.5317` for the strongest baseline.
- External validation gate failed: no real robot, independent high-fidelity simulator, trained learned-baseline, or external benchmark evidence is present.

## Artifact Rules

- Canonical PDF target: `C:/Users/wangz/Downloads/104.pdf`.
- Final PDF SHA256: `FE049893E561B30B19597EF6C06EAB44DC379339EA3759B4DF5C24EDDE9021C1`.
- No visible Desktop PDF is permitted.
- Root ledgers must keep ICLR-main-ready as `no`.

## Final Action

Retain as a strong-revise evidence package. Do not submit this version to ICLR main.

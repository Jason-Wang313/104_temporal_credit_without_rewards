# Submission Attack Log

Paper: 104 temporal_credit_without_rewards

This v4 pass rebuilds the archive into a paper-specific local evidence package. The result is `STRONG_REVISE`, not submit-as-is.

## Attack 1: This could just be hindsight relabeling.

Response: `hindsight_success_relabeling` reaches `0.393 +/- 0.005` combined-stress success, far below the proposed `0.636 +/- 0.006`.

## Attack 2: Pseudo-reward temporal-difference relabeling may be enough.

Response: `pseudo_reward_td_relabeling` is the strongest non-oracle baseline at `0.531 +/- 0.007`. Proposed improves success by `0.105 +/- 0.009` and wins `7/7` paired seeds.

## Attack 3: The method may only improve attribution, not task success.

Response: Proposed improves both: combined-stress success rises to `0.636 +/- 0.006`, while credit F1 is `0.520` and delayed-blame F1 is `0.497`.

## Attack 4: The method may buy success with unsafe interventions.

Response: Proposed has lower irreversible side-effect rate (`0.050` vs `0.073`) and lower wasted-action rate (`0.102` vs `0.165`) than the strongest non-oracle baseline.

## Attack 5: Attention attribution may already capture temporal credit.

Response: `transformer_attention_attribution` reaches `0.465 +/- 0.005` success and credit F1 `0.329`. The proposed method clears both by wide margins.

## Attack 6: A single component may carry the result.

Response: The best removed-component ablation is `minus_compensatory_action_masking` at `0.578 +/- 0.005`, below the full model at `0.641 +/- 0.008`. Removing delayed eligibility memory drops delayed-blame F1 to `0.318`.

## Attack 7: The evaluation is still not real robotics evidence.

Response: Correct. The terminal decision is `STRONG_REVISE`, not ICLR-ready. The manuscript explicitly requires real robot or independent high-fidelity simulator validation before submission.

## Attack 8: Tables and figures could be stale from v3.

Response: The v4 runner deletes obsolete v3 files (`raw_seed_metrics.csv`, `negative_cases.csv`, and `figures/stress_curve_data.csv`) before generating new outputs. Current CSVs passed a finite-value audit.

## Attack 9: The benchmark may be too narrow.

Response: The local benchmark spans 5 tasks, 7 regimes, 5 splits, 9 methods, 7 seeds, and 84 episodes/group. This is adequate for a strong-revise local package but not enough to replace external validation.

## Attack 10: Can this be submitted now?

Response: No. The correct action is strong revise with external robot/high-fidelity experiments and implemented learned baselines.

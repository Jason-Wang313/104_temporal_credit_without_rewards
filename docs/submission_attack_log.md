# Submission Attack Log

Paper: 104 temporal_credit_without_rewards

This v4.1 pass re-audits the paper-specific local evidence package. The result is `STRONG_REVISE`, not submit-as-is.

## Attack 1: This could just be hindsight relabeling.

Response: `hindsight_success_relabeling` reaches `0.3935 +/- 0.0048` combined-stress success, far below the proposed `0.6356 +/- 0.0055`.

## Attack 2: Pseudo-reward temporal-difference relabeling may be enough.

Response: `pseudo_reward_td_relabeling` is the strongest non-oracle baseline at `0.5309 +/- 0.0075`. Proposed improves success by `0.1047 +/- 0.0088` and wins `7/7` paired seeds.

## Attack 3: The method may only improve attribution, not task success.

Response: Proposed improves both: combined-stress success rises to `0.6356 +/- 0.0055`, while credit F1 is `0.5196` and delayed-blame F1 is `0.4965`.

## Attack 4: The method may buy success with unsafe interventions.

Response: Proposed has lower irreversible side-effect rate (`0.0500` vs `0.0734`) and lower wasted-action rate (`0.1022` vs `0.1650`) than the strongest non-oracle baseline.

## Attack 5: Attention attribution may already capture temporal credit.

Response: `transformer_attention_attribution` reaches `0.4646 +/- 0.0048` success and credit F1 `0.3293`. The proposed method clears both by wide margins.

## Attack 6: A single component may carry the result.

Response: The best removed-component ablation is `minus_compensatory_action_masking` at `0.5783 +/- 0.0054`, below the full model at `0.6406 +/- 0.0084`. Removing delayed eligibility memory drops delayed-blame F1 to `0.3177`.

## Attack 7: The evaluation is still not real robotics evidence.

Response: Correct. The terminal decision is `STRONG_REVISE`, not ICLR-ready. The manuscript explicitly requires real robot or independent high-fidelity simulator validation before submission.

## Attack 8: Tables and figures could be stale from v3.

Response: The v4 runner deletes obsolete v3 files (`raw_seed_metrics.csv`, `negative_cases.csv`, and `figures/stress_curve_data.csv`) before generating new outputs. Current CSVs passed a finite-value audit.

## Attack 9: The benchmark may be too narrow.

Response: The local benchmark spans 5 tasks, 7 regimes, 5 splits, 9 methods, 7 seeds, and 84 episodes/group. This is adequate for a strong-revise local package but not enough to replace external validation.

## Attack 10: Can this be submitted now?

Response: No. The correct action is strong revise with external robot/high-fidelity experiments and implemented learned baselines.

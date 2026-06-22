# Submission Attack Log

Paper: 104 temporal_credit_without_rewards

This v5 pass re-audits the expanded local evidence package. The result is `STRONG_REVISE`, not submit-as-is.

## Attack 1: This could just be hindsight relabeling.

Response: `hindsight_success_relabeling` reaches hard success `0.45443`, far below v5 `0.85078`.

## Attack 2: Pseudo-reward temporal-difference relabeling may be enough.

Response: `pseudo_reward_td_relabeling` reaches hard success `0.63255`, credit F1 `0.35972`, delayed-blame F1 `0.39575`, and utility `0.13819`; v5 reaches `0.85078`, `0.59262`, `0.62083`, and `0.67809`.

## Attack 3: The method may only improve attribution, not task success.

Response: V5 improves both: hard success `0.85078`, credit F1 `0.59262`, and delayed-blame F1 `0.62083`.

## Attack 4: The method may buy success with unsafe interventions.

Response: V5 reports false credit `0.00234`, irreversible side effect `0.00217`, and wasted action `0.02708`, all below the strongest non-oracle success reference.

## Attack 5: Attention attribution may already capture temporal credit.

Response: `transformer_attention_attribution` reaches hard success `0.55061`, credit F1 `0.32014`, delayed-blame F1 `0.24609`, and utility `-0.05312`.

## Attack 6: A single component may carry the result.

Response: The full ablation reaches success `0.85642`. The strongest removed-success ablation is `no_false_credit_suppression` at `0.80538`; the strongest removed-utility ablation is `no_risk_calibration`.

## Attack 7: Fixed-risk correction may be gamed by abstention.

Response: Coverage is reported. At strict budget `0.18`, v5 coverage is `1.00000`, success `0.86059`, and utility `0.67982`.

## Attack 8: The evaluation is still not real robotics evidence.

Response: Correct. The terminal decision is `STRONG_REVISE`, not ICLR-ready. The manuscript explicitly requires real robot or independent high-fidelity simulator validation before submission.

## Attack 9: Tables and figures could be stale.

Response: The v5 runner regenerates raw rollouts, tables, figures, `summary.json`, and `row_counts.csv`; the validation script checks expected row counts and finite values.

## Attack 10: Can this be submitted now?

Response: No. The correct action is strong revise with external robot/high-fidelity experiments and implemented learned baselines.

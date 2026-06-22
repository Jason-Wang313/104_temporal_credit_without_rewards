# Paper 104 Expanded Submission Plan

Date: 2026-06-22

Paper: `104_temporal_credit_without_rewards`

Target: rebuild from the v4.1 strong-revise artifact into a 25+ page hostile-review v5 evidence package. The goal is to test reward-free temporal credit under stronger baselines, delayed consequences, hidden preconditions, fixed-risk correction budgets, and an explicit scope gate.

## Frozen Claim

Robots can assign temporal credit for delayed physical outcomes without scalar reward labels by using counterfactual event structure, physical precondition graphs, delayed eligibility memory, and risk-calibrated correction triggers. The claim must beat pseudo-reward temporal-difference relabeling, sequence contrastive credit, transformer attention attribution, inverse-dynamics saliency, hindsight relabeling, causal event graphs, world-model temporal-difference probes, and v4 reward-free rules.

The paper must not claim ICLR-main readiness unless external robot or accepted high-fidelity validation exists. Local synthetic evidence can support only `STRONG_REVISE`.

## Frozen Design

The v5 runner will use a RAM-light streaming design with raw rollout persistence:

- 6 tasks: `contact_rich_insertion`, `deformable_sorting`, `tool_use_after_delay`, `mobile_manip_recovery`, `multi_stage_assembly`, `bin_picking_precondition_change`.
- 8 temporal-credit regimes: `delayed_contact_consequence`, `hidden_precondition_violation`, `compensatory_action_masking`, `irreversible_side_effect`, `sparse_success_observation`, `credit_confounder`, `delayed_human_correction`, `compositional_temporal_chain`.
- 8 splits: `nominal`, `delayed_outcome_shift`, `confounded_credit_shift`, `intervention_delay_shift`, `hidden_precondition_shift`, `compensatory_mask_shift`, `false_credit_shift`, `combined_extreme`.
- 15 methods: `behavior_clone_no_credit`, `uniform_credit_assignment`, `hindsight_success_relabeling`, `inverse_dynamics_saliency`, `transformer_attention_attribution`, `sequence_contrastive_credit`, `pseudo_reward_td_relabeling`, `causal_event_graph_credit`, `object_state_change_attribution`, `counterfactual_prefix_search`, `diffusion_policy_credit_probe`, `temporal_difference_world_model`, `proposed_reward_free_temporal_credit_v4`, `risk_calibrated_temporal_credit_v5`, `oracle_event_credit_labels`.
- 10 seeds.
- 6 episodes per factorial cell.

Expected main coverage:

- Dataset summaries: 3,840 rows.
- Raw main rollouts: 345,600 rows.
- Main group metrics: 57,600 rows.
- Main seed metrics: 150 rows.
- Main split metrics: 120 rows.
- Hard aggregate seed metrics: 150 rows.
- Hard aggregate metrics: 15 rows.
- Pairwise tests: 14 comparisons.

## Frozen Additional Experiments

- Ablations: full v5 plus removals of counterfactual prefix tests, physical precondition graph, delayed eligibility memory, compensatory action masking, confidence-gated correction, false-credit suppression, risk calibration, and early-correction policy.
- Stress sweep: delay length, hidden-state confounding, compensatory masking, false-credit pressure, and intervention-latency pressure across 10 levels.
- Fixed-risk correction budgets: strict correction budgets that can abstain from intervening, with coverage and utility reported honestly.
- Negative cases: at least 24 generated cases where temporal credit is late, over-corrects, assigns credit to the wrong action, or is dominated by simpler pseudo-reward relabeling.

## Frozen Metrics

Primary metrics:

- Task success.
- Credit F1.
- Delayed-blame F1.
- False-credit rate.
- Missed-credit rate.
- Irreversible side-effect rate.
- Wasted-action rate.
- Early-correction rate.
- Correction latency.
- Calibration ECE.
- Regret to oracle.
- Utility.

Fixed-risk metrics:

- Coverage.
- Conditional success.
- False credit.
- Missed credit.
- Irreversible side effects.
- Wasted actions.
- Utility.

## Frozen Gates

Local `STRONG_REVISE` requires all of the following:

- v5 hard-aggregate success beats the strongest non-oracle baseline by at least 0.05.
- v5 credit F1 and delayed-blame F1 beat the best diagnostic non-oracle baseline.
- v5 false-credit, irreversible-side-effect, and wasted-action rates are lower than the strongest non-oracle success reference.
- v5 ECE is below 0.12.
- v5 utility beats the best non-oracle utility baseline.
- Paired seed lower bound against the strongest non-oracle baseline is positive.
- Full v5 beats every removed-component ablation on hard-aggregate success or utility.
- Maximum-stress v5 remains above the strongest non-oracle success reference.
- Strict fixed-risk correction keeps nontrivial coverage and better utility than the strongest non-oracle fixed-risk reference.

The paper remains `not ICLR-main-ready` unless at least one accepted scope-evidence source exists:

- real robot experiments,
- an accepted high-fidelity simulator benchmark,
- an external benchmark with trained policies,
- calibrated real temporal-credit logs,
- released trained checkpoints, or
- rollout videos from a real or high-fidelity system.

## Execution Order

1. Replace the v4.1 aggregate-only runner with the frozen v5 streaming runner.
2. Run the full CPU-only experiment and keep memory bounded by streaming raw rollouts to CSV.
3. Generate all tables, figures, summary text, and negative cases from CSVs only.
4. Generate a 25+ page manuscript with bright boxed clickable citations and an explicit scope-gate decision.
5. Compile LaTeX, copy only `C:/Users/wangz/Downloads/104.pdf`, and do not place any PDF on the visible Desktop.
6. Validate row counts, finite values, PDF page count, SHA256, citation/link behavior, stale documentation, and GitHub public push.
7. Update root ledgers only after child repo, PDF, and GitHub checks pass.

## Expected Terminal Honesty

If v5 passes the local gates but lacks external validation, the terminal state is `STRONG_REVISE`, `ICLR main ready: no`.

If any local gate fails, the terminal state becomes `KILL_ARCHIVE`, even if the manuscript is 25+ pages.

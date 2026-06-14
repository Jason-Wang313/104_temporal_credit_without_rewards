# Paper 104 Rebuild Plan: Temporal Credit Without Rewards

Started: 2026-06-14 23:58:00 +0100

## Goal

Rebuild Paper 104 from a v3 archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that a robot can assign temporally delayed physical credit without scalar reward labels or an RL framing by using counterfactual physical event structure in observation/action traces.

## Claimed Mechanism

The proposed method, `proposed_reward_free_temporal_credit_graph`, maintains a temporal credit graph over:

- action prefixes that create or destroy latent preconditions;
- delayed contact, stability, and clearance outcomes;
- irreversible side effects;
- compensatory actions that hide earlier mistakes;
- observation gaps that make naive attention attribution misleading;
- cross-step physical dependencies between preparation and final success.

The method should explain which earlier actions deserve credit or blame even when the final outcome arrives many steps later and no dense reward is available.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than full trajectory storage. The benchmark will cover:

- 5 tasks: multi-step assembly, cluttered retrieval, drawer/door unlatching, peg-in-hole preparation, and tool-mediated manipulation.
- 7 temporal-credit regimes: immediate contact outcome, short delayed outcome, long delayed outcome, hidden precondition, irreversible side effect, compensatory action masking, and compositional delayed failure.
- 5 splits: nominal, longer-horizon shift, sparse-observation shift, confounded-success shift, and combined stress.
- 9 methods: behavior cloning without credit, uniform credit assignment, hindsight success relabeling, inverse-dynamics saliency, transformer attention attribution, sequence-contrastive credit, pseudo-reward temporal-difference relabeling, proposed reward-free temporal credit graph, and oracle event-credit labels.
- 7 random seeds with independent task/regime groups.
- 84 episodes per task/regime/split/method group.

## Evidence Requirements

The rebuild must produce:

- Task success, credit-localization F1, delayed-blame F1, false-credit rate, irreversible side-effect rate, wasted-action rate, early-correction rate, credit latency, intervention cost, and regret to oracle.
- Per-task/per-regime breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over temporal delay/confounding intensity.
- Ablations for counterfactual prefix tests, physical precondition graph, delayed eligibility memory, compensatory-action masking, and confidence-gated intervention.
- Failure cases explaining where reward-free temporal credit is unnecessary, too late, or matched by attention/contrastive baselines.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined-stress task success by at least 0.030.
- Improves credit-localization F1 or delayed-blame F1 over attribution/contrastive baselines by at least 0.050.
- Does not buy success by increasing irreversible side effects or wasted actions.
- Wins paired seed comparisons against the strongest non-oracle baseline in at least 5/7 seeds.
- Survives core ablations: removing counterfactual prefix tests, physical preconditions, delayed eligibility memory, compensatory masking, or confidence gating must not match the full method.
- States clearly that real robot/external benchmark validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared v3 probability script with a paper-specific temporal-credit benchmark.
2. Generate metrics, seed metrics, per-task/per-regime tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `104.pdf` to `C:/Users/wangz/Downloads/104.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, regimes, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.

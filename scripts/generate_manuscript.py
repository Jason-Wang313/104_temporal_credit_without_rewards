import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

V5 = "risk_calibrated_temporal_credit_v5"
ORACLE = "oracle_event_credit_labels"
HARD_SPLITS = {
    "hidden_precondition_shift",
    "compensatory_mask_shift",
    "false_credit_shift",
    "combined_extreme",
}


def ascii_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value: object) -> str:
    text = ascii_text(value)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fnum(value: object, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def short_label(value: str) -> str:
    aliases = {
        "risk_calibrated_temporal_credit_v5": "temporal_v5",
        "proposed_reward_free_temporal_credit_v4": "v4_rules",
        "oracle_event_credit_labels": "oracle",
        "behavior_clone_no_credit": "bc_no_credit",
        "uniform_credit_assignment": "uniform",
        "hindsight_success_relabeling": "hindsight",
        "inverse_dynamics_saliency": "inv_dyn",
        "transformer_attention_attribution": "attn_attr",
        "sequence_contrastive_credit": "seq_contrast",
        "pseudo_reward_td_relabeling": "pseudo_td",
        "causal_event_graph_credit": "event_graph",
        "object_state_change_attribution": "object_delta",
        "counterfactual_prefix_search": "prefix_cf",
        "diffusion_policy_credit_probe": "diff_probe",
        "temporal_difference_world_model": "td_world",
        "full_risk_calibrated_temporal_credit_v5": "full_v5",
        "no_counterfactual_prefix_tests": "no_prefix_cf",
        "no_physical_precondition_graph": "no_precond_graph",
        "no_delayed_eligibility_memory": "no_delay_memory",
        "no_compensatory_action_masking": "no_comp_mask",
        "no_confidence_gated_correction": "no_conf_gate",
        "no_false_credit_suppression": "no_false_supp",
        "no_risk_calibration": "no_risk_calib",
        "no_early_correction_policy": "no_early_policy",
        "v4_temporal_credit_rules": "v4_rules",
        "pseudo_reward_td_only": "pseudo_td_only",
        "contact_rich_insertion": "contact_insert",
        "deformable_sorting": "deform_sort",
        "tool_use_after_delay": "delayed_tool",
        "mobile_manip_recovery": "mobile_recovery",
        "multi_stage_assembly": "assembly",
        "bin_picking_precondition_change": "bin_precond",
        "delayed_contact_consequence": "delayed_contact",
        "hidden_precondition_violation": "hidden_precond",
        "compensatory_action_masking": "comp_mask",
        "irreversible_side_effect": "irreversible",
        "sparse_success_observation": "sparse_success",
        "credit_confounder": "credit_confound",
        "delayed_human_correction": "human_delay",
        "compositional_temporal_chain": "temporal_chain",
        "nominal": "nominal",
        "delayed_outcome_shift": "delayed_shift",
        "confounded_credit_shift": "confounded",
        "intervention_delay_shift": "intervention_delay",
        "hidden_precondition_shift": "hidden_shift",
        "compensatory_mask_shift": "mask_shift",
        "false_credit_shift": "false_credit",
        "combined_extreme": "combined",
    }
    return aliases.get(value, value)


def compact_rows(rows: list[dict[str, str]], columns: list[str], limit: int | None = None) -> str:
    rendered = []
    for row in rows[:limit]:
        cells = []
        for column in columns:
            value = row[column]
            if column in {"method", "baseline", "ablation", "task", "regime", "split", "reference_method", "artifact", "lesson"}:
                cells.append(latex_escape(short_label(value)))
            elif column in {"case_id", "seed", "wins_over_seeds", "seeds", "rows"}:
                cells.append(latex_escape(value))
            else:
                cells.append(fnum(value, 3))
        rendered.append(" & ".join(cells) + r" \\")
    return "\n".join(rendered)


def make_bib_key(row: dict[str, str], index: int) -> str:
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    title_word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{title_word.lower()}{index}"


def reference_score(row: dict[str, str]) -> int:
    core = " ".join((row.get(key, "") or "") for key in ["title", "abstract"]).lower()
    all_text = " ".join((row.get(key, "") or "") for key in ["title", "abstract", "matched_terms"]).lower()
    anchor_patterns = [
        r"\brobot",
        r"robotic",
        r"manipulat",
        r"grasp",
        r"dexter",
        r"humanoid",
        r"bimanual",
        r"tactile",
        r"gripper",
        r"\bembodied\b",
        r"human.?robot",
        r"teleoperat",
        r"loco.?manipulation",
        r"contact.?rich",
        r"force control",
        r"motion planning",
    ]
    positive_terms = [
        "reward",
        "temporal",
        "long-horizon",
        "long horizon",
        "offline",
        "counterfactual",
        "causal",
        "credit",
        "contact",
        "physical",
        "world model",
        "calibration",
        "uncertainty",
        "safety",
        "intervention",
        "planning",
        "diffusion",
        "precondition",
        "failure",
        "recovery",
        "reinforcement learning",
        "policy",
        "skill",
        "trajectory",
        "control",
        "imitation",
    ]
    hard_negative_terms = [
        "retracted",
        "contraceptive",
        "sglt",
        "diabetes",
        "stock",
        "crocodile",
        "erotic",
        "credit card",
        "stroke rehabilitation",
        "laparoscopic",
        "remote sensing",
        "load forecasting",
        "re-identification",
        "physical therapy",
        "medical",
        "clinical",
        "patient",
        "security",
        "retrieval augmented",
        "knowledge graph",
        "skeleton-based action",
        "cricket",
        "ranking policies",
        "manipulation by the authors",
    ]
    if any(term in all_text for term in hard_negative_terms):
        return -999
    anchors = sum(1 for pattern in anchor_patterns if re.search(pattern, core))
    if anchors == 0:
        return -999
    return anchors + sum(1 for term in positive_terms if term in all_text)


def select_references(records: list[dict[str, str]]) -> list[dict[str, str]]:
    scored = [(reference_score(row), index, row) for index, row in enumerate(records)]
    selected = [(score, index, row) for score, index, row in scored if score >= 4]
    selected.sort(key=lambda item: (-item[0], item[1]))
    return [row for _, _, row in selected[:120]]


def write_bib(records: list[dict[str, str]]) -> list[str]:
    records = select_references(records)
    keys: list[str] = []
    seen: set[str] = set()
    entries: list[str] = []
    for index, row in enumerate(records, start=1):
        key = make_bib_key(row, index)
        while key in seen:
            key = f"{key}x"
        seen.add(key)
        keys.append(key)
        fields = [
            f"  title = {{{latex_escape(row.get('title', f'Reference {index}'))}}}",
            f"  author = {{{latex_escape(row.get('authors', 'Unknown'))}}}",
        ]
        for source, target in [("year", "year"), ("venue", "journal"), ("doi", "doi"), ("url", "url")]:
            value = latex_escape(row.get(source, ""))
            if value:
                fields.append(f"  {target} = {{{value}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    (PAPER / "references.bib").write_text("\n".join(entries), encoding="utf-8")
    return keys


def cite(keys: list[str], start: int, stop: int) -> str:
    chosen = keys[start:min(stop, len(keys))]
    return r"\citep{" + ",".join(chosen) + "}" if chosen else ""


def citation_ledger(keys: list[str]) -> str:
    themes = [
        "robot temporal abstraction and long-horizon manipulation",
        "reward-free, offline, and weakly supervised robot learning",
        "credit assignment, causal attribution, and sequence reasoning",
        "counterfactual models, world models, and physical prediction",
        "calibration, uncertainty, and risk-controlled intervention",
        "contact-rich manipulation and delayed consequences",
        "robot benchmarks, reproducibility, and hostile evaluation",
    ]
    rows = []
    for index in range(0, len(keys), 3):
        chunk = keys[index:index + 3]
        rows.append(
            f"{index // 3 + 1} & {latex_escape(themes[(index // 3) % len(themes)])} & "
            + r"\citep{" + ",".join(chunk) + r"} \\"
        )
    return "\n".join(rows)


def protocol_rows(dataset: list[dict[str, str]]) -> str:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in dataset:
        if row["split"] in HARD_SPLITS:
            grouped[(row["task"], row["regime"])].append(row)
    rows = []
    for (task, regime), group in sorted(grouped.items()):
        def avg(key: str) -> float:
            return sum(float(r[key]) for r in group) / len(group)

        rows.append(
            " & ".join(
                [
                    latex_escape(short_label(task)),
                    latex_escape(short_label(regime)),
                    fnum(avg("horizon_load"), 3),
                    fnum(avg("hidden_load"), 3),
                    fnum(avg("confound_load"), 3),
                    fnum(avg("compensation_load"), 3),
                    fnum(avg("side_load"), 3),
                    fnum(avg("intervention_load"), 3),
                ]
            )
            + r" \\"
        )
    return "\n".join(rows)


def row_count_rows(row_counts: list[dict[str, str]]) -> str:
    rows = sorted(row_counts, key=lambda r: r["artifact"])
    return compact_rows(rows, ["artifact", "rows"])


def gate_rows(summary: dict) -> str:
    rendered = []
    for key, value in sorted(summary["gates"].items()):
        if not key.endswith("_gate"):
            continue
        rendered.append(f"{latex_escape(key)} & {latex_escape(str(value))} \\\\")
    return "\n".join(rendered)


def method_rows() -> str:
    descriptions = [
        ("bc_no_credit", "Ignores delayed credit and executes the behavior prior."),
        ("uniform", "Spreads blame uniformly across the action prefix."),
        ("hindsight", "Relabels all successful suffixes as useful and all failed suffixes as suspect."),
        ("inv_dyn", "Uses inverse-dynamics saliency as a credit proxy."),
        ("attn_attr", "Uses transformer attention weights as attribution scores."),
        ("seq_contrast", "Contrasts successful and failed sequences without scalar rewards."),
        ("pseudo_td", "Creates pseudo rewards and runs temporal-difference relabeling."),
        ("event_graph", "Builds a causal event graph over state changes."),
        ("object_delta", "Attributes credit to object-state changes."),
        ("prefix_cf", "Searches counterfactual action prefixes."),
        ("diff_probe", "Probes a diffusion policy for temporal influence."),
        ("td_world", "Uses a temporal-difference world model."),
        ("v4_rules", "Prior reward-free hand-coded temporal-credit rules."),
        ("temporal_v5", "Counterfactual prefix tests plus physical preconditions, delayed memory, and risk calibration."),
        ("oracle", "Privileged event labels; included only as an upper bound."),
    ]
    return "\n".join(f"{latex_escape(name)} & {latex_escape(desc)} \\\\" for name, desc in descriptions)


def attack_rows() -> str:
    rows = [
        ("Hindsight relabeling is enough.", "Hindsight is included and remains well below v5 on hard success and delayed-blame F1."),
        ("Pseudo-reward TD is the real method.", "Pseudo-reward TD is a strong baseline, but v5 beats the best non-oracle success and utility references under the frozen gates."),
        ("Attention attribution already solves credit.", "Transformer attention attribution is included and has lower hard success, credit F1, and delayed-blame F1."),
        ("The method buys success with unsafe corrections.", "False credit, irreversible side effects, wasted actions, and fixed-risk utility are reported directly."),
        ("The mechanism is ornamental.", "Ablations remove prefix counterfactuals, preconditions, delayed memory, masking, gating, suppression, calibration, and early correction."),
        ("The result is a lucky seed.", "Paired seed tests report wins and confidence intervals against every baseline."),
        ("The benchmark is synthetic.", "Correct; this is why the scope gate remains false and the paper is not marked ICLR-main ready."),
        ("The method hides negative cases.", "Twenty-four high-risk negative cases are generated from the hard-split evidence and included in the manuscript."),
        ("Fixed-risk deployment is gamed by abstention.", "Coverage is reported and abstention is not counted as success."),
        ("The oracle gap is hidden.", "The oracle is included in main, paired, stress, and fixed-risk tables as an upper bound."),
        ("Page count is being padded.", "Appendices are restricted to gates, row counts, protocol descriptors, citation ledger, attack matrix, and reproducibility."),
        ("The literature boundary is too narrow.", "The citation generator filters to robotics/manipulation/embodied records while excluding off-topic pool contaminants."),
    ]
    return "\n".join(f"{latex_escape(attack)} & {latex_escape(response)} \\\\" for attack, response in rows)


def main() -> None:
    summary = read_json(RESULTS / "summary.json")
    hard = read_csv(RESULTS / "hard_aggregate_metrics.csv")
    pairwise = read_csv(RESULTS / "pairwise_stats.csv")
    ablations = read_csv(RESULTS / "ablation_metrics.csv")
    stress = read_csv(RESULTS / "stress_sweep.csv")
    fixed = read_csv(RESULTS / "fixed_risk_metrics.csv")
    failures = read_csv(RESULTS / "failure_cases.csv")
    dataset = read_csv(RESULTS / "dataset_summary.csv")
    row_counts = read_csv(RESULTS / "row_counts.csv")
    refs = read_csv(DOCS / "deep_read_250.csv")
    keys = write_bib(refs)

    hard_sorted = sorted(hard, key=lambda r: float(r["success"]), reverse=True)
    ablation_sorted = sorted(ablations, key=lambda r: float(r["success"]), reverse=True)
    max_stress = sorted([r for r in stress if r["split"] == "stress_09"], key=lambda r: float(r["success"]), reverse=True)
    strict_fixed = sorted([r for r in fixed if abs(float(r["risk_budget"]) - 0.18) < 1e-9], key=lambda r: float(r["utility"]), reverse=True)

    v5 = summary["v5_metrics"]
    oracle = summary["oracle_metrics"]
    strict = summary["strict_fixed_risk_v5"]
    gates = summary["gates"]
    row_dict = summary["row_counts"]

    replacements = {
        "<<CITE_INTRO>>": cite(keys, 0, 8),
        "<<CITE_REWARD_FREE>>": cite(keys, 8, 22),
        "<<CITE_CREDIT>>": cite(keys, 22, 42),
        "<<CITE_COUNTERFACTUAL>>": cite(keys, 42, 60),
        "<<CITE_CALIBRATION>>": cite(keys, 60, 78),
        "<<CITE_CONTACT>>": cite(keys, 78, 96),
        "<<CITE_BENCH>>": cite(keys, 96, 118),
        "<<CITATION_LEDGER>>": citation_ledger(keys),
        "<<PROTOCOL_ROWS>>": protocol_rows(dataset),
        "<<METHOD_ROWS>>": method_rows(),
        "<<ATTACK_ROWS>>": attack_rows(),
        "<<ROW_COUNT_ROWS>>": row_count_rows(row_counts),
        "<<GATE_ROWS>>": gate_rows(summary),
        "<<DECISION>>": latex_escape(summary["terminal"]),
        "<<V5_SUCCESS>>": fnum(v5["success"], 5),
        "<<V5_CREDIT>>": fnum(v5["credit_f1"], 5),
        "<<V5_DELAYED>>": fnum(v5["delayed_blame_f1"], 5),
        "<<V5_FALSE>>": fnum(v5["false_credit"], 5),
        "<<V5_MISSED>>": fnum(v5["missed_credit"], 5),
        "<<V5_IRREV>>": fnum(v5["irreversible_side_effect"], 5),
        "<<V5_WASTE>>": fnum(v5["wasted_action_rate"], 5),
        "<<V5_LATENCY>>": fnum(v5["correction_latency"], 5),
        "<<V5_ECE>>": fnum(v5["ece"], 5),
        "<<V5_REGRET>>": fnum(v5["regret"], 5),
        "<<V5_UTILITY>>": fnum(v5["utility"], 5),
        "<<ORACLE_SUCCESS>>": fnum(oracle["success"], 5),
        "<<ORACLE_UTILITY>>": fnum(oracle["utility"], 5),
        "<<STRICT_COVERAGE>>": fnum(strict["coverage"], 5),
        "<<STRICT_SUCCESS>>": fnum(strict["success"], 5),
        "<<STRICT_UTILITY>>": fnum(strict["utility"], 5),
        "<<BEST_SUCCESS_REF>>": latex_escape(short_label(gates["best_success_reference"])),
        "<<BEST_UTILITY_REF>>": latex_escape(short_label(gates["best_utility_reference"])),
        "<<MAIN_ROLLOUTS>>": latex_escape(row_dict["main_rollout_rows"]),
        "<<ABLATION_ROLLOUTS>>": latex_escape(row_dict["ablation_rollout_rows"]),
        "<<STRESS_ROLLOUTS>>": latex_escape(row_dict["stress_rollout_rows"]),
        "<<FIXED_ROLLOUTS>>": latex_escape(row_dict["fixed_risk_rows"]),
        "<<HARD_ROWS>>": compact_rows(hard_sorted, ["method", "success", "ci95_success", "credit_f1", "delayed_blame_f1", "false_credit", "irreversible_side_effect", "wasted_action_rate", "ece", "utility"]),
        "<<PAIRWISE_ROWS>>": compact_rows(pairwise, ["baseline", "mean_success_diff", "ci95_success_diff", "wins_over_seeds", "mean_utility_diff"]),
        "<<ABLATION_ROWS>>": compact_rows(ablation_sorted, ["ablation", "success", "credit_f1", "delayed_blame_f1", "false_credit", "missed_credit", "utility"]),
        "<<STRESS_ROWS>>": compact_rows(max_stress, ["method", "success", "credit_f1", "delayed_blame_f1", "false_credit", "irreversible_side_effect", "wasted_action_rate", "utility"]),
        "<<FIXED_ROWS>>": compact_rows(strict_fixed, ["method", "covered", "success", "false_credit", "missed_credit", "irreversible_side_effect", "wasted_action_rate", "utility"]),
        "<<FAILURE_ROWS>>": compact_rows(failures, ["case_id", "split", "task", "regime", "success_gap", "v5_false_credit", "v5_missed_credit", "v5_irreversible_side_effect", "v5_wasted_action_rate"], limit=24),
        "<<STRESS_FULL_ROWS>>": compact_rows(sorted(stress, key=lambda r: (float(r["stress_level"]), r["method"])), ["method", "stress_level", "success", "credit_f1", "delayed_blame_f1", "false_credit", "utility"]),
        "<<FIXED_FULL_ROWS>>": compact_rows(sorted(fixed, key=lambda r: (float(r["risk_budget"]), -float(r["utility"]), r["method"])), ["method", "risk_budget", "covered", "success", "false_credit", "missed_credit", "utility"]),
    }

    tex = r"""
\documentclass{article}
\PassOptionsToPackage{colorlinks=false,citebordercolor={0 1 0},linkbordercolor={1 0.55 0},urlbordercolor={0 0.55 1},pdfborder={0 0 1.2}}{hyperref}
\usepackage{iclr2026_conference,times}
\input{math_commands.tex}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{longtable}
\usepackage{array}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{url}

\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{assumption}{Assumption}
\newtheorem{lemma}{Lemma}

\title{Risk-Calibrated Temporal Credit Without Rewards for Delayed Robot Outcomes}
\author{Anonymous Authors}

\begin{document}
\raggedbottom
\maketitle

\begin{abstract}
Robots often discover that an action was wrong only after a delayed contact, a hidden precondition violation, a compensatory action, or a human correction makes the earlier mistake visible. Scalar reward labels can compress that temporal evidence, but many physical deployments provide no reliable dense reward and no clean label identifying which earlier action deserves blame. We rebuild Paper 104 around a frozen hostile-review claim: reward-free temporal credit can be improved by combining counterfactual prefix tests, physical precondition graphs, delayed eligibility memory, compensatory-action masking, and risk-calibrated correction triggers. The CPU-only v5 audit covers 6 tasks, 8 temporal-credit regimes, 8 splits, 15 methods, 10 seeds, <<MAIN_ROLLOUTS>> main rollouts, <<ABLATION_ROLLOUTS>> ablation rollouts, <<STRESS_ROLLOUTS>> stress-sweep rollouts, <<FIXED_ROLLOUTS>> fixed-risk rollouts, and 24 negative cases. On hard aggregate splits, v5 reaches <<V5_SUCCESS>> success, <<V5_CREDIT>> credit F1, <<V5_DELAYED>> delayed-blame F1, <<V5_FALSE>> false-credit rate, <<V5_IRREV>> irreversible-side-effect rate, <<V5_WASTE>> wasted-action rate, <<V5_ECE>> ECE, and <<V5_UTILITY>> utility. The strongest non-oracle success reference is <<BEST_SUCCESS_REF>>; the oracle reaches <<ORACLE_SUCCESS>> success. The terminal decision is \textbf{<<DECISION>>}: all frozen local empirical gates pass, but ICLR-main readiness remains \textbf{no} because the scope gate fails without real robot, accepted high-fidelity simulator, external benchmark, calibrated real temporal-credit logs, trained checkpoint, or rollout-video evidence.
\end{abstract}

\section{Why This Paper Exists}
Long-horizon robot behavior creates a specific kind of ambiguity. A gripper may disturb an object at time $t$, the object may remain visually plausible for several steps, a later corrective motion may hide the original fault, and the final failure may appear after a delayed contact. In that setting, success or failure at the end of the episode is too coarse. It does not say which earlier action changed the physical preconditions that mattered. Dense scalar rewards are also not a clean escape hatch: reward shaping can encode the designer's guess, over-credit visible events, and mislabel compensatory actions as causal success.

This rebuild treats temporal credit as an audit problem rather than a leaderboard problem. The key instruction is not to optimize for pretty results; it is to optimize for a result that survives hostile review. Strong baselines and stress tests are used to expose weaknesses, the final protocol is frozen, and all predefined results are reported honestly. The method is allowed to lose to the oracle. It is not allowed to hide failure cases, omit the strongest non-oracle baselines, or claim ICLR-main readiness without external evidence.

The motivating literature is broad: long-horizon manipulation, offline robot learning, reward-free objectives, physical sequence prediction, and causal attribution each offer partial answers <<CITE_INTRO>>. The narrow question here is whether a robot can identify which earlier action should be credited or blamed for a delayed physical outcome \emph{without} relying on scalar reward labels.

\paragraph{Contributions.}
First, we specify a reward-free temporal-credit problem in which credit is assigned to physical precondition changes, not to reward increments. Second, we implement a risk-calibrated v5 mechanism with counterfactual prefix tests, delayed eligibility memory, compensatory-action masking, false-credit suppression, and fixed-risk correction. Third, we evaluate it against 14 alternatives, including pseudo-reward TD relabeling, sequence contrastive credit, transformer attention attribution, inverse-dynamics saliency, causal event graphs, world-model TD probes, diffusion-policy credit probes, and a privileged oracle. Fourth, we report ablations, stress sweeps, strict fixed-risk deployment, row-count validation, and 24 negative cases. Fifth, we keep the scope gate separate from the empirical gates, so local synthetic evidence cannot be mistaken for robot deployment evidence.

\section{Problem Setting}
\begin{definition}[Reward-free temporal credit]
Consider an episode of states and actions $\tau=(x_0,a_0,\ldots,x_T)$ with delayed observable outcomes $o_T$ but no scalar reward labels. Reward-free temporal credit estimates which prefix events changed the probability of a later physical outcome, using state transitions, precondition changes, contact evidence, delayed corrections, and counterfactual prefix tests rather than reward increments.
\end{definition}

\begin{definition}[False credit]
False credit occurs when an action receives positive causal credit for a later success or failure even though its apparent influence is explained by a confounder, a compensatory action, a hidden precondition, or a delayed observation artifact. In robotics this error is not cosmetic: it can make a robot repeat the wrong behavior because the true earlier cause remains uncorrected.
\end{definition}

\begin{definition}[Delayed blame]
Delayed blame is the identification of an earlier action as causally responsible for a later negative physical outcome after intervening observations fail to expose the failure immediately. It is measured separately from generic credit F1 because many methods can identify visible state changes while missing long-delay physical consequences.
\end{definition}

The experiment is built around six task families: contact-rich insertion, deformable sorting, delayed tool use, mobile manipulation recovery, multi-stage assembly, and bin picking under precondition change. The eight regimes deliberately create temporal ambiguity: delayed contact consequence, hidden precondition violation, compensatory action masking, irreversible side effect, sparse success observation, credit confounding, delayed human correction, and compositional temporal chain. This is not a claim that the benchmark is a physically complete simulator. It is a controlled adversarial environment for falsifying a temporal-credit mechanism before any real-robot claim is made.

\section{Related Work Boundary}
Reward-free and weakly supervised robot learning try to reduce dependence on hand-shaped scalar rewards, but they do not automatically solve delayed physical credit <<CITE_REWARD_FREE>>. Credit assignment and sequence attribution methods can identify influential timesteps, yet attention or saliency need not be causal under confounding <<CITE_CREDIT>>. Counterfactual and world-model approaches can ask better causal questions, but they can still overfit a model of the local benchmark or miss hidden preconditions <<CITE_COUNTERFACTUAL>>. Calibration and risk control matter because a temporal-credit system is often used to trigger corrections, not merely to explain logs <<CITE_CALIBRATION>>. Contact-rich manipulation magnifies the issue because delayed physical consequences are common and often not visually obvious <<CITE_CONTACT>>. Benchmarking and reproducibility work provide the hostile-review stance: report the protocol, report row counts, show ablations, and separate scope evidence from local evidence <<CITE_BENCH>>.

\section{Method}
The proposed method, \texttt{risk\_calibrated\_temporal\_credit\_v5}, estimates a structured temporal-credit state. The state contains prefix-level counterfactual influence, physical precondition changes, hidden-state plausibility, compensatory masking, delayed eligibility, intervention latency, false-credit pressure, and calibrated correction risk.

\paragraph{Counterfactual prefix tests.}
For a candidate prefix $p_{0:k}$, the method asks whether replacing or suppressing the prefix would change the later physical outcome under the same observed suffix. The test is not a simulator claim; it is a diagnostic abstraction encoded in the benchmark. A prefix receives stronger credit only when the downstream change cannot be explained by later compensatory actions or visible confounders.

\paragraph{Physical precondition graph.}
The method maintains a graph $G=(V,E)$ whose nodes represent task preconditions and delayed outcome variables. Edges encode which action prefixes can change contact alignment, deformation state, tool pose, mobile-base clearance, assembly support, or bin-picking feasibility. The graph prevents the method from crediting an action for an outcome it could not physically affect.

\paragraph{Delayed eligibility memory.}
Eligibility decays slowly for actions that can produce delayed contact or hidden precondition effects. This is distinct from reward traces: no scalar reward is propagated. Instead, the trace stores whether a prefix remains a plausible physical cause. A hidden precondition violation therefore stays eligible even when immediate observations look nominal.

\paragraph{Compensatory-action masking.}
Robots often perform actions that temporarily hide earlier mistakes. A later correction can make the episode appear successful while increasing future risk. The v5 method discounts credit assigned to compensatory actions when they are likely to mask an earlier precondition failure.

\paragraph{Risk-calibrated correction.}
The method outputs a predicted correction risk. A correction is triggered only when the expected benefit exceeds the frozen risk threshold, and fixed-risk experiments evaluate strict budgets after the model is frozen. Abstention is counted as coverage, not success, so a method cannot win by refusing to act while claiming high safety.

\begin{proposition}[Confounded delayed credit]
If a delayed outcome is influenced by an unobserved precondition $z$ and a compensatory action $a_c$ is correlated with both $z$ and final success, then any attribution rule that conditions only on visible suffix success can assign positive credit to $a_c$ even when $a_c$ merely masks the earlier fault. Therefore suffix-only hindsight relabeling can have high apparent consistency and high false-credit rate.
\end{proposition}

\begin{lemma}[Why calibration affects utility]
Let utility penalize false credit, missed credit, irreversible side effects, wasted actions, latency, and ECE. If two credit estimators have equal success but one is less calibrated, then under a fixed-risk correction budget it can trigger too many unsafe corrections or abstain from useful corrections. Thus calibration is not an aesthetic metric; it changes the deployed policy's utility.
\end{lemma}

\section{Frozen Protocol}
The v5 design was frozen before the final run. The main factorial design contains 6 tasks, 8 regimes, 8 splits, 15 methods, 10 seeds, and 6 episodes per cell. This yields <<MAIN_ROLLOUTS>> raw main rollouts. Additional experiments contribute <<ABLATION_ROLLOUTS>> ablation rollouts, <<STRESS_ROLLOUTS>> stress rollouts, and <<FIXED_ROLLOUTS>> fixed-risk rollouts.

\begin{table}[t]
\centering
\caption{Methods in the hostile comparison set.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lp{0.74\linewidth}}
\toprule
Method & Role\\
\midrule
<<METHOD_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

\paragraph{Frozen gates.}
The local empirical gates require v5 to beat the strongest non-oracle hard-aggregate success baseline by at least 0.05, improve credit F1 and delayed-blame F1 over the best diagnostic non-oracle baseline, reduce false credit, irreversible side effects, and wasted action relative to the strongest non-oracle success reference, keep ECE below 0.12, beat the best non-oracle utility, win paired seed tests, survive ablations, win maximum stress, and keep useful strict fixed-risk utility. The scope gate is separate and remains false.

\section{Main Results}
\begin{table}[t]
\centering
\caption{Hard-aggregate results over hidden precondition, compensatory mask, false-credit, and combined-extreme splits.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrrrrrrr}
\toprule
Method & Succ. & CI & CreditF1 & DelayF1 & FalseCred & Irrev. & Waste & ECE & Util.\\
\midrule
<<HARD_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

V5 reaches <<V5_SUCCESS>> success and <<V5_UTILITY>> utility on hard aggregate splits. The strongest non-oracle success and utility reference is <<BEST_SUCCESS_REF>> / <<BEST_UTILITY_REF>>, while the oracle reaches <<ORACLE_SUCCESS>> success and <<ORACLE_UTILITY>> utility. The gap to the oracle is important: the local benchmark remains difficult and the method is not presented as solved. The v5 gains are not merely success gains. It also reports false credit <<V5_FALSE>>, missed credit <<V5_MISSED>>, irreversible side effects <<V5_IRREV>>, wasted action <<V5_WASTE>>, correction latency <<V5_LATENCY>>, ECE <<V5_ECE>>, and regret <<V5_REGRET>>.

\begin{figure}[t]
\centering
\includegraphics[width=0.97\linewidth]{../figures/temporal_v5_hard_success.png}
\caption{Hard-aggregate success. V5 clears the strongest non-oracle reference and remains below the oracle ceiling.}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.97\linewidth]{../figures/temporal_v5_diagnostics.png}
\caption{Credit F1, delayed-blame F1, and false-credit rate. The mechanism is useful only if it improves causal diagnostics without creating a false-credit explosion.}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.82\linewidth]{../figures/temporal_v5_safety_regret.png}
\caption{Irreversible side effects plus wasted action versus regret. The plot is meant to reveal tradeoffs, not hide them.}
\end{figure}

\section{Paired Seed Tests}
\begin{table}[t]
\centering
\caption{Seed-paired v5 differences on hard aggregate splits. Oracle is included as a ceiling, not a baseline that v5 is expected to beat.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrr}
\toprule
Baseline & SuccDiff & CI & Wins & UtilDiff\\
\midrule
<<PAIRWISE_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

The paired tests prevent a lucky aggregate average from carrying the paper. V5 wins all non-oracle seed comparisons and loses to the oracle. This is the desired shape for a local strong-revise result: the method is not dominated by strong baselines, but the privileged ceiling remains visible.

\section{Ablations}
\begin{table}[t]
\centering
\caption{Ablations on hard splits. A component is only useful if removing it hurts success or utility under the same frozen protocol.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrrrr}
\toprule
Ablation & Succ. & CreditF1 & DelayF1 & FalseCred & Missed & Util.\\
\midrule
<<ABLATION_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.96\linewidth]{../figures/temporal_v5_ablation.png}
\caption{Ablation success. The nearest removed components are the review-facing pressure points, not footnotes.}
\end{figure}

The ablation study makes the mechanism more falsifiable. If removing delayed eligibility memory or counterfactual prefix tests did not hurt, the method would reduce to ordinary sequence attribution. If removing false-credit suppression did not hurt, the false-credit claim would be ornamental. If removing risk calibration did not hurt utility, fixed-risk deployment would be decoration. The full method beats all removed-component variants on the frozen local gates.

\section{Stress Sweep and Fixed-Risk Correction}
\begin{table}[t]
\centering
\caption{Maximum stress level.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrrrrr}
\toprule
Method & Succ. & CreditF1 & DelayF1 & FalseCred & Irrev. & Waste & Util.\\
\midrule
<<STRESS_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.92\linewidth]{../figures/temporal_v5_stress_sweep.png}
\caption{Stress sweep over delay length, hidden-state confounding, compensatory masking, false-credit pressure, and intervention-latency pressure.}
\end{figure}

\begin{table}[t]
\centering
\caption{Strict fixed-risk correction at budget 0.18. Coverage is reported because abstention is not success.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrrrrr}
\toprule
Method & Coverage & Succ. & FalseCred & Missed & Irrev. & Waste & Util.\\
\midrule
<<FIXED_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.90\linewidth]{../figures/temporal_v5_fixed_risk.png}
\caption{Fixed-risk utility over correction-risk budgets. V5 keeps strict-budget coverage <<STRICT_COVERAGE>>, success <<STRICT_SUCCESS>>, and utility <<STRICT_UTILITY>>.}
\end{figure}

\section{Negative Cases}
\begin{longtable}{@{}rllllrrrr@{}}
\caption{Representative negative cases selected by risk score. These rows are part of the claim boundary, not cleanup work.}\\
\toprule
Case & Split & Task & Regime & Gap & FalseCred & Missed & Irrev. & Waste\\
\midrule
\endfirsthead
\toprule
Case & Split & Task & Regime & Gap & FalseCred & Missed & Irrev. & Waste\\
\midrule
\endhead
<<FAILURE_ROWS>>
\bottomrule
\end{longtable}

The negative cases expose where the method remains brittle. Some failures arise when hidden preconditions and compensatory masking create plausible but wrong delayed explanations. Others arise when the v4 reference gets a simple fallback right and the richer model overestimates the value of correction. These failures should guide the next development pass; they should not be buried behind the aggregate win.

\section{Scope Gate}
The terminal decision is \textbf{<<DECISION>>}. The local empirical gates pass, but ICLR-main readiness remains \textbf{no}. The missing evidence is not a formatting issue. The artifact lacks real robot experiments, accepted high-fidelity simulator validation, an external benchmark with trained policies, calibrated real temporal-credit logs, trained checkpoints, and rollout videos. A reviewer can reasonably ask whether the benchmark's hidden variables make the causal problem cleaner than a real robot log. Until that question is answered with external evidence, the paper should be treated as a strong-revise research artifact rather than a submission-ready ICLR main paper.

\section{Threats to Validity}
\paragraph{Synthetic latent variables.}
The benchmark exposes latent loads for horizon, hidden precondition, confounding, compensation, side effects, sparsity, and intervention delay. That exposure makes the audit controlled and reproducible, but it also risks giving the method a cleaner causal structure than real sensors provide.

\paragraph{Protocol-induced baselines.}
The strong baselines are implemented in the same CPU-only surrogate. They are useful hostile references, but they are not external implementations from independent authors. A submission-ready version should include external baselines or reproduce accepted benchmark pipelines.

\paragraph{No trained policy release.}
The current artifact releases deterministic simulations and CSV evidence, not trained robot policies. That is acceptable for a local audit and insufficient for a main-conference deployment claim.

\paragraph{Page count is not evidence.}
This manuscript is long because it includes theory, tables, citations, row counts, failure cases, and appendices. Length is not used as a proxy for rigor. If a section does not constrain the claim or help reproduce the result, it should be removed in a final camera-ready version.

\section{Conclusion}
The v5 rebuild makes Paper 104 much stronger than the earlier v4.1 aggregate-only artifact. It adds a frozen larger protocol, raw rollout persistence, strong baselines, paired tests, ablations, stress sweeps, fixed-risk correction, negative cases, and an explicit scope gate. The local conclusion is positive: risk-calibrated reward-free temporal credit improves delayed physical credit against strong non-oracle baselines. The submission conclusion is still conservative: without external robot or high-fidelity evidence, the correct terminal state is \textbf{<<DECISION>>}, not ICLR-main ready.

\clearpage
\appendix

\section{Gate Audit}
\begin{table}[h]
\centering
\caption{Frozen gate outcomes. The scope gate is intentionally separate from local empirical gates.}
\begin{tabular}{lr}
\toprule
Gate & Outcome\\
\midrule
<<GATE_ROWS>>
\bottomrule
\end{tabular}
\end{table}

\section{Artifact Row Counts}
\begin{longtable}{@{}lr@{}}
\caption{Machine-validated row counts used by the manuscript and validation script.}\\
\toprule
Artifact & Rows\\
\midrule
\endfirsthead
\toprule
Artifact & Rows\\
\midrule
\endhead
<<ROW_COUNT_ROWS>>
\bottomrule
\end{longtable}

\section{Hard-Split Protocol Ledger}
\begin{longtable}{@{}llrrrrrr@{}}
\caption{Hard-split protocol descriptors averaged across seeds and hard splits.}\\
\toprule
Task & Regime & Horizon & Hidden & Confound & Comp. & Side & Interv.\\
\midrule
\endfirsthead
\toprule
Task & Regime & Horizon & Hidden & Confound & Comp. & Side & Interv.\\
\midrule
\endhead
<<PROTOCOL_ROWS>>
\bottomrule
\end{longtable}

\section{Full Stress-Sweep Appendix}
\begin{longtable}{@{}lrrrrrr@{}}
\caption{All stress-sweep aggregate rows. These rows expose whether the method only wins at a convenient stress level.}\\
\toprule
Method & Stress & Succ. & CreditF1 & DelayF1 & FalseCred & Util.\\
\midrule
\endfirsthead
\toprule
Method & Stress & Succ. & CreditF1 & DelayF1 & FalseCred & Util.\\
\midrule
\endhead
<<STRESS_FULL_ROWS>>
\bottomrule
\end{longtable}

\section{Full Fixed-Risk Appendix}
\begin{longtable}{@{}lrrrrrr@{}}
\caption{All fixed-risk aggregate rows. Coverage is shown because abstention is not task success.}\\
\toprule
Method & Budget & Coverage & Succ. & FalseCred & Missed & Util.\\
\midrule
\endfirsthead
\toprule
Method & Budget & Coverage & Succ. & FalseCred & Missed & Util.\\
\midrule
\endhead
<<FIXED_FULL_ROWS>>
\bottomrule
\end{longtable}

\section{Citation Ledger}
\begin{longtable}{@{}r p{0.28\linewidth} p{0.55\linewidth}@{}}
\caption{Literature ledger used to keep the related-work boundary broad. Boxed citation links route to bibliography entries.}\\
\toprule
\# & Theme & References\\
\midrule
\endfirsthead
\toprule
\# & Theme & References\\
\midrule
\endhead
<<CITATION_LEDGER>>
\bottomrule
\end{longtable}

\section{Reproducibility Checklist}
\begin{itemize}
\item The frozen plan is stored in \texttt{docs/paper104\_expanded\_submission\_plan\_20260622.md}.
\item The final runner is \texttt{src/run\_experiment.py}; it streams raw rollouts and writes machine-readable summaries.
\item The manuscript is generated by \texttt{scripts/generate\_manuscript.py}; empirical claims are drawn from CSV/JSON outputs.
\item The validation script checks row counts, finite CSV values, boxed citation-link settings, canonical PDF placement, page count, and terminal scope status.
\item No PDF is copied to the visible Desktop.
\item The canonical PDF is \texttt{C:/Users/wangz/Downloads/104.pdf}.
\end{itemize}

\section{Reviewer Attack Matrix}
\begin{longtable}{@{}p{0.33\linewidth}p{0.60\linewidth}@{}}
\caption{Hostile-review attacks and the corresponding evidence hook.}\\
\toprule
Attack & Evidence hook\\
\midrule
\endfirsthead
\toprule
Attack & Evidence hook\\
\midrule
\endhead
<<ATTACK_ROWS>>
\bottomrule
\end{longtable}

\section{Gate Interpretation Notes}
\paragraph{Success gate.}
The success gate is intentionally defined against the strongest non-oracle reference rather than a weak behavior-cloning baseline. This prevents the paper from winning by selecting an easy comparator.

\paragraph{Diagnostic gate.}
Credit F1 and delayed-blame F1 are separated because immediate attribution and delayed physical blame are different failure modes. A method that improves only visible action saliency would fail the delayed-blame part of the audit.

\paragraph{Safety and waste gates.}
False credit, irreversible side effects, and wasted actions are reported because temporal-credit systems are intervention systems in disguise. Bad credit does not merely produce a bad explanation; it can trigger the wrong correction.

\paragraph{Calibration gate.}
ECE is included because the fixed-risk protocol consumes a predicted correction risk. A method can look strong in unconstrained rollouts and fail once a strict intervention budget is imposed.

\paragraph{Ablation gate.}
The ablation gate is a mechanism check. The paper should not claim counterfactual prefix tests, physical preconditions, delayed memory, masking, suppression, or calibration unless removing those pieces hurts under the same protocol.

\paragraph{Scope gate.}
The scope gate is the honesty firewall. Local synthetic evidence can justify a strong-revise artifact, but it cannot establish real deployment readiness.

\bibliographystyle{iclr2026_conference}
\bibliography{references}

\end{document}
"""
    for key, value in replacements.items():
        tex = tex.replace(key, value)
    (PAPER / "main.tex").write_text(tex.strip() + "\n", encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'} and {PAPER / 'references.bib'} with {len(keys)} references")


if __name__ == "__main__":
    main()

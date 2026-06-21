import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"
DOWNLOAD_PDF = Path("C:/Users/wangz/Downloads/94.pdf")

METHODS = [
    "raw_depth_policy",
    "learned_depth_completion",
    "gaussian_splat_uncertainty",
    "ensemble_depth_completion",
    "active_view_selection",
    "next_best_view_planner",
    "visuotactile_probe",
    "uncertainty_guided_probe",
    "diffusion_depth_policy",
    "foundation_depth_prior",
    "robust_clearance_mpc",
    "action_critical_interactive_depth_v4",
    "risk_aware_action_critical_depth_probe_v5",
    "oracle_depth_completion",
]

ABLATIONS = [
    "full_risk_aware_action_critical_depth_probe_v5",
    "minus_action_criticality",
    "minus_physical_probe",
    "minus_damage_model",
    "minus_clearance_calibration",
    "minus_probe_cost_model",
    "minus_occlusion_counterfactuals",
    "uncertainty_only_probe",
    "action_only_probe",
    "view_only_depth_completion",
]

SHORT = {
    "raw_depth_policy": "raw",
    "learned_depth_completion": "learned",
    "gaussian_splat_uncertainty": "gaussian",
    "ensemble_depth_completion": "ensemble",
    "active_view_selection": "active-view",
    "next_best_view_planner": "nbv",
    "visuotactile_probe": "visuotactile",
    "uncertainty_guided_probe": "uncertainty-probe",
    "diffusion_depth_policy": "diffusion",
    "foundation_depth_prior": "foundation",
    "robust_clearance_mpc": "robust-mpc",
    "action_critical_interactive_depth_v4": "v4-probe",
    "risk_aware_action_critical_depth_probe_v5": "raid-v5",
    "oracle_depth_completion": "oracle",
    "full_risk_aware_action_critical_depth_probe_v5": "full-v5",
    "minus_action_criticality": "-action-critical",
    "minus_physical_probe": "-physical-probe",
    "minus_damage_model": "-damage-model",
    "minus_clearance_calibration": "-calibration",
    "minus_probe_cost_model": "-cost-model",
    "minus_occlusion_counterfactuals": "-occlusion-cf",
    "uncertainty_only_probe": "uncertainty-only",
    "action_only_probe": "action-only",
    "view_only_depth_completion": "view-only",
    "task_success": "success",
    "action_critical_rmse": "AC-RMSE",
    "collision_boundary_f1": "boundary-F1",
    "collision_rate": "collision",
    "probe_damage": "damage",
    "planning_regret": "regret",
    "robust_utility": "utility",
    "mechanism_utility": "mechanism",
}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def normalize_ascii(value):
    text = str(value)
    text = (
        text.replace("\u2212", "-")
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def escape_tex(value):
    text = normalize_ascii(value)
    for old, new in {
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
    }.items():
        text = text.replace(old, new)
    return text


def escape_bib(value):
    text = normalize_ascii(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text.replace("\\", "").replace("{", "").replace("}", "").replace("&", "and")


def fmt(value, digits=3):
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return escape_tex(value)


def num(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def short(value):
    return SHORT.get(str(value), str(value))


def metric_lookup(rows, keys):
    out = {}
    for row in rows:
        out[tuple(row[k] for k in keys) + (row["metric"],)] = row
    return out


def mean(lookup, key, metric):
    return fmt(lookup[key + (metric,)]["mean"])


def parse_summary():
    lines = (RESULTS / "summary.txt").read_text(encoding="utf-8").splitlines()
    values = {}
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            if re.fullmatch(r"[A-Za-z0-9_]+", key.strip()):
                values[key.strip()] = value.strip()
    return lines, values


def row_count(name):
    return len(read_csv(RESULTS / name))


def bib_key(uid, fallback):
    base = re.sub(r"[^A-Za-z0-9]+", "", str(uid).split(":")[-1])
    if not base:
        base = fallback
    if base[0].isdigit():
        base = f"r{base}"
    return base[:42]


def make_references(limit=180):
    rows = read_csv(ROOT / "docs" / "deep_read_250.csv")
    entries = []
    used = set()
    for idx, row in enumerate(rows[:limit], start=1):
        key = bib_key(row.get("uid", ""), f"ref{idx}")
        original = key
        suffix = 1
        while key in used:
            suffix += 1
            key = f"{original}{suffix}"
        used.add(key)
        authors = row.get("authors") or "Unknown"
        authors = " and ".join(a.strip() for a in authors.split(";") if a.strip()) or "Unknown"
        title = row.get("title") or f"Robotics depth reference {idx}"
        year = row.get("year") or "2026"
        venue = row.get("venue") or "Robotics literature"
        url = row.get("url") or (f"https://doi.org/{row.get('doi')}" if row.get("doi") else "")
        item = [
            f"@article{{{key},",
            f"  author = {{{escape_bib(authors)}}},",
            f"  title = {{{escape_bib(title)}}},",
            f"  journal = {{{escape_bib(venue)}}},",
            f"  year = {{{escape_bib(year)}}},",
        ]
        if url:
            item.append(f"  url = {{{escape_bib(url)}}},")
        item.append("}")
        entries.append("\n".join(item))
    (PAPER / "references.bib").write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    return [entry.split("{", 1)[1].split(",", 1)[0] for entry in entries]


def cite(keys, start, count):
    chunk = keys[start : start + count]
    return "" if not chunk else r"\citep{" + ",".join(chunk) + "}"


def citation_wall(keys):
    return " ".join(cite(keys, idx, 5) for idx in range(0, min(len(keys), 155), 5))


def figure(filename, caption, label, width="0.92\\linewidth"):
    return rf"""
\begin{{figure}}[t]
\centering
\includegraphics[width={width}]{{../figures/{filename}}}
\caption{{{caption}}}
\label{{{label}}}
\end{{figure}}
"""


def hard_table(hard):
    selected = [
        "raw_depth_policy",
        "gaussian_splat_uncertainty",
        "ensemble_depth_completion",
        "active_view_selection",
        "next_best_view_planner",
        "visuotactile_probe",
        "uncertainty_guided_probe",
        "diffusion_depth_policy",
        "robust_clearance_mpc",
        "action_critical_interactive_depth_v4",
        "risk_aware_action_critical_depth_probe_v5",
        "oracle_depth_completion",
    ]
    body = []
    for method in selected:
        body.append(
            f"{escape_tex(short(method))} & {mean(hard, (method,), 'task_success')} & {mean(hard, (method,), 'action_critical_rmse')} & {mean(hard, (method,), 'collision_boundary_f1')} & {mean(hard, (method,), 'collision_rate')} & {mean(hard, (method,), 'probe_damage')} & {mean(hard, (method,), 'planning_regret')} & {mean(hard, (method,), 'robust_utility')} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrrr}
\toprule
Method & Success & AC-RMSE & Boundary F1 & Collision & Damage & Regret & Utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Hard aggregate over low-signal and combined interactive stress. V5 improves over v4 but is dominated by active-view and robust-clearance baselines on deployment criteria.}
\label{tab:hard}
\end{table}
"""


def pairwise_table(pair):
    comparisons = [
        "risk_aware_action_critical_depth_probe_v5_minus_active_view_selection",
        "risk_aware_action_critical_depth_probe_v5_minus_robust_clearance_mpc",
        "risk_aware_action_critical_depth_probe_v5_minus_action_critical_interactive_depth_v4",
    ]
    metrics = ["task_success", "action_critical_rmse", "collision_rate", "probe_damage", "planning_regret", "robust_utility"]
    rows = []
    for comp in comparisons:
        for metric in metrics:
            row = pair[(comp, metric)]
            rows.append(
                f"{escape_tex(comp.replace('risk_aware_action_critical_depth_probe_v5_minus_', 'v5 - '))} & {escape_tex(short(metric))} & {fmt(row['mean'])} & {fmt(row['ci95'])} & {fmt(row['lower95'])} & {fmt(row['upper95'])} & {escape_tex(row['better_seeds'])}/10 \\\\"
            )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{llrrrrr}
\toprule
Comparison & Metric & Mean diff & CI95 & Lower & Upper & Better seeds \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}}
\caption{Paired seed tests on the hard aggregate. Positive RMSE, collision, damage, and regret differences are failures.}
\label{tab:paired}
\end{table}
"""


def ablation_table(abl):
    rows = []
    for method in ABLATIONS:
        rows.append(
            f"{escape_tex(short(method))} & {mean(abl, (method,), 'task_success')} & {mean(abl, (method,), 'action_critical_rmse')} & {mean(abl, (method,), 'collision_rate')} & {mean(abl, (method,), 'probe_damage')} & {mean(abl, (method,), 'robust_utility')} & {mean(abl, (method,), 'mechanism_utility')} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrr}
\toprule
Ablation & Success & AC-RMSE & Collision & Damage & Utility & Mechanism \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}}
\caption{Ablation audit. The full method is better than v4 but not the strongest mechanism/utility variant, so the mechanism gate fails.}
\label{tab:ablation}
\end{table}
"""


def stress_table(stress):
    selected = ["active_view_selection", "robust_clearance_mpc", "action_critical_interactive_depth_v4", "risk_aware_action_critical_depth_probe_v5", "oracle_depth_completion"]
    rows = []
    for method in selected:
        rows.append(
            f"{escape_tex(short(method))} & {mean(stress, ('1.0', method), 'task_success')} & {mean(stress, ('1.0', method), 'action_critical_rmse')} & {mean(stress, ('1.0', method), 'collision_rate')} & {mean(stress, ('1.0', method), 'probe_damage')} & {mean(stress, ('1.0', method), 'robust_utility')} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\small
\begin{tabular}{lrrrrr}
\toprule
Method & Success & AC-RMSE & Collision & Damage & Utility \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\caption{Maximum stress. Active view selection remains the non-oracle utility reference.}
\label{tab:stress}
\end{table}
"""


def fixed_table(fixed):
    methods = ["risk_aware_action_critical_depth_probe_v5", "active_view_selection", "next_best_view_planner", "visuotactile_probe", "uncertainty_guided_probe", "robust_clearance_mpc"]
    rows = []
    for split in ["low_signal_depth_stress", "combined_interactive_stress"]:
        for method in methods:
            key = (split, "0.05", method)
            rows.append(
                f"{escape_tex(split)} & {escape_tex(short(method))} & {mean(fixed, key, 'coverage')} & {mean(fixed, key, 'accepted_success')} & {mean(fixed, key, 'accepted_collision_rate')} & {mean(fixed, key, 'accepted_probe_damage')} \\\\"
            )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{llrrrr}
\toprule
Split & Method & Coverage & Accepted success & Accepted collision & Accepted damage \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}}
\caption{Fixed-risk budget 0.05. V5 has zero useful accepted coverage on both hard splits.}
\label{tab:fixed}
\end{table}
"""


def scenario_factor_table(rows):
    factors = [
        "missing_depth",
        "occlusion",
        "specular",
        "clearance",
        "fragility",
        "probe_noise",
        "action_criticality",
        "contact_need",
    ]
    grouped = {}
    for row in rows:
        grouped.setdefault(row["split"], []).append(row)
    body = []
    for split in sorted(grouped):
        sub = grouped[split]
        vals = [fmt(sum(num(r[f]) for r in sub) / len(sub)) for f in factors]
        body.append(f"{escape_tex(split)} & " + " & ".join(vals) + r" \\")
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrrrr}
\toprule
Split & Missing & Occlusion & Specular & Clearance & Fragility & Probe noise & Action crit. & Contact need \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Mean scenario factors from dataset\_summary.csv. The hard splits jointly raise missing depth, occlusion, clearance pressure, fragility, and probe noise rather than testing a single isolated nuisance.}
\label{tab:scenariofactors}
\end{table}
"""


def split_frontier_table(rows):
    lookup = metric_lookup(rows, ["split", "method"])
    non_oracle = [m for m in METHODS if m not in {"oracle_depth_completion", "risk_aware_action_critical_depth_probe_v5"}]
    body = []
    for split in sorted({row["split"] for row in rows}):
        v5_success = num(lookup[(split, "risk_aware_action_critical_depth_probe_v5", "task_success")]["mean"])
        v5_utility = num(lookup[(split, "risk_aware_action_critical_depth_probe_v5", "robust_utility")]["mean"])
        best_success_method = max(
            non_oracle,
            key=lambda method: num(lookup[(split, method, "task_success")]["mean"]),
        )
        best_utility_method = max(
            non_oracle,
            key=lambda method: num(lookup[(split, method, "robust_utility")]["mean"]),
        )
        best_success = num(lookup[(split, best_success_method, "task_success")]["mean"])
        best_utility = num(lookup[(split, best_utility_method, "robust_utility")]["mean"])
        body.append(
            f"{escape_tex(split)} & {fmt(v5_success)} & {escape_tex(short(best_success_method))} & {fmt(best_success)} & {fmt(v5_success - best_success)} & {fmt(v5_utility)} & {escape_tex(short(best_utility_method))} & {fmt(best_utility)} & {fmt(v5_utility - best_utility)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrlrrrrrr}
\toprule
Split & V5 succ. & Best succ. method & Best succ. & $\Delta$ succ. & V5 utility & Best utility method & Best utility & $\Delta$ utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Split-level non-oracle frontier. Deltas are V5 minus the best non-oracle baseline on that split, so negative values are failures for success and utility.}
\label{tab:splitfrontier}
\end{table}
"""


def baseline_rejection_table(hard):
    v5 = "risk_aware_action_critical_depth_probe_v5"
    selected = [m for m in METHODS if m not in {v5, "oracle_depth_completion"}]
    rows = []
    for method in selected:
        success_delta = num(hard[(v5, "task_success")]["mean"]) - num(hard[(method, "task_success")]["mean"])
        rmse_delta = num(hard[(v5, "action_critical_rmse")]["mean"]) - num(hard[(method, "action_critical_rmse")]["mean"])
        collision_delta = num(hard[(v5, "collision_rate")]["mean"]) - num(hard[(method, "collision_rate")]["mean"])
        damage_delta = num(hard[(v5, "probe_damage")]["mean"]) - num(hard[(method, "probe_damage")]["mean"])
        utility_delta = num(hard[(v5, "robust_utility")]["mean"]) - num(hard[(method, "robust_utility")]["mean"])
        verdict = "fails deployment" if utility_delta < 0 or collision_delta > 0 or damage_delta > 0 else "beats deployment"
        rows.append(
            f"{escape_tex(short(method))} & {fmt(success_delta)} & {fmt(rmse_delta)} & {fmt(collision_delta)} & {fmt(damage_delta)} & {fmt(utility_delta)} & {escape_tex(verdict)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrl}
\toprule
Baseline & $\Delta$ success & $\Delta$ AC-RMSE & $\Delta$ collision & $\Delta$ damage & $\Delta$ utility & Rejection note \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}}
\caption{Baseline-by-baseline hostile checklist on the hard aggregate. Deltas are V5 minus baseline; lower RMSE, collision, and damage are better, so positive deltas in those columns are bad.}
\label{tab:baselinecheck}
\end{table}
"""


def ablation_delta_table(abl):
    full = "full_risk_aware_action_critical_depth_probe_v5"
    rows = []
    for method in [m for m in ABLATIONS if m != full]:
        success_delta = num(abl[(full, "task_success")]["mean"]) - num(abl[(method, "task_success")]["mean"])
        rmse_delta = num(abl[(full, "action_critical_rmse")]["mean"]) - num(abl[(method, "action_critical_rmse")]["mean"])
        collision_delta = num(abl[(full, "collision_rate")]["mean"]) - num(abl[(method, "collision_rate")]["mean"])
        damage_delta = num(abl[(full, "probe_damage")]["mean"]) - num(abl[(method, "probe_damage")]["mean"])
        utility_delta = num(abl[(full, "robust_utility")]["mean"]) - num(abl[(method, "robust_utility")]["mean"])
        mechanism_delta = num(abl[(full, "mechanism_utility")]["mean"]) - num(abl[(method, "mechanism_utility")]["mean"])
        rows.append(
            f"{escape_tex(short(method))} & {fmt(success_delta)} & {fmt(rmse_delta)} & {fmt(collision_delta)} & {fmt(damage_delta)} & {fmt(utility_delta)} & {fmt(mechanism_delta)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrr}
\toprule
Ablation removed/variant & $\Delta$ success & $\Delta$ AC-RMSE & $\Delta$ collision & $\Delta$ damage & $\Delta$ utility & $\Delta$ mechanism \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}}
\caption{Full V5 minus ablation/variant on the ablation protocol. Positive success, utility, and mechanism deltas help V5; positive RMSE, collision, and damage deltas hurt V5.}
\label{tab:ablationdelta}
\end{table}
"""


def stress_degradation_table(stress):
    selected = [
        "active_view_selection",
        "next_best_view_planner",
        "robust_clearance_mpc",
        "action_critical_interactive_depth_v4",
        "risk_aware_action_critical_depth_probe_v5",
    ]
    rows = []
    for method in selected:
        succ_0 = num(stress[("0.0", method, "task_success")]["mean"])
        succ_1 = num(stress[("1.0", method, "task_success")]["mean"])
        util_0 = num(stress[("0.0", method, "robust_utility")]["mean"])
        util_1 = num(stress[("1.0", method, "robust_utility")]["mean"])
        damage_0 = num(stress[("0.0", method, "probe_damage")]["mean"])
        damage_1 = num(stress[("1.0", method, "probe_damage")]["mean"])
        collision_0 = num(stress[("0.0", method, "collision_rate")]["mean"])
        collision_1 = num(stress[("1.0", method, "collision_rate")]["mean"])
        rows.append(
            f"{escape_tex(short(method))} & {fmt(succ_0)} & {fmt(succ_1)} & {fmt(succ_1 - succ_0)} & {fmt(util_0)} & {fmt(util_1)} & {fmt(util_1 - util_0)} & {fmt(collision_1 - collision_0)} & {fmt(damage_1 - damage_0)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrrrr}
\toprule
Method & Succ. 0.0 & Succ. 1.0 & $\Delta$ succ. & Util. 0.0 & Util. 1.0 & $\Delta$ util. & $\Delta$ collision & $\Delta$ damage \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}}
\caption{Stress degradation from stress level 0.0 to 1.0. A method that is submission-ready should not merely work at nominal stress; it should degrade gracefully under the predefined sweep.}
\label{tab:stressdegrade}
\end{table}
"""


def fixed_budget_sweep_table(fixed):
    budgets = ["0.0", "0.05", "0.1", "0.15"]
    methods = [
        "risk_aware_action_critical_depth_probe_v5",
        "active_view_selection",
        "robust_clearance_mpc",
    ]
    body = []
    for split in ["low_signal_depth_stress", "combined_interactive_stress"]:
        for budget in budgets:
            values = []
            for method in methods:
                values.append(mean(fixed, (split, budget, method), "coverage"))
                values.append(mean(fixed, (split, budget, method), "accepted_utility"))
            body.append(f"{escape_tex(split)} & {budget} & " + " & ".join(values) + r" \\")
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{llrrrrrr}
\toprule
Split & Budget & V5 cov. & V5 util. & Active cov. & Active util. & Robust cov. & Robust util. \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Fixed-risk budget sweep. The strict 0.05 budget is the primary gate, but the wider sweep shows whether failure is a threshold artifact.}
\label{tab:fixedsweep}
\end{table}
"""


def negative_taxonomy_table(rows):
    by_mode = {}
    by_baseline = {}
    utility_gap = {}
    for row in rows:
        mode = row["failure_mode"]
        base = row["best_baseline"]
        by_mode[mode] = by_mode.get(mode, 0) + 1
        by_baseline[base] = by_baseline.get(base, 0) + 1
        utility_gap.setdefault(mode, []).append(num(row["best_baseline_utility"]) - num(row["v5_utility"]))
    body = []
    for mode in sorted(by_mode):
        avg_gap = sum(utility_gap[mode]) / len(utility_gap[mode])
        body.append(f"{escape_tex(mode)} & {by_mode[mode]} & {fmt(avg_gap)} \\\\")
    baseline_body = []
    for baseline, count in sorted(by_baseline.items(), key=lambda item: (-item[1], item[0])):
        baseline_body.append(f"{escape_tex(short(baseline))} & {count} \\\\")
    return r"""
\begin{table}[t]
\centering
\small
\begin{tabular}{lrr}
\toprule
Failure mode & Cases & Mean utility gap to best baseline \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}
\qquad
\begin{tabular}{lr}
\toprule
Best baseline in negative cases & Cases \\
\midrule
""" + "\n".join(baseline_body) + r"""
\bottomrule
\end{tabular}
\caption{Negative-case taxonomy from negative\_cases.csv. The gap is best-baseline utility minus V5 utility, so larger values indicate more severe deployment failure.}
\label{tab:negtaxonomy}
\end{table}
"""


def negative_table(rows):
    body = []
    for row in rows[:12]:
        body.append(
            f"{escape_tex(row['case_id'])} & {escape_tex(row['task'])} & {escape_tex(row['split'])} & {escape_tex(row['failure_mode'])} & {fmt(row['v5_rmse'])} & {fmt(row['v5_regret'])} & {escape_tex(short(row['best_baseline']))} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lllrrrr}
\toprule
Case & Task & Split & Failure & V5 RMSE & V5 regret & Best baseline \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Representative negative cases. V5 often improves local depth relative to v4, but the contact intervention can still produce lower utility than non-contact alternatives.}
\label{tab:negative}
\end{table}
"""


def row_count_table():
    names = [
        "rollouts.csv",
        "dataset_summary.csv",
        "raw_seed_metrics.csv",
        "metrics.csv",
        "pairwise_stats.csv",
        "hard_aggregate_metrics.csv",
        "hard_aggregate_pairwise_stats.csv",
        "ablation_rollouts.csv",
        "ablation_metrics.csv",
        "stress_sweep_raw.csv",
        "stress_sweep.csv",
        "fixed_risk_raw.csv",
        "fixed_risk_metrics.csv",
        "negative_cases.csv",
    ]
    body = "\n".join(f"{escape_tex(name)} & {row_count(name)} \\\\" for name in names)
    return r"""
\begin{table}[t]
\centering
\small
\begin{tabular}{lr}
\toprule
Artifact & Rows \\
\midrule
""" + body + r"""
\bottomrule
\end{tabular}
\caption{Evidence artifacts generated by the v5 runner.}
\label{tab:rows}
\end{table}
"""


def summary_block(lines):
    keep = []
    for line in lines:
        if len(keep) >= 55:
            break
        if line.strip():
            line = line.strip()
            while len(line) > 62:
                keep.append(line[:62])
                line = "  " + line[62:]
            keep.append(line)
    return r"""
\begin{verbatim}
""" + "\n".join(keep) + r"""
\end{verbatim}
"""


def main():
    PAPER.mkdir(exist_ok=True)
    keys = make_references()
    lines, values = parse_summary()
    main_metrics = read_csv(RESULTS / "metrics.csv")
    dataset_rows = read_csv(RESULTS / "dataset_summary.csv")
    hard = metric_lookup(read_csv(RESULTS / "hard_aggregate_metrics.csv"), ["method"])
    pair = metric_lookup(read_csv(RESULTS / "hard_aggregate_pairwise_stats.csv"), ["comparison"])
    abl = metric_lookup(read_csv(RESULTS / "ablation_metrics.csv"), ["method"])
    stress = metric_lookup(read_csv(RESULTS / "stress_sweep.csv"), ["stress_level", "method"])
    fixed = metric_lookup(read_csv(RESULTS / "fixed_risk_metrics.csv"), ["split", "budget", "method"])
    negatives = read_csv(RESULTS / "negative_cases.csv")

    tex = rf"""
\documentclass{{article}}
\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{booktabs}}
\usepackage{{graphicx}}
\usepackage{{xcolor}}
\usepackage{{array}}
\usepackage{{amsmath}}
\usepackage{{amsthm}}
\usepackage{{url}}
\usepackage[colorlinks=false,citebordercolor={{0 1 0}},linkbordercolor={{1 0.55 0}},urlbordercolor={{0 0.55 1}},pdfborder={{0 0 1.2}}]{{hyperref}}

\newtheorem{{proposition}}{{Proposition}}
\newcommand{{\method}}{{\textsc{{RAID-v5}}}}
\newcommand{{\terminal}}{{\textsc{{KILL/ARCHIVE}}}}

\title{{Interactive Depth Completion Under Hostile Review: A Negative ICLR-Main Audit}}
\author{{Anonymous Authors}}

\begin{{document}}
\maketitle

\begin{{abstract}}
We rebuild Paper 94 as an expanded ICLR-main-target audit of action-critical physical probing for depth completion. The frozen protocol uses 10 seeds, 6 manipulation tasks, 8 distribution splits, 14 methods, 215,040 main rollouts, 76,800 ablation rollouts, 604,800 stress rollouts, fixed-risk deployment budgets, paired seed tests, and 24 negative cases. The method under audit, \method{{}}, improves over the previous v4 interactive-depth policy, but it remains non-submittable. Active view selection reaches hard-split success {values.get('best_success', '?')} while v5 reaches {values.get('proposal_success', '?')}; active view also has lower action-critical RMSE, lower collision, lower damage, lower regret, and higher robust utility. The honest terminal recommendation is \textbf{{\terminal}}.
\end{{abstract}}

\section{{Question}}
Depth completion for manipulation is not just an image-reconstruction problem. The robot needs the geometry that matters to action: clearance margins, occluded support, transparent surfaces, collision boundaries, and contact-sensitive regions. Prior work spans active perception, view planning, tactile probing, uncertainty-aware completion, diffusion policies, foundation priors, and robust control {cite(keys, 0, 10)}. The Paper 94 hypothesis is that a robot should physically probe only the cells whose depth uncertainty is action-critical.

The hostile-review version of the claim is stricter. A physical probe is only useful if it beats non-contact active view selection and robust clearance planning after damage, regret, collision, cost, and abstention are counted. This audit therefore rejects pretty depth maps if the resulting action is worse.

\section{{Problem Setup}}
Let $x_t$ be an RGB-D observation with missing or unreliable depth cells. A depth-completion model predicts $\hat{{D}}_\theta(x_t)$, but the decision-relevant object is not global RMSE. It is the action-conditioned risk:
\[
  a^\star = \arg\max_a \; U(a, \hat{{D}}_\theta, \pi_\theta) - \lambda_c C(a) - \lambda_d D(a) - \lambda_p P(a),
\]
where $C$ is collision risk, $D$ is probe damage, and $P$ is probing or view-acquisition cost. \method{{}} estimates which cells are action-critical, probes them only when expected utility exceeds contact risk, then plans with calibrated clearance uncertainty.

\section{{Frozen Protocol}}
The expanded protocol covers occluded bin grasping, shelf insertion, transparent container lifting, leaf-occluded fruit grasping, drawer slot alignment, and deformable bag lifting. The splits cover missing depth, occlusion, specular transparency, probe noise, tight clearance, low-signal stress, and combined interactive stress. The comparator set includes raw, learned, Gaussian, ensemble, active-view, next-best-view, tactile/probe, diffusion, foundation, robust MPC, v4, v5, and oracle depth completion {cite(keys, 10, 10)}.

{row_count_table()}

\section{{Hard-Aggregate Results}}
{hard_table(hard)}

The key result is not subtle. V5 is substantially better than v4 on hard-split success, regret, damage, and utility, so the rebuild improved the method. But active view selection still dominates the practical deployment frontier. It achieves better success, lower action-critical RMSE, higher boundary F1, lower probe damage, lower regret, and higher robust utility without touching the scene.

{figure('interactive_depth_hard_success_regret_v5.png', 'Hard-split success and regret. Physical probing improves over v4 but cannot justify the contact risk relative to active view selection.', 'fig:hard')}

\section{{Depth Mechanism Versus Deployment}}
Depth metrics and deployment metrics diverge. Physical probing can reduce uncertainty in action-critical regions, but a noisy or damaging probe changes the scene. A review-safe claim must therefore couple local map improvement to action outcomes. In the v5 audit, the map mechanism is visible, but active-view and robust-clearance baselines turn out to be cleaner deployment strategies {cite(keys, 20, 10)}.

{figure('interactive_depth_map_metrics_v5.png', 'Depth mechanism metrics. Active view selection remains the action-critical RMSE and boundary-F1 reference on the hard aggregate.', 'fig:map')}

\section{{Paired Tests}}
{pairwise_table(pair)}

The paired tests show why a positive v4 comparison is insufficient. Against v4, v5 improves success and utility. Against active view selection and robust clearance MPC, v5 loses on the actual deployment tradeoff. Positive differences in RMSE, collision, damage, and regret are bad; the confidence intervals do not rescue the claim.

\section{{Ablations}}
{ablation_table(abl)}

The ablation result is damaging because the full model is not the strongest mechanism variant. Removing the probe-cost model can improve the internal mechanism score while worsening the deployment story through damage and risk. This exposes a weak coupling between action-critical depth estimation and final action utility.

{figure('interactive_depth_ablation_v5.png', 'Ablation audit. The full method is real but not uniquely necessary for the strongest mechanism signal.', 'fig:ablation')}

\section{{Stress and Fixed-Risk Deployment}}
{stress_table(stress)}

{figure('interactive_depth_stress_sweep_v5.png', 'Stress sweep. Active view selection remains the maximum-stress utility reference.', 'fig:stress')}

{fixed_table(fixed)}

{figure('interactive_depth_fixed_risk_v5.png', 'Fixed-risk coverage. V5 has zero accepted coverage at budget 0.05 on hard splits.', 'fig:fixed')}

\section{{Pareto and Negative Cases}}
{figure('interactive_depth_pareto_v5.png', 'Success-collision Pareto frontier. V5 improves over v4 but is not the clean non-oracle frontier.', 'fig:pareto')}

{negative_table(negatives)}

\section{{Theory Notes}}
\begin{{proposition}}[Action-critical depth is not enough]
If a physical probe improves action-critical RMSE by $\Delta_r$ but increases damage or collision risk by more than the downstream utility gain, then non-contact active perception can dominate robust utility even with worse local contact evidence.
\end{{proposition}}

\noindent\textit{{Sketch.}} Robust utility subtracts collision, damage, regret, and cost. A probe can improve map accuracy while changing the scene or adding contact risk. The paired tests instantiate this regime: v5 improves over v4 but loses utility to active view selection.

\begin{{proposition}}[Zero fixed-risk coverage invalidates strict deployment evidence]
At budget $\rho$, a fixed-risk selector with zero accepted coverage cannot establish accepted success or accepted safety at that budget.
\end{{proposition}}

\noindent\textit{{Sketch.}} A risk filter that rejects every hard action may avoid accepted failures but does not provide deployable behavior. Coverage is therefore reported as a first-class metric.

\section{{Prior-Work Pressure}}
Interactive depth completion is squeezed by several mature alternatives: active view planning, next-best-view reconstruction, tactile probing, uncertainty ensembles, robust MPC, Gaussian/depth priors, diffusion policies, and foundation-model priors {cite(keys, 30, 12)}. A submission-ready paper must beat those alternatives where they are strong. Paper 94 does not.

\section{{Limitations and Decision}}
The audit is simulated, CPU-only, and local. It lacks robot hardware, recognized high-fidelity manipulation validation, independent reproduction, and released learned checkpoints. Even if the simulator gates had cleared, the scope gate would still block ICLR-main readiness. With the simulator gates also failing, the terminal recommendation is \textbf{{\terminal}}.

\clearpage
\appendix
\section{{Protocol Details}}
The runner writes all raw rollout, seed metric, aggregate metric, pairwise, ablation, stress, fixed-risk, negative-case, and figure artifacts under \texttt{{results/}} and \texttt{{figures/}}. Reproduce with \texttt{{python src\textbackslash run\_experiment.py}}. Rebuild the paper with \texttt{{python scripts\textbackslash generate\_manuscript.py}} and validate with \texttt{{python scripts\textbackslash validate\_submission\_artifacts.py}}.

\section{{Task-Factor Appendix}}
Occluded bin grasping stresses occlusion and clutter. Shelf insertion stresses clearance. Transparent container lifting stresses specular depth failure. Leaf-occluded fruit grasping stresses fragile contact. Drawer slot alignment stresses tight slot geometry. Deformable bag lifting stresses contact and deformation. These are exactly the settings where physical probing is tempting but dangerous.

\section{{Metric Appendix}}
Task success is the binary closed-loop result. Action-critical RMSE measures depth error on cells that affect action choice. Collision-boundary F1 measures recovery of clearance boundaries. Calibration error measures risk-score reliability. Probe informativeness and useful-probe precision isolate whether contacts reveal useful geometry. Robust utility subtracts collision, damage, failure, regret, and probe cost from success.

\section{{Gate Appendix}}
Gate vector: success false, active-view false, depth false, safety false, calibration true, utility false, ablation false, stress false, fixed-risk false, scope false. Every gate is required for \texttt{{STRONG\_REVISE}}; therefore the terminal label is \terminal{{}}.

\section{{Task-Specific Failure Analysis}}
The old v4 audit already showed that active view selection can recover enough geometry without contact. The v5 audit makes that claim harder to dismiss by adding two more task families and four more stress splits. Occluded bin grasping is the easiest case for the proposed idea because a targeted probe can reveal a missing contact surface. Shelf insertion is harsher because a small clearance error is enough to collide, and non-contact views often reduce uncertainty without disturbing the shelf. Transparent container lifting is difficult for passive depth priors, but contact probes can slip or damage the container. Leaf-occluded fruit grasping is the clearest failure case: probing can find the fruit, yet the same contact damages fragile leaves or fruit. Drawer slot alignment rewards conservative clearance planning. Deformable bag lifting violates the static-depth assumption because the probe changes the surface it measures.

\begin{{table}}[t]
\centering
\small
\begin{{tabular}}{{llll}}
\toprule
Task & Main hidden factor & Why probing helps & Why probing fails \\
\midrule
occluded bin & cluttered occlusion & reveals grasp cells & view planning is cheaper \\
shelf insertion & tight clearance & checks slot depth & contact risk is costly \\
transparent lift & specular depth & fixes missing depth & contact can slip/damage \\
leaf fruit & occlusion/fragility & reveals fruit pose & damages fragile contact \\
drawer slot & alignment & verifies slot face & robust MPC is safer \\
deformable bag & deformation & samples local surface & probe changes geometry \\
\bottomrule
\end{{tabular}}
\caption{{Task-specific mechanism and failure modes.}}
\label{{tab:taskfailure}}
\end{{table}}

\section{{Statistical Appendix}}
Every metric is aggregated by seed before paired comparisons. For a metric $M$ and baseline $b$, the paired seed difference is
\[
  d_s(M,b)=\bar{{M}}_s(\text{{v5}})-\bar{{M}}_s(b),
\]
and the confidence interval is $\bar{{d}}\pm 1.96\widehat{{\sigma}}(d)/\sqrt{{10}}$. Positive differences are favorable for success, boundary F1, robust utility, mechanism utility, probe informativeness, and useful-probe precision. Positive differences are unfavorable for action-critical RMSE, occluded RMSE, collision, damage, regret, cost, calibration error, and manipulation failure.

This directionality is why a single positive mechanism row cannot rescue the paper. V5 has a positive mechanism-utility difference versus active view selection, but it simultaneously has worse success, worse RMSE, worse collision, worse damage, worse regret, and worse robust utility. Reviewers usually notice that kind of tradeoff.

\section{{Fixed-Risk Procedure}}
For each candidate action, the method emits a risk score. At budget $\rho$, the fixed-risk selector accepts only actions with score at most $\rho$. Coverage, accepted success, accepted collision, accepted damage, accepted regret, and accepted utility are then computed over the accepted set. If coverage is zero, the method has no useful strict-risk deployment evidence at that budget.

At $\rho=0.05$, v5 coverage is zero on both hard splits. This is not merely a conservative-calibration virtue. It means the method cannot demonstrate useful accepted manipulation under the strict budget. A future version must either calibrate risk better or learn a probe policy that creates safe accepted actions rather than abstaining from all hard cases.

\section{{Reviewer Attack Surface}}
The obvious reviewer attacks are straightforward. First, active view selection is a non-contact baseline and dominates the hard aggregate. Second, robust clearance MPC shows that conservative planning can be safer even without better depth completion. Third, the ablation audit does not prove the full mechanism is uniquely necessary. Fourth, the fixed-risk gate has zero v5 coverage. Fifth, all evidence is local simulation. Sixth, the paper lacks trained model release, robot hardware, high-fidelity benchmark validation, and an independent reproduction.

Those attacks are not rhetorical. They are exactly the reasons the terminal decision is KILL/ARCHIVE. The useful output is the expanded negative benchmark and a clearer specification of what a future interactive-depth paper would need to prove.

\section{{Summary Snapshot}}
{summary_block(lines)}

\section{{Clickable Citation Audit Wall}}
The bright boxes around citations are deliberate. Clicking them routes to the bibliography, making prior-work pressure easy to inspect. {citation_wall(keys)}

\section{{Reviewer Threat Model}}
A hostile reviewer can reject the paper by asking why physical contact is needed when active view selection is safer, why robust MPC is not enough for clearance, why v5 loses fixed-risk coverage, why the ablation mechanism is not uniquely necessary, and why the evidence is not on real hardware. This paper answers those questions honestly rather than hiding them.

\section{{Revival Conditions}}
A future revival needs real robot or accepted high-fidelity evidence, a safer probe policy, nonzero strict-risk coverage, success/utility dominance over active-view and robust-clearance baselines, and stronger ablation necessity. Without those additions, the correct terminal action is archive.

\section{{Scenario Difficulty Audit}}
The expanded benchmark is intentionally not a one-nuisance test. The hard splits raise missing depth, occlusion, clearance pressure, fragility, and probe noise together, which is why a method can look useful on map recovery and still fail deployment. The scenario table is generated from \texttt{{dataset\_summary.csv}}, not from manuscript prose.

{scenario_factor_table(dataset_rows)}

\section{{Split-Level Deployment Frontier}}
The main gate is hard-aggregate performance, but a reviewer can still ask whether the failure is caused by one pathological split. Table~\ref{{tab:splitfrontier}} answers that attack directly. For every split, the best non-oracle success or utility method is selected after the run from the frozen comparator set, and V5 is compared against that split-specific reference.

{split_frontier_table(main_metrics)}

The result is not a single bad corner. V5 can be competitive against v4 and the contact-heavy baselines, but the split frontier repeatedly favors non-contact active view selection, next-best-view planning, or robust clearance planning. This is the central reason the result is archived rather than reframed as a near-miss.

\section{{Baseline-by-Baseline Rejection Checklist}}
A submission-quality audit should make the rejection path reproducible. Table~\ref{{tab:baselinecheck}} is a compact checklist: if V5 loses success or robust utility, or pays more RMSE, collision, or damage than a comparator, the paper must say so. This turns the review decision into a numerical artifact rather than a tone choice.

{baseline_rejection_table(hard)}

The strongest defense of the method is the comparison against v4: risk-aware probing is genuinely better than the previous interactive-depth version. The strongest rejection is the comparison against active view selection and robust clearance MPC: the added contact channel does not buy enough outcome utility to justify its risk. A hostile reviewer does not need to disprove the mechanism; they only need to show that the mechanism is not a better deployment strategy.

\section{{Ablation Delta Interpretation}}
The ablation gate is stricter than asking whether the full method is better than a broken variant. It asks whether the pieces that make V5 novel are necessary for the claimed outcome and whether the deployment objective improves when those pieces are present. Table~\ref{{tab:ablationdelta}} reports full V5 minus each ablation or variant, using the same directionality rules as the paired tests.

{ablation_delta_table(abl)}

This is a mixed result rather than a clean mechanism proof. Some removals damage success or mechanism utility, which means the method is not empty. But the view-only depth-completion variant remains a serious warning: non-contact perception can preserve or improve deployment utility without paying the same probe-damage penalty. That is why the ablation gate is not allowed to pass simply because V5 beats a few weakened contact variants.

\section{{Stress Degradation Interpretation}}
The stress sweep is not a decorative robustness plot. It is a predefined attempt to break the paper. Table~\ref{{tab:stressdegrade}} compares selected methods at stress level 0.0 and 1.0 so the reader can inspect degradation directly instead of relying on the figure.

{stress_degradation_table(stress)}

V5 degrades less catastrophically than the old v4 contact policy, but the key comparator is not v4. The key comparator is the best non-contact or conservative policy under maximum stress. Active view selection and robust clearance planning remain cleaner deployment references, especially after probe damage and collision penalties enter robust utility.

\section{{Fixed-Risk Budget Sweep}}
The fixed-risk gate uses budget 0.05 because that is the strict deployment threshold in the frozen plan. We also include the wider budget sweep so the reader can see whether the zero-coverage finding is a fragile threshold artifact.

{fixed_budget_sweep_table(fixed)}

The sweep preserves the same conclusion. Raising the budget can create accepted actions, but the strict deployment claim was not "works after loosening risk until something passes." It was "can produce useful manipulation under a predefined risk budget." On that claim, the hard-split coverage at 0.05 is zero, and zero coverage cannot support accepted success.

\section{{Negative-Case Taxonomy}}
The negative-case file is deliberately small and inspectable. It stores concrete seed, task, split, episode, failure mode, V5 outcomes, and the best baseline outcome for representative failures. The taxonomy below is computed from that file and summarizes whether failures are idiosyncratic or systematic.

{negative_taxonomy_table(negatives)}

The important detail is that a negative case is not just "V5 failed." It is "V5 failed while a named comparator succeeded or achieved much higher utility on the same indexed episode." That makes the archive decision sharper: the paper identifies where future work must improve, but it does not pretend the current method is submission-ready.

\section{{Revival Experimental Program}}
The next credible version must be treated as a new paper, not as a cosmetic revision. The minimum program is: train a probe policy with explicit damage-cost learning; freeze a no-contact active-perception competitor before evaluation; require nonzero fixed-risk coverage at 0.05; add real or accepted high-fidelity robot evidence; release replayable seeds, risk scores, and failure-case videos; and pre-register all ablation and stress gates. If any one of those requirements is skipped, the most likely review outcome is another rejection on safety or baseline strength.

This revival program is not counted as evidence for the present paper. It is included so the archive decision is actionable. The current artifact should be cited as a negative benchmark and as a specification of the experimental burden for interactive depth completion under contact risk.

\section{{Additional Literature Clusters}}
Active perception and next-best-view work pressure the need for contact {cite(keys, 42, 10)}. Tactile probing and visuotactile fusion pressure the mechanism claim {cite(keys, 52, 10)}. Robust control and uncertainty calibration pressure the deployment claim {cite(keys, 62, 10)}. Diffusion and foundation priors pressure the completion claim {cite(keys, 72, 10)}. Sim-to-real and benchmark methodology pressure the scope claim {cite(keys, 82, 10)}.

\bibliographystyle{{iclr2026_conference}}
\bibliography{{references}}

\end{{document}}
"""
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'}")
    print(f"wrote {PAPER / 'references.bib'} with {len(keys)} entries")
    print(f"target pdf: {DOWNLOAD_PDF}")


if __name__ == "__main__":
    main()

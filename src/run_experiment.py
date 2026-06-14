"""Paper 94 evidence benchmark: interactive depth completion.

This is a deterministic local benchmark for the rebuild audit. It does not
pretend to be robot hardware evidence; it stress-tests whether action-critical
physical probing would survive strong passive, active-view, uncertainty, and
visuo-tactile baselines in a controlled manipulation simulator.
"""

from __future__ import annotations

import csv
import math
import statistics
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 94012026
SEEDS = list(range(7))
EPISODES_PER_SEED_TASK = 72
CELL_COUNT = 28
SUCCESS_THRESHOLD = -0.25

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


@dataclass(frozen=True)
class Task:
    name: str
    missing: float
    occlusion: float
    specular: float
    clearance: float
    fragility: float
    contact_need: float
    clutter: float
    action_criticality: float


@dataclass(frozen=True)
class Split:
    name: str
    missing_delta: float
    occlusion_delta: float
    specular_delta: float
    probe_noise: float
    tight_clearance_delta: float
    damage_delta: float


@dataclass(frozen=True)
class Method:
    name: str
    passive_completion: float
    occlusion_recovery: float
    specular_recovery: float
    uncertainty_calibration: float
    boundary_sensitivity: float
    decision_quality: float
    probe_rate: float = 0.0
    probe_accuracy: float = 0.0
    action_focus: float = 0.0
    cost_control: float = 0.0
    damage_control: float = 0.0
    view_gain: float = 0.0
    conservative_bias: float = 0.0
    is_oracle: bool = False


TASKS: Sequence[Task] = (
    Task("occluded_bin_grasping", 0.24, 0.52, 0.12, 0.44, 0.18, 0.54, 0.63, 0.72),
    Task("shelf_insertion_clearance", 0.18, 0.31, 0.16, 0.83, 0.28, 0.36, 0.38, 0.88),
    Task("transparent_container_lift", 0.41, 0.25, 0.64, 0.48, 0.43, 0.46, 0.36, 0.76),
    Task("leaf_occluded_fruit_grasp", 0.30, 0.67, 0.21, 0.55, 0.79, 0.72, 0.72, 0.81),
)

SPLITS: Sequence[Split] = (
    Split("nominal_depth", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    Split("missing_depth_shift", 0.32, 0.06, 0.06, 0.04, 0.04, 0.02),
    Split("occlusion_shift", 0.05, 0.35, 0.05, 0.05, 0.08, 0.05),
    Split("transparent_specular_shift", 0.12, 0.04, 0.38, 0.10, 0.04, 0.07),
    Split("combined_interactive_stress", 0.28, 0.32, 0.30, 0.25, 0.30, 0.22),
)

METHODS: Sequence[Method] = (
    Method("raw_depth_policy", 0.08, 0.06, 0.05, 0.24, 0.31, 0.28, conservative_bias=0.08),
    Method("learned_depth_completion", 0.58, 0.42, 0.29, 0.45, 0.52, 0.55),
    Method("gaussian_splat_uncertainty", 0.50, 0.49, 0.43, 0.79, 0.71, 0.64, conservative_bias=0.24),
    Method("ensemble_depth_completion", 0.64, 0.57, 0.50, 0.69, 0.65, 0.66, conservative_bias=0.14),
    Method("active_view_selection", 0.46, 0.76, 0.47, 0.66, 0.68, 0.69, view_gain=0.46, conservative_bias=0.17),
    Method("visuotactile_probe", 0.51, 0.60, 0.57, 0.67, 0.70, 0.70, probe_rate=0.54, probe_accuracy=0.74, action_focus=0.53, cost_control=0.50, damage_control=0.63),
    Method("uncertainty_guided_probe", 0.55, 0.66, 0.61, 0.73, 0.73, 0.70, probe_rate=0.73, probe_accuracy=0.79, action_focus=0.31, cost_control=0.31, damage_control=0.48),
    Method("proposed_action_critical_interactive_depth", 0.54, 0.64, 0.59, 0.76, 0.74, 0.72, probe_rate=0.52, probe_accuracy=0.80, action_focus=0.84, cost_control=0.62, damage_control=0.57, conservative_bias=0.08),
    Method("oracle_depth_completion", 0.93, 0.94, 0.92, 0.93, 0.93, 0.91, probe_rate=0.18, probe_accuracy=0.96, action_focus=0.92, cost_control=0.92, damage_control=0.92, view_gain=0.38, is_oracle=True),
)

ABLATIONS: Sequence[Method] = (
    next(m for m in METHODS if m.name == "proposed_action_critical_interactive_depth"),
    replace(next(m for m in METHODS if m.name == "proposed_action_critical_interactive_depth"), name="minus_action_criticality", action_focus=0.24),
    replace(next(m for m in METHODS if m.name == "proposed_action_critical_interactive_depth"), name="minus_physical_probe", probe_rate=0.0, probe_accuracy=0.0, cost_control=0.0, damage_control=0.0),
    replace(next(m for m in METHODS if m.name == "proposed_action_critical_interactive_depth"), name="minus_uncertainty_calibration", uncertainty_calibration=0.36, boundary_sensitivity=0.58),
    replace(next(m for m in METHODS if m.name == "proposed_action_critical_interactive_depth"), name="minus_probe_cost_model", probe_rate=0.78, cost_control=0.24, damage_control=0.37),
    replace(next(m for m in METHODS if m.name == "proposed_action_critical_interactive_depth"), name="uncertainty_only_probe", probe_rate=0.72, action_focus=0.18, cost_control=0.34, damage_control=0.46),
    replace(next(m for m in METHODS if m.name == "proposed_action_critical_interactive_depth"), name="action_only_probe", uncertainty_calibration=0.39, action_focus=0.86, probe_accuracy=0.64),
)


METRIC_FIELDS = (
    "action_critical_rmse",
    "occluded_region_rmse",
    "collision_boundary_f1",
    "calibration_error",
    "probe_informativeness",
    "task_success",
    "collision_rate",
    "manipulation_failure_rate",
    "probe_cost",
    "probe_damage",
    "planning_regret_to_oracle",
    "probe_rate",
)


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def ci95(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    return 1.96 * statistics.stdev(values) / math.sqrt(len(values))


def rng_for(seed_id: int, task_idx: int, split_idx: int, method_idx: int, episode_idx: int) -> np.random.Generator:
    token = (
        BASE_SEED
        + seed_id * 1_000_003
        + task_idx * 19_997
        + split_idx * 8_191
        + method_idx * 521
        + episode_idx * 37
    )
    return np.random.default_rng(token)


def split_task(task: Task, split: Split) -> Dict[str, float]:
    return {
        "missing": clamp(task.missing + split.missing_delta, 0.0, 0.94),
        "occlusion": clamp(task.occlusion + split.occlusion_delta, 0.0, 0.94),
        "specular": clamp(task.specular + split.specular_delta, 0.0, 0.94),
        "clearance": clamp(task.clearance + split.tight_clearance_delta, 0.0, 0.96),
        "fragility": clamp(task.fragility + split.damage_delta, 0.0, 0.96),
        "probe_noise": clamp(split.probe_noise, 0.0, 0.94),
        "contact_need": task.contact_need,
        "clutter": task.clutter,
        "action_criticality": task.action_criticality,
    }


def f1_score(truth: np.ndarray, pred: np.ndarray) -> float:
    tp = float(np.sum(truth & pred))
    fp = float(np.sum(~truth & pred))
    fn = float(np.sum(truth & ~pred))
    if tp == 0.0 and fp == 0.0 and fn == 0.0:
        return 1.0
    if tp == 0.0:
        return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2.0 * precision * recall / (precision + recall)


def simulate_episode(method: Method, task: Task, split: Split, rng: np.random.Generator) -> Dict[str, float]:
    env = split_task(task, split)
    true_depth = rng.normal(0.52, 0.16, CELL_COUNT)
    true_depth = np.clip(true_depth, 0.08, 1.10)

    criticality = rng.beta(1.2 + 3.1 * env["action_criticality"], 2.1, CELL_COUNT)
    boundary_pressure = rng.beta(1.1 + 2.4 * env["clearance"], 2.0, CELL_COUNT)
    criticality = np.clip(0.72 * criticality + 0.28 * boundary_pressure, 0.0, 1.0)

    missing_mask = rng.random(CELL_COUNT) < env["missing"]
    occluded_mask = rng.random(CELL_COUNT) < env["occlusion"]
    specular_mask = rng.random(CELL_COUNT) < env["specular"]
    degraded_mask = missing_mask | occluded_mask | specular_mask
    if not np.any(degraded_mask):
        degraded_mask[rng.integers(0, CELL_COUNT)] = True

    base_sigma = (
        0.012
        + 0.070 * missing_mask.astype(float)
        + 0.060 * occluded_mask.astype(float)
        + 0.075 * specular_mask.astype(float)
        + 0.020 * env["clutter"]
        + rng.uniform(0.0, 0.010, CELL_COUNT)
    )
    baseline_sigma = base_sigma.copy()

    occlusion_gain = method.occlusion_recovery * occluded_mask.astype(float)
    specular_gain = method.specular_recovery * specular_mask.astype(float)
    passive_gain = method.passive_completion * (0.34 + 0.38 * degraded_mask.astype(float))
    passive_gain += 0.21 * occlusion_gain + 0.18 * specular_gain
    passive_gain = np.clip(passive_gain, 0.0, 0.82)

    view_gain = np.zeros(CELL_COUNT)
    if method.view_gain > 0.0:
        view_gain = method.view_gain * (0.52 * occluded_mask.astype(float) + 0.16 * missing_mask.astype(float))
        view_gain *= 1.0 - 0.28 * env["specular"]

    sigma_after_passive = baseline_sigma * (1.0 - np.clip(passive_gain + view_gain, 0.0, 0.88))
    sigma_after_passive = np.clip(sigma_after_passive, 0.004, None)

    probe_count = 0
    probe_damage_event = False
    probe_cost = 0.012 * method.view_gain * (0.4 + env["occlusion"])
    probe_info = 0.0
    sigma_after_probe = sigma_after_passive.copy()
    if method.probe_rate > 0.0:
        scene_uncertainty = float(np.mean(degraded_mask) + 0.45 * env["probe_noise"])
        expected_probe_rate = method.probe_rate * (0.37 + 0.45 * scene_uncertainty + 0.18 * env["action_criticality"])
        expected_probe_rate = clamp(expected_probe_rate, 0.0, 0.95)
        probe_count = int(np.clip(round(1 + 5 * expected_probe_rate + rng.normal(0.0, 0.8)), 0, 6))
        if probe_count > 0:
            uncertainty_score = sigma_after_passive / (np.max(sigma_after_passive) + 1e-9)
            target_score = method.action_focus * criticality + (1.0 - method.action_focus) * uncertainty_score
            target_score += 0.28 * degraded_mask.astype(float) + rng.normal(0.0, 0.025, CELL_COUNT)
            target_indices = np.argsort(target_score)[-probe_count:]
            contact_gain = 0.42 + 0.25 * env["contact_need"] + 0.18 * criticality[target_indices]
            noise_penalty = 0.34 * env["probe_noise"] + 0.16 * env["specular"]
            probe_gain = np.clip(method.probe_accuracy * contact_gain - noise_penalty, 0.0, 0.76)
            before = sigma_after_probe[target_indices].copy()
            sigma_after_probe[target_indices] = np.clip(before * (1.0 - probe_gain), 0.003, None)
            probe_info = float(np.mean(before - sigma_after_probe[target_indices]))
            probe_cost = (
                0.018 * probe_count
                * (1.0 + 0.62 * env["clearance"] + 0.36 * env["contact_need"])
                * (1.22 - method.cost_control)
            )
            damage_probability = (
                0.012 * probe_count
                + 0.030 * env["probe_noise"] * probe_count
                + 0.145 * env["fragility"] * env["contact_need"] * probe_count * (1.0 - method.damage_control)
            )
            probe_damage_event = bool(rng.random() < clamp(damage_probability, 0.0, 0.82))

    if method.is_oracle:
        sigma_after_probe = np.minimum(sigma_after_probe, 0.004 + 0.002 * degraded_mask.astype(float))
        probe_damage_event = False
        probe_cost *= 0.45
        probe_info = max(probe_info, float(np.mean(baseline_sigma - sigma_after_probe)))

    signed_error = rng.normal(0.0, sigma_after_probe)
    predicted_depth = true_depth + signed_error
    approach_depth = float(np.quantile(true_depth, 0.43 + 0.12 * env["clearance"]))
    margin = 0.045 + 0.060 * (1.0 - env["clearance"])
    true_boundary = np.abs(true_depth - approach_depth) < margin
    pred_boundary = np.abs(predicted_depth - approach_depth) < margin * (0.72 + 0.48 * method.boundary_sensitivity + method.conservative_bias)
    boundary_f1 = f1_score(true_boundary, pred_boundary)

    critical_threshold = float(np.quantile(criticality, 0.68))
    critical_mask = criticality >= critical_threshold
    action_critical_rmse = float(np.sqrt(np.mean((predicted_depth[critical_mask] - true_depth[critical_mask]) ** 2)))
    occluded_region_rmse = float(np.sqrt(np.mean((predicted_depth[degraded_mask] - true_depth[degraded_mask]) ** 2)))

    predicted_uncertainty = sigma_after_probe * (0.55 + 0.80 * method.uncertainty_calibration)
    calibration_coverage = float(np.mean(np.abs(signed_error) <= 1.64 * predicted_uncertainty))
    calibration_error = abs(calibration_coverage - 0.90)

    depth_quality = math.exp(-action_critical_rmse / 0.055)
    occlusion_quality = math.exp(-occluded_region_rmse / 0.068)
    calibration_bonus = 1.0 - clamp(calibration_error / 0.42)
    damage_penalty = 0.44 if probe_damage_event else 0.0
    contact_penalty = 0.16 * probe_cost * (0.6 + env["fragility"])
    difficulty = (
        0.33
        + 0.18 * env["clearance"]
        + 0.13 * env["occlusion"]
        + 0.12 * env["specular"]
        + 0.08 * env["missing"]
        + 0.09 * env["fragility"]
    )
    decision_score = (
        0.39 * depth_quality
        + 0.17 * occlusion_quality
        + 0.19 * boundary_f1
        + 0.09 * calibration_bonus
        + 0.13 * method.decision_quality
        + 0.05 * min(probe_info / 0.045, 1.0)
        - difficulty
        - contact_penalty
        - damage_penalty
        + rng.normal(0.0, 0.045)
    )
    success = float(decision_score > SUCCESS_THRESHOLD)

    collision_probability = (
        0.28 * (1.0 - boundary_f1) * env["clearance"]
        + 0.22 * action_critical_rmse / 0.10
        + 0.08 * env["occlusion"]
        - 0.08 * method.conservative_bias
        - 0.06 * method.boundary_sensitivity
    )
    collision = float((not success) and rng.random() < clamp(collision_probability, 0.0, 0.92))
    manipulation_failure = float((not success) and not collision)
    planning_regret = clamp(
        0.58 * action_critical_rmse / 0.10
        + 0.24 * (1.0 - boundary_f1)
        + 0.12 * probe_cost
        + (0.22 if probe_damage_event else 0.0)
        + 0.06 * manipulation_failure
        - (0.07 if success else 0.0),
        0.0,
        1.0,
    )

    return {
        "action_critical_rmse": action_critical_rmse,
        "occluded_region_rmse": occluded_region_rmse,
        "collision_boundary_f1": boundary_f1,
        "calibration_error": calibration_error,
        "probe_informativeness": probe_info,
        "task_success": success,
        "collision_rate": collision,
        "manipulation_failure_rate": manipulation_failure,
        "probe_cost": probe_cost,
        "probe_damage": float(probe_damage_event),
        "planning_regret_to_oracle": planning_regret,
        "probe_rate": float(probe_count > 0),
    }


def run_seed_task(method: Method, task: Task, split: Split, seed_id: int, task_idx: int, split_idx: int, method_idx: int, episodes: int) -> Dict[str, float]:
    accum: Dict[str, List[float]] = {name: [] for name in METRIC_FIELDS}
    for episode_idx in range(episodes):
        rng = rng_for(seed_id, task_idx, split_idx, method_idx, episode_idx)
        metrics = simulate_episode(method, task, split, rng)
        for name in METRIC_FIELDS:
            accum[name].append(metrics[name])
    return {name: float(np.mean(values)) for name, values in accum.items()}


def aggregate(rows: Sequence[Dict[str, str]], group_keys: Sequence[str], metrics: Iterable[str]) -> List[Dict[str, str]]:
    grouped: Dict[tuple, List[Dict[str, str]]] = {}
    for row in rows:
        key = tuple(row[k] for k in group_keys)
        grouped.setdefault(key, []).append(row)

    output: List[Dict[str, str]] = []
    for key, group in sorted(grouped.items()):
        out = {k: v for k, v in zip(group_keys, key)}
        out["groups"] = str(len(group))
        for metric in metrics:
            values = [float(r[metric]) for r in group]
            out[f"mean_{metric}"] = f"{statistics.mean(values):.5f}"
            out[f"ci95_{metric}"] = f"{ci95(values):.5f}"
        output.append(out)
    return output


def write_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def method_mean(rows: Sequence[Dict[str, str]], method: str, split: str, metric: str) -> float:
    values = [float(r[metric]) for r in rows if r["method"] == method and r["split"] == split]
    return statistics.mean(values)


def paired_diff(rows: Sequence[Dict[str, str]], method_a: str, method_b: str, split: str, metric: str) -> Dict[str, str]:
    index_b = {
        (r["task"], r["seed"]): float(r[metric])
        for r in rows
        if r["method"] == method_b and r["split"] == split
    }
    diffs: List[float] = []
    for row in rows:
        if row["method"] == method_a and row["split"] == split:
            key = (row["task"], row["seed"])
            diffs.append(float(row[metric]) - index_b[key])
    return {
        "method_a": method_a,
        "method_b": method_b,
        "split": split,
        "metric": metric,
        "mean_diff_a_minus_b": f"{statistics.mean(diffs):.5f}",
        "ci95_diff": f"{ci95(diffs):.5f}",
        "paired_groups": str(len(diffs)),
    }


def build_main_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for method_idx, method in enumerate(METHODS):
        for split_idx, split in enumerate(SPLITS):
            for task_idx, task in enumerate(TASKS):
                for seed_id in SEEDS:
                    metrics = run_seed_task(method, task, split, seed_id, task_idx, split_idx, method_idx, EPISODES_PER_SEED_TASK)
                    row: Dict[str, str] = {
                        "method": method.name,
                        "split": split.name,
                        "task": task.name,
                        "seed": str(seed_id),
                        "episodes": str(EPISODES_PER_SEED_TASK),
                    }
                    row.update({name: f"{metrics[name]:.6f}" for name in METRIC_FIELDS})
                    rows.append(row)
    return rows


def build_ablation_rows() -> List[Dict[str, str]]:
    combined = next(split for split in SPLITS if split.name == "combined_interactive_stress")
    rows: List[Dict[str, str]] = []
    for method_idx, method in enumerate(ABLATIONS):
        for task_idx, task in enumerate(TASKS):
            for seed_id in SEEDS:
                metrics = run_seed_task(method, task, combined, seed_id, task_idx, 99, method_idx + 40, EPISODES_PER_SEED_TASK)
                row: Dict[str, str] = {
                    "ablation": method.name,
                    "split": combined.name,
                    "task": task.name,
                    "seed": str(seed_id),
                    "episodes": str(EPISODES_PER_SEED_TASK),
                }
                row.update({name: f"{metrics[name]:.6f}" for name in METRIC_FIELDS})
                rows.append(row)
    return rows


def build_stress_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    selected = [
        "learned_depth_completion",
        "ensemble_depth_completion",
        "active_view_selection",
        "visuotactile_probe",
        "uncertainty_guided_probe",
        "proposed_action_critical_interactive_depth",
        "oracle_depth_completion",
    ]
    methods = [m for m in METHODS if m.name in selected]
    levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    for level_idx, level in enumerate(levels):
        split = Split(
            name=f"stress_{level:.1f}",
            missing_delta=0.28 * level,
            occlusion_delta=0.34 * level,
            specular_delta=0.32 * level,
            probe_noise=0.28 * level,
            tight_clearance_delta=0.32 * level,
            damage_delta=0.24 * level,
        )
        for method_idx, method in enumerate(methods):
            for task_idx, task in enumerate(TASKS):
                for seed_id in SEEDS:
                    metrics = run_seed_task(method, task, split, seed_id, task_idx, level_idx + 120, method_idx + 80, 44)
                    rows.append(
                        {
                            "stress_level": f"{level:.1f}",
                            "method": method.name,
                            "task": task.name,
                            "seed": str(seed_id),
                            "task_success": f"{metrics['task_success']:.6f}",
                            "action_critical_rmse": f"{metrics['action_critical_rmse']:.6f}",
                            "collision_rate": f"{metrics['collision_rate']:.6f}",
                            "probe_damage": f"{metrics['probe_damage']:.6f}",
                        }
                    )
    return rows


def write_latex_table(path: Path, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{tabular}{" + "l" * len(headers) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(headers) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            handle.write(" & ".join(row) + " \\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")


def build_tables(summary_rows: Sequence[Dict[str, str]], ablation_summary: Sequence[Dict[str, str]], pairwise_rows: Sequence[Dict[str, str]]) -> None:
    combined = [r for r in summary_rows if r["split"] == "combined_interactive_stress"]
    combined_rows = []
    for row in combined:
        combined_rows.append(
            [
                row["method"].replace("_", "\\_"),
                f"{float(row['mean_task_success']):.3f} $\\pm$ {float(row['ci95_task_success']):.3f}",
                f"{float(row['mean_action_critical_rmse']):.3f}",
                f"{float(row['mean_collision_rate']):.3f}",
                f"{float(row['mean_probe_cost']):.3f}",
                f"{float(row['mean_probe_damage']):.3f}",
            ]
        )
    write_latex_table(
        RESULTS / "combined_stress_table.tex",
        ["Method", "Success", "AC-RMSE", "Collision", "Probe cost", "Damage"],
        combined_rows,
    )

    ablation_rows = []
    for row in ablation_summary:
        ablation_rows.append(
            [
                row["ablation"].replace("_", "\\_"),
                f"{float(row['mean_task_success']):.3f} $\\pm$ {float(row['ci95_task_success']):.3f}",
                f"{float(row['mean_action_critical_rmse']):.3f}",
                f"{float(row['mean_probe_cost']):.3f}",
                f"{float(row['mean_probe_damage']):.3f}",
            ]
        )
    write_latex_table(
        RESULTS / "ablation_table.tex",
        ["Ablation", "Success", "AC-RMSE", "Probe cost", "Damage"],
        ablation_rows,
    )

    pairwise_lines = []
    for row in pairwise_rows:
        pairwise_lines.append(
            [
                row["metric"].replace("_", "\\_"),
                row["method_b"].replace("_", "\\_"),
                f"{float(row['mean_diff_a_minus_b']):.4f}",
                f"{float(row['ci95_diff']):.4f}",
            ]
        )
    write_latex_table(RESULTS / "pairwise_decision_table.tex", ["Metric", "Comparator", "Diff", "CI95"], pairwise_lines)


def plot_outputs(summary_rows: Sequence[Dict[str, str]], ablation_summary: Sequence[Dict[str, str]], stress_summary: Sequence[Dict[str, str]]) -> None:
    combined = [r for r in summary_rows if r["split"] == "combined_interactive_stress" and r["method"] != "oracle_depth_completion"]
    labels = [r["method"].replace("_", "\n") for r in combined]
    x = np.arange(len(labels))

    plt.figure(figsize=(12, 5))
    rmse = [float(r["mean_action_critical_rmse"]) for r in combined]
    occ = [float(r["mean_occluded_region_rmse"]) for r in combined]
    plt.bar(x - 0.18, rmse, 0.36, label="Action-critical RMSE")
    plt.bar(x + 0.18, occ, 0.36, label="Occluded-region RMSE")
    plt.xticks(x, labels, rotation=35, ha="right", fontsize=8)
    plt.ylabel("Depth RMSE (lower is better)")
    plt.title("Interactive depth quality under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_quality.png", dpi=190)
    plt.close()

    plt.figure(figsize=(12, 5))
    success = [float(r["mean_task_success"]) for r in combined]
    collisions = [float(r["mean_collision_rate"]) for r in combined]
    plt.bar(x - 0.18, success, 0.36, label="Task success")
    plt.bar(x + 0.18, collisions, 0.36, label="Collision rate")
    plt.xticks(x, labels, rotation=35, ha="right", fontsize=8)
    plt.ylim(0, 1)
    plt.ylabel("Rate")
    plt.title("Closed-loop manipulation outcomes under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_task_outcomes.png", dpi=190)
    plt.close()

    plt.figure(figsize=(8, 5))
    for row in combined:
        plt.scatter(float(row["mean_probe_cost"]), float(row["mean_planning_regret_to_oracle"]), s=80)
        plt.text(float(row["mean_probe_cost"]) + 0.002, float(row["mean_planning_regret_to_oracle"]), row["method"].replace("_", " "), fontsize=8)
    plt.xlabel("Mean probe/view cost")
    plt.ylabel("Planning regret to oracle")
    plt.title("Cost-regret tradeoff")
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_cost_regret.png", dpi=190)
    plt.close()

    plt.figure(figsize=(11, 5))
    labels = [r["ablation"].replace("_", "\n") for r in ablation_summary]
    x = np.arange(len(labels))
    plt.bar(x - 0.18, [float(r["mean_task_success"]) for r in ablation_summary], 0.36, label="Task success")
    plt.bar(x + 0.18, [float(r["mean_action_critical_rmse"]) for r in ablation_summary], 0.36, label="AC-RMSE")
    plt.xticks(x, labels, rotation=30, ha="right", fontsize=8)
    plt.title("Ablations under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_ablation.png", dpi=190)
    plt.close()

    plt.figure(figsize=(9, 5))
    for method in sorted({r["method"] for r in stress_summary if r["method"] != "oracle_depth_completion"}):
        rows = [r for r in stress_summary if r["method"] == method]
        rows.sort(key=lambda r: float(r["stress_level"]))
        plt.plot(
            [float(r["stress_level"]) for r in rows],
            [float(r["mean_task_success"]) for r in rows],
            marker="o",
            linewidth=2,
            label=method.replace("_", " "),
        )
    plt.xlabel("Combined stress level")
    plt.ylabel("Task success")
    plt.ylim(0, 1)
    plt.title("Stress sweep success curves")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_stress_sweep.png", dpi=190)
    plt.close()


def failure_cases(rows: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    combined = [r for r in rows if r["split"] == "combined_interactive_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_action_critical_interactive_depth"]
    by_task: Dict[str, List[Dict[str, str]]] = {}
    for row in proposed:
        by_task.setdefault(row["task"], []).append(row)
    output: List[Dict[str, str]] = []
    for task, task_rows in sorted(by_task.items()):
        output.append(
            {
                "case": task,
                "observed_success": f"{statistics.mean(float(r['task_success']) for r in task_rows):.4f}",
                "collision_rate": f"{statistics.mean(float(r['collision_rate']) for r in task_rows):.4f}",
                "probe_damage": f"{statistics.mean(float(r['probe_damage']) for r in task_rows):.4f}",
                "lesson": {
                    "leaf_occluded_fruit_grasp": "action-critical probing improves depth but fragile contact damage erases the closed-loop advantage",
                    "transparent_container_lift": "specular depth plus probe noise leaves uncertainty-guided and tactile baselines competitive",
                    "shelf_insertion_clearance": "tight clearance rewards conservative uncertainty baselines as much as targeted probing",
                    "occluded_bin_grasping": "active view selection recovers enough occluded geometry without physical contact cost",
                }[task],
            }
        )
    return output


def terminal_decision(rows: Sequence[Dict[str, str]], ablation_rows: Sequence[Dict[str, str]]) -> Dict[str, object]:
    split = "combined_interactive_stress"
    proposed = "proposed_action_critical_interactive_depth"
    non_oracle = [
        method.name
        for method in METHODS
        if not method.is_oracle and method.name != proposed
    ]
    success_means = {method: method_mean(rows, method, split, "task_success") for method in non_oracle}
    best_success_baseline = max(
        non_oracle,
        key=lambda method: (
            success_means[method],
            -method_mean(rows, method, split, "action_critical_rmse"),
            -method_mean(rows, method, split, "planning_regret_to_oracle"),
        ),
    )
    pairwise = [
        paired_diff(rows, proposed, best_success_baseline, split, "task_success"),
        paired_diff(rows, proposed, best_success_baseline, split, "action_critical_rmse"),
        paired_diff(rows, proposed, best_success_baseline, split, "collision_rate"),
        paired_diff(rows, proposed, best_success_baseline, split, "planning_regret_to_oracle"),
        paired_diff(rows, proposed, best_success_baseline, split, "probe_damage"),
    ]

    proposed_success = method_mean(rows, proposed, split, "task_success")
    proposed_rmse = method_mean(rows, proposed, split, "action_critical_rmse")
    proposed_collision = method_mean(rows, proposed, split, "collision_rate")
    proposed_damage = method_mean(rows, proposed, split, "probe_damage")
    proposed_cost = method_mean(rows, proposed, split, "probe_cost")
    best_success = success_means[best_success_baseline]

    rmse_means = {method: method_mean(rows, method, split, "action_critical_rmse") for method in non_oracle}
    best_rmse_baseline = min(rmse_means, key=rmse_means.get)
    best_rmse = rmse_means[best_rmse_baseline]

    ablation_success = {
        row["ablation"]: float(row["mean_task_success"])
        for row in aggregate(ablation_rows, ["ablation"], ["task_success"])
    }
    full_ablation_success = ablation_success[proposed]
    matched_ablations = [
        name
        for name, value in ablation_success.items()
        if name != proposed and value >= full_ablation_success - 0.015
    ]

    success_diff = float(pairwise[0]["mean_diff_a_minus_b"])
    success_ci = float(pairwise[0]["ci95_diff"])
    rmse_diff = float(paired_diff(rows, proposed, best_rmse_baseline, split, "action_critical_rmse")["mean_diff_a_minus_b"])
    collision_diff = float(pairwise[2]["mean_diff_a_minus_b"])
    regret_diff = float(pairwise[3]["mean_diff_a_minus_b"])

    clears_gate = (
        proposed_success > best_success
        and success_diff - success_ci > 0.0
        and proposed_rmse < best_rmse
        and rmse_diff < 0.0
        and (collision_diff < 0.0 or regret_diff < 0.0)
        and proposed_damage < 0.08
        and proposed_cost < 0.13
        and not matched_ablations
    )

    reason = (
        "Proposed action-critical probing does not clear the ICLR-main gate: it fails to significantly beat the strongest "
        f"non-oracle baseline ({best_success_baseline}) on combined-stress task success, and ablations/baselines remain competitive."
    )
    if clears_gate:
        reason = (
            "Proposed action-critical probing clears the local evidence gate against the strongest non-oracle baseline, but still needs "
            "hardware or high-fidelity simulator validation before an ICLR-main submission claim."
        )

    return {
        "status": "STRONG_REVISE" if clears_gate else "KILL_ARCHIVE",
        "reason": reason,
        "best_success_baseline": best_success_baseline,
        "best_rmse_baseline": best_rmse_baseline,
        "proposed_success": proposed_success,
        "best_success": best_success,
        "proposed_rmse": proposed_rmse,
        "best_rmse": best_rmse,
        "proposed_collision": proposed_collision,
        "proposed_damage": proposed_damage,
        "proposed_cost": proposed_cost,
        "matched_ablations": matched_ablations,
        "pairwise_rows": pairwise,
    }


def write_summary(decision: Dict[str, object], summary_rows: Sequence[Dict[str, str]], failure_rows: Sequence[Dict[str, str]]) -> None:
    combined = [r for r in summary_rows if r["split"] == "combined_interactive_stress"]
    combined_sorted = sorted(combined, key=lambda r: float(r["mean_task_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 94: interactive_depth_completion evidence audit\n")
        handle.write(f"Seeds: {len(SEEDS)}; tasks: {len(TASKS)}; splits: {len(SPLITS)}; episodes per seed/task: {EPISODES_PER_SEED_TASK}\n")
        handle.write("Evidence type: deterministic local active-perception manipulation simulator, not robot hardware validation.\n")
        handle.write(f"Terminal decision: {decision['status']}\n")
        handle.write(f"Reason: {decision['reason']}\n\n")
        handle.write("Combined-stress ranking by task success:\n")
        for row in combined_sorted:
            handle.write(
                f"- {row['method']}: success={float(row['mean_task_success']):.4f} +/- {float(row['ci95_task_success']):.4f}; "
                f"AC-RMSE={float(row['mean_action_critical_rmse']):.4f}; collision={float(row['mean_collision_rate']):.4f}; "
                f"damage={float(row['mean_probe_damage']):.4f}; regret={float(row['mean_planning_regret_to_oracle']):.4f}\n"
            )
        handle.write("\nGate details:\n")
        handle.write(f"- Strongest non-oracle success baseline: {decision['best_success_baseline']} ({decision['best_success']:.4f})\n")
        handle.write(f"- Proposed success: {decision['proposed_success']:.4f}\n")
        handle.write(f"- Best non-oracle AC-RMSE baseline: {decision['best_rmse_baseline']} ({decision['best_rmse']:.4f})\n")
        handle.write(f"- Proposed AC-RMSE: {decision['proposed_rmse']:.4f}\n")
        handle.write(f"- Proposed collision: {decision['proposed_collision']:.4f}; cost: {decision['proposed_cost']:.4f}; damage: {decision['proposed_damage']:.4f}\n")
        handle.write(f"- Ablations matching full within 0.015 success: {', '.join(decision['matched_ablations']) if decision['matched_ablations'] else 'none'}\n\n")
        handle.write("Failure cases:\n")
        for row in failure_rows:
            handle.write(
                f"- {row['case']}: success={row['observed_success']}, collision={row['collision_rate']}, damage={row['probe_damage']}; {row['lesson']}\n"
            )


def main() -> None:
    main_rows = build_main_rows()
    write_csv(RESULTS / "seed_task_metrics.csv", main_rows)

    summary_rows = aggregate(main_rows, ["method", "split"], METRIC_FIELDS)
    write_csv(RESULTS / "metrics.csv", summary_rows)

    per_task_rows = aggregate(main_rows, ["method", "split", "task"], METRIC_FIELDS)
    write_csv(RESULTS / "per_task_metrics.csv", per_task_rows)

    ablation_rows = build_ablation_rows()
    write_csv(RESULTS / "ablation_seed_task_metrics.csv", ablation_rows)
    ablation_summary = aggregate(ablation_rows, ["ablation"], METRIC_FIELDS)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_summary)

    stress_rows = build_stress_rows()
    write_csv(RESULTS / "stress_sweep_seed_task_metrics.csv", stress_rows)
    stress_summary = aggregate(stress_rows, ["stress_level", "method"], ("task_success", "action_critical_rmse", "collision_rate", "probe_damage"))
    write_csv(RESULTS / "stress_sweep.csv", stress_summary)
    write_csv(FIGURES / "stress_curve_data.csv", stress_summary)

    decision = terminal_decision(main_rows, ablation_rows)
    pairwise_rows = decision["pairwise_rows"]
    write_csv(RESULTS / "pairwise_stats.csv", pairwise_rows)

    failure_rows = failure_cases(main_rows)
    write_csv(RESULTS / "failure_cases.csv", failure_rows)

    build_tables(summary_rows, ablation_summary, pairwise_rows)
    plot_outputs(summary_rows, ablation_summary, stress_summary)
    write_summary(decision, summary_rows, failure_rows)

    print(f"Paper 94 evidence audit complete: {decision['status']}")
    print(RESULTS / "summary.txt")


if __name__ == "__main__":
    main()

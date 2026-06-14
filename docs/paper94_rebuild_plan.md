# Paper 94 Rebuild Plan: Interactive Depth Completion

Timestamp: 2026-06-14 15:46:00 +01:00

## Starting Point

Paper 94 is currently a v3 archive. The original bet is:

> Complete depth by physically probing where perception uncertainty matters to action.

The hostile prior-work pressure is strong: learned depth completion, Gaussian-splatting depth uncertainty, active perception and manipulation, visuo-tactile perception, active uncertainty reduction, active collision avoidance, and VLA active perception already cover much of the obvious space. The rebuild cannot claim novelty from "active probing" or "uncertainty." It must show that physical interaction completes action-critical depth better than passive completion, active view selection, uncertainty-guided completion, and visuo-tactile/probing baselines.

## Rebuilt Claim Under Test

The strongest defensible claim is:

> Interactive depth completion is useful when the robot probes only depth regions that are both uncertain and action-critical, producing enough local geometry improvement to change manipulation decisions without excessive probe cost or damage.

This is a local evidence audit, not hardware validation.

## Benchmark Design

I will replace the template success-rate generator with a deterministic active-perception manipulation benchmark. Each episode samples an object/scene with occlusion, specular/missing depth, collision risk, contact affordances, and action-critical geometry. Methods choose whether and where to complete depth, then execute a manipulation action using the completed depth map.

Tasks:

1. `occluded_bin_grasping`
2. `shelf_insertion_clearance`
3. `transparent_container_lift`
4. `leaf_occluded_fruit_grasp`

Splits:

1. `nominal_depth`
2. `missing_depth_shift`
3. `occlusion_shift`
4. `transparent_specular_shift`
5. `combined_interactive_stress`

## Methods To Compare

Strong baselines:

1. `raw_depth_policy`
2. `learned_depth_completion`
3. `gaussian_splat_uncertainty`
4. `ensemble_depth_completion`
5. `active_view_selection`
6. `visuotactile_probe`
7. `uncertainty_guided_probe`
8. `proposed_action_critical_interactive_depth`
9. `oracle_depth_completion`

## Metrics

Map/perception metrics:

1. Action-critical depth RMSE.
2. Occluded-region depth RMSE.
3. Collision-boundary F1.
4. Calibration error.
5. Probe informativeness.

Closed-loop metrics:

1. Task success.
2. Collision rate.
3. Grasp/insertion failure rate.
4. Probe cost.
5. Probe damage.
6. Planning regret to oracle.

Statistics:

1. Seven deterministic seeds.
2. Per-task and per-split means with 95 percent confidence intervals.
3. Paired seed/task comparison against the strongest non-oracle baseline.
4. Explicit terminal decision in `results/summary.txt`.

## Ablations

The full method must beat stripped variants:

1. `full_action_critical_interactive_depth`
2. `minus_action_criticality`
3. `minus_physical_probe`
4. `minus_uncertainty_calibration`
5. `minus_probe_cost_model`
6. `uncertainty_only_probe`
7. `action_only_probe`

If stripped variants match or beat full on task success or action-critical RMSE without a clear tradeoff, the mechanism is not supported.

## Stress Tests

Stress axes:

1. Missing depth rate.
2. Occlusion density.
3. Transparent/specular surface fraction.
4. Probe noise/damage risk.
5. Tight clearance / collision sensitivity.
6. Combined maximum stress.

The stress sweep must show whether the proposed action-critical probing remains useful when passive completion and active view selection degrade.

## Paper Rewrite Requirements

After experiments:

1. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative evidence audit.
2. Replace template claims with measured claims only.
3. Include tables for combined stress, ablations, and failure cases.
4. Include figures for depth quality, closed-loop outcomes, calibration/cost, ablations, and stress curves.
5. Update README, child status, claims, final audit, and submission-readiness docs.
6. Build only `C:/Users/wangz/Downloads/94.pdf`; do not copy anything to Desktop.
7. Commit and push to `https://github.com/Jason-Wang313/94_interactive_depth_completion`.

## Terminal Gate

Mark `STRONG_REVISE` only if all of the following are true:

1. `proposed_action_critical_interactive_depth` beats the strongest non-oracle baseline on combined-stress task success and action-critical depth RMSE.
2. It also reduces collision or planning regret without excessive probe cost/damage.
3. Core ablations degrade in expected directions.
4. Maximum-stress curves do not reverse in favor of learned completion, Gaussian-splat uncertainty, active view selection, visuo-tactile probing, or uncertainty-only probing.
5. The paper honestly states the evidence is local/simulated and not robot hardware validation.

Otherwise mark `KILL_ARCHIVE`. A physically interactive depth method that is matched by passive completion, active view selection, or generic uncertainty/tactile probing is not ICLR-main ready.

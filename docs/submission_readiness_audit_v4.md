# Submission Readiness Audit v4.1

Date: 2026-06-15

Paper: 94 Interactive Depth Completion

Terminal decision: KILL_ARCHIVE

## Commands Run

```powershell
python -m py_compile src\run_experiment.py
python src\run_experiment.py
```

Both commands completed. The full experiment output was redirected to `logs/94_interactive_depth_completion_continuation_rerun_20260615.log`.

## Evidence Coverage

- Aggregate metrics: 45 rows.
- Per-task metrics: 180 rows.
- Seed/task metrics: 1,260 rows.
- Pairwise gate rows: 5 rows.
- Ablation aggregate metrics: 7 rows.
- Ablation seed/task metrics: 196 rows.
- Stress sweep aggregates: 42 rows.
- Stress sweep seed/task metrics: 1,176 rows.
- Failure cases: 4 rows.
- Seeds: 0, 1, 2, 3, 4, 5, 6.
- Tasks: `occluded_bin_grasping`, `shelf_insertion_clearance`, `transparent_container_lift`, `leaf_occluded_fruit_grasp`.
- Splits: `nominal_depth`, `missing_depth_shift`, `occlusion_shift`, `transparent_specular_shift`, `combined_interactive_stress`.
- Methods: `raw_depth_policy`, `learned_depth_completion`, `gaussian_splat_uncertainty`, `ensemble_depth_completion`, `active_view_selection`, `visuotactile_probe`, `uncertainty_guided_probe`, `proposed_action_critical_interactive_depth`, `oracle_depth_completion`.

## Main Gate

On combined interactive stress, `proposed_action_critical_interactive_depth` reaches task success `0.51438 +/- 0.10648`, action-critical RMSE `0.05597`, collision rate `0.12302`, probe damage `0.15278`, and planning regret `0.44115`.

The strongest non-oracle baseline is `active_view_selection`, which reaches task success `0.79514 +/- 0.07968`, action-critical RMSE `0.04338`, collision rate `0.04762`, zero probe damage, and planning regret `0.26703`.

The paired proposed-minus-active-view differences over 28 task/seed groups are:

- Task success: `-0.28075 +/- 0.07128`.
- Action-critical RMSE: `+0.01259 +/- 0.00203`.
- Collision rate: `+0.07540 +/- 0.02471`.
- Planning regret: `+0.17412 +/- 0.02408`.
- Probe damage: `+0.15278 +/- 0.02223`.

## Contradictory Evidence

- Active view selection beats the proposed method on the main closed-loop task-success gate.
- Active view selection also beats the proposed method on action-critical RMSE.
- Physical probing introduces probe damage that active view selection avoids.
- Collision rate and planning regret both worsen for the proposed method.
- At maximum stress, active view selection remains ahead: success `0.78003` versus proposed `0.49432`.
- The evidence remains local/simulated and lacks robot hardware or accepted high-fidelity active-perception manipulation validation.

## Readiness Judgment

The paper is reproducible as a negative evidence audit. The proposed mechanism has some internal ablation support, but the external active-view baseline dominates the practical closed-loop objective. This is not submission-ready for ICLR main.

## Terminal Action

Keep `KILL_ARCHIVE`. Do not submit this paper to ICLR main in the current form.

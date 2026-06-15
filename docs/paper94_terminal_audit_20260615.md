# Paper 94 Terminal Audit

Date: 2026-06-15

Paper: `94_interactive_depth_completion`

Decision: `KILL_ARCHIVE`

## Reproduction

- `python -m py_compile src\run_experiment.py`: passed.
- `python src\run_experiment.py`: passed; log at `logs/94_interactive_depth_completion_continuation_rerun_20260615.log`.
- PDF target: `C:/Users/wangz/Downloads/94.pdf`.
- Visible Desktop copy: not allowed.

## Evidence Files

- `results/metrics.csv`: 45 rows.
- `results/per_task_metrics.csv`: 180 rows.
- `results/seed_task_metrics.csv`: 1,260 rows.
- `results/pairwise_stats.csv`: 5 rows.
- `results/ablation_metrics.csv`: 7 rows.
- `results/ablation_seed_task_metrics.csv`: 196 rows.
- `results/stress_sweep.csv`: 42 rows.
- `results/stress_sweep_seed_task_metrics.csv`: 1,176 rows.
- `results/failure_cases.csv`: 4 rows.
- `results/combined_stress_table.tex`: regenerated.
- `results/ablation_table.tex`: regenerated.
- `results/pairwise_decision_table.tex`: regenerated.

## Key Results

Combined interactive stress:

- `active_view_selection`: success `0.79514 +/- 0.07968`, action-critical RMSE `0.04338`, collision `0.04762`, damage `0.00000`, regret `0.26703`.
- `proposed_action_critical_interactive_depth`: success `0.51438 +/- 0.10648`, action-critical RMSE `0.05597`, collision `0.12302`, damage `0.15278`, regret `0.44115`.
- `ensemble_depth_completion`: success `0.48363`, action-critical RMSE `0.05969`, collision `0.13244`, regret `0.42031`.
- Paired success difference versus `active_view_selection`: `-0.28075 +/- 0.07128`.
- Paired action-critical RMSE difference: `+0.01259 +/- 0.00203`.
- Paired collision difference: `+0.07540 +/- 0.02471`.
- Paired regret difference: `+0.17412 +/- 0.02408`.
- Paired probe-damage difference: `+0.15278 +/- 0.02223`.

Ablation:

- Full proposed method: success `0.51885`, action-critical RMSE `0.05554`, collision `0.12054`, damage `0.14633`, regret `0.43689`.
- `minus_physical_probe`: success `0.39831`, zero probe damage, regret `0.47886`.
- `minus_probe_cost_model`: lower RMSE `0.05235` but worse damage `0.25893`.

Maximum stress:

- `active_view_selection`: success `0.78003`, action-critical RMSE `0.04351`, collision `0.04464`, damage `0.00000`.
- `proposed_action_critical_interactive_depth`: success `0.49432`, action-critical RMSE `0.05581`, collision `0.13068`, damage `0.13961`.

## Terminal Reason

The rerun verifies the v4 negative decision. Physical probing does not beat active view selection on task success, action-critical geometry, collision safety, planning regret, or damage. Internal ablation support cannot rescue an external-baseline failure. The only honest ICLR-main decision is `KILL_ARCHIVE`.

## PDF Verification

- Build command: two-pass `pdflatex -interaction=nonstopmode -halt-on-error main.tex`.
- Canonical PDF: `C:/Users/wangz/Downloads/94.pdf`.
- PDF SHA256: `78E7BB88FE7E967D7ABE335837FA1247ACCCEB5730B3A2FD382DC3DE8393256F`.
- PDF size: 539,854 bytes.
- LaTeX log scan: no document warnings/errors requiring action after the second pass.
- Desktop copy: absent.

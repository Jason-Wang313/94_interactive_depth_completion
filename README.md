# 94 Interactive Depth Completion

Submission-hardening version: v4.1 rerun audit

Terminal decision: KILL_ARCHIVE for ICLR main conference.

This repository is a negative evidence audit for the generated robotics idea:

> Complete depth by physically probing where perception uncertainty matters to action.

The rebuilt benchmark tests the strongest defensible version of the idea: action-critical probing should improve the local depth cells that matter to manipulation, and that improvement should translate into better closed-loop outcomes than passive completion, Gaussian/ensemble uncertainty, active view selection, visuo-tactile probing, and uncertainty-guided probing.

It does not clear that bar. Under combined interactive stress, active view selection is the strongest non-oracle baseline:

The 2026-06-15 continuation rerun reproduced the same terminal decision: active view selection remains stronger than action-critical physical probing on success, action-critical RMSE, collisions, regret, and damage.

| Method | Task success | Action-critical RMSE | Collision | Probe damage |
| --- | ---: | ---: | ---: | ---: |
| active_view_selection | 0.795 +/- 0.080 | 0.043 | 0.048 | 0.000 |
| proposed_action_critical_interactive_depth | 0.514 +/- 0.106 | 0.056 | 0.123 | 0.153 |

Paired comparison against active view selection over 28 task/seed groups:

- Task success diff: -0.28075 +/- 0.07128.
- Action-critical RMSE diff: +0.01259 +/- 0.00203.
- Collision-rate diff: +0.07540 +/- 0.02471.
- Planning-regret diff: +0.17412 +/- 0.02408.
- Probe-damage diff: +0.15278 +/- 0.02223.

The paper is therefore archived rather than submitted. The useful artifact is the reproducible negative benchmark and failure analysis, not an ICLR-main claim.

## Reproduce

```powershell
python src\run_experiment.py
```

The script writes:

- `results/metrics.csv`
- `results/per_task_metrics.csv`
- `results/seed_task_metrics.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/pairwise_stats.csv`
- `results/failure_cases.csv`
- `figures/interactive_depth_*.png`

## Rebuild Archive PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/94.pdf`

No PDF should be copied to the visible Desktop.

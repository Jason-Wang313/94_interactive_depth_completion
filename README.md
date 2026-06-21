# 94 Interactive Depth Completion

Expanded submission-audit version: v5, rebuilt on 2026-06-22.

Terminal decision: KILL_ARCHIVE for ICLR main conference.

This repository is a rigorous negative evidence audit for the generated robotics idea:

> Complete depth by physically probing where perception uncertainty matters to action.

The v5 rebuild tests the strongest CPU-only version of the idea: risk-aware action-critical physical probing should improve the depth cells that matter to manipulation and should convert that map improvement into better closed-loop behavior than passive completion, uncertainty baselines, active/next-best-view perception, tactile probing, diffusion/foundation priors, robust clearance MPC, and the previous v4 interactive-depth method.

It does not clear that bar. The method under audit, `risk_aware_action_critical_depth_probe_v5`, improves over v4, but the hard aggregate is still dominated by active view selection and robust clearance planning once collision, probe damage, regret, utility, and fixed-risk coverage are counted.

## v5 Evidence Digest

- 10 seeds.
- 6 manipulation tasks.
- 8 distribution splits.
- 14 methods including oracle.
- 215,040 main rollout rows.
- 15,360 dataset rows.
- 76,800 ablation rollout rows.
- 604,800 stress-sweep raw rows.
- 69,120 fixed-risk raw rows.
- 24 indexed negative cases.
- 25-page ICLR-style PDF with bright boxed clickable citations.

## Hard-Aggregate Result

| Method | Task success | AC-RMSE | Collision | Probe damage | Regret | Utility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| active_view_selection | 0.76693 | 0.03623 | 0.17344 | 0.00156 | 0.32102 | 0.36148 |
| robust_clearance_mpc | 0.65703 | 0.08903 | 0.10938 | 0.00130 | 0.41091 | 0.24304 |
| action_critical_interactive_depth_v4 | 0.46198 | 0.05925 | 0.23620 | 0.08906 | 0.52953 | -0.25187 |
| risk_aware_action_critical_depth_probe_v5 | 0.60885 | 0.05641 | 0.20547 | 0.07682 | 0.43869 | 0.01034 |

The v5 method improves on v4 but loses to active view selection on success, action-critical RMSE, collision, damage, regret, and robust utility. It also loses to robust clearance MPC on safety and utility tradeoffs.

## Gate Vector

- `success_gate=False`
- `active_view_gate=False`
- `depth_gate=False`
- `safety_gate=False`
- `calibration_gate=True`
- `utility_gate=False`
- `ablation_gate=False`
- `stress_gate=False`
- `fixed_risk_gate=False`
- `scope_gate=False`

At fixed-risk budget 0.05, v5 has zero accepted coverage on both hard splits. That is not deployable evidence.

## Canonical Artifacts

- Downloads PDF: `C:/Users/wangz/Downloads/94.pdf`
- PDF SHA256: `122B4E1F84A7BBA741DC56FEB2F26A2C001F25D986880057D18D7AB796BF71F3`
- Public repo: `https://github.com/Jason-Wang313/94_interactive_depth_completion`
- Raw stress file is local and ignored: `results/stress_sweep_raw.csv`
- Tracked compressed stress artifact: `results/stress_sweep_raw.csv.gz`
- Stress artifact manifest: `results/STRESS_SWEEP_RAW_MANIFEST.md`

No PDF should be copied to the visible Desktop.

## Reproduce

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item paper\main.pdf C:\Users\wangz\Downloads\94.pdf -Force
python scripts\validate_submission_artifacts.py
```

The validator checks row counts, gate tokens, LaTeX health, 25+ pages, citation annotations, the Downloads-only PDF target, and absence of a Desktop PDF leak.

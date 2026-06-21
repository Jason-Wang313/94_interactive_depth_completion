# Final Audit

1. Chosen thesis: Interactive Depth Completion tests whether a robot should physically probe depth regions where perception uncertainty matters to action.
2. ICLR-main decision: KILL_ARCHIVE.
3. Submission-hardening version: v5 expanded audit.
4. Last update: 2026-06-22 06:06 Asia/Shanghai.
5. Evidence: deterministic local active-perception manipulation benchmark with 10 seeds, 6 tasks, 8 splits, 14 methods, 215,040 main rollout rows, 76,800 ablation rollout rows, 604,800 stress rows, 69,120 fixed-risk rows, paired confidence intervals, and 24 negative cases.
6. Strongest non-oracle hard-success baseline: active_view_selection.
7. Hard-aggregate evidence: active view selection reaches task success 0.76693; v5 reaches 0.60885.
8. Paired hard-aggregate result vs active view selection: success lower95 -0.18224, action-critical RMSE upper95 +0.02094, planning-regret upper95 +0.13293, robust-utility lower95 -0.40092.
9. Main failure mode: physical probing improves over v4 but introduces contact risk, damage, collision exposure, and utility loss relative to non-contact active view selection and robust clearance planning.
10. Gate vector: success false, active-view false, depth false, safety false, calibration true, utility false, ablation false, stress false, fixed-risk false, scope false.
11. Reproducibility: `python src/run_experiment.py`, `python scripts/generate_manuscript.py`, LaTeX build, and `python scripts/validate_submission_artifacts.py` regenerate and validate the artifacts.
12. Public packaging: `results/stress_sweep_raw.csv.gz` is tracked with manifest; raw `results/stress_sweep_raw.csv` remains local and ignored because it exceeds GitHub's hard file-size limit.
13. Claim-validity status: ICLR-main claim killed; archive retained as a rigorous negative evidence report.
14. Exact Downloads PDF path: `C:/Users/wangz/Downloads/94.pdf`.
15. PDF SHA256: `122B4E1F84A7BBA741DC56FEB2F26A2C001F25D986880057D18D7AB796BF71F3`.
16. GitHub URL: https://github.com/Jason-Wang313/94_interactive_depth_completion.
17. Confirmation: no visible Desktop PDF copy was requested or made.

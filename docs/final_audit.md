# Final Audit

1. Chosen thesis: Interactive Depth Completion tests whether a robot should physically probe depth regions where perception uncertainty matters to action.
2. ICLR-main decision: KILL_ARCHIVE.
3. Submission-hardening version: v4.
4. Last update: 2026-06-14 16:13:24 +01:00.
5. Evidence: deterministic local active-perception manipulation benchmark with seven seeds, four tasks, five splits, nine methods, ablations, stress sweeps, paired confidence intervals, and failure cases.
6. Strongest non-oracle baseline: active_view_selection.
7. Combined-stress evidence: active view selection reaches 0.795 +/- 0.080 task success; the proposed method reaches 0.514 +/- 0.106.
8. Paired task/seed result: proposed minus active view selection is -0.28075 +/- 0.07128 for success, +0.01259 +/- 0.00203 for action-critical RMSE, +0.07540 +/- 0.02471 for collisions, +0.17412 +/- 0.02408 for regret, and +0.15278 +/- 0.02223 for probe damage.
9. Main failure mode: physical probing improves some local geometry but introduces contact cost and damage; active view selection recovers enough occluded geometry without contact.
10. Closest hostile prior work: see `docs/hostile_prior_work.md`, `docs/hostile_prior_work_100_cards.csv`, and `docs/hostile_reviewer_response.md`.
11. Reproducibility: `python src/run_experiment.py` regenerates the CSVs, figures, LaTeX tables, and terminal decision.
12. Claim-validity status: ICLR-main claim killed; archive retained as a negative evidence report.
13. Exact Downloads PDF path: `C:/Users/wangz/Downloads/94.pdf`.
14. GitHub URL: https://github.com/Jason-Wang313/94_interactive_depth_completion.
15. Confirmation: no visible Desktop PDF copy was requested or made.

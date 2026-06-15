# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Replaced the toy experiment with seven-seed metrics, stronger baselines, ablations, stress tests, and negative cases.
- Narrowed claims to synthetic diagnostic evidence.
- Recompiled canonical PDF at `C:/Users/wangz/Downloads/94.pdf`.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied the stricter ICLR-main-conference standard.
- Re-read local paper, docs, experiments, prior-work artifacts, PDF state, and repo state.
- Determined that missing real-robot/high-fidelity evidence, template-generated experiments, and unresolved novelty threats were not recoverable from local artifacts.
- Recompiled the canonical PDF with `Submission-hardening version: v3`.
- Terminal decision: KILL_ARCHIVE.

## v4 - Paper-Specific Evidence Audit

- Added a concrete Paper 94 rebuild plan before experiments.
- Replaced the generic probability scaffold with a deterministic interactive-depth manipulation simulator.
- Tested four tasks, five splits, nine methods, seven seeds, ablations, stress sweeps, paired comparisons, and failure cases.
- Generated paper-specific figures and LaTeX tables.
- Found that active view selection dominates proposed physical probing under combined stress.
- Terminal decision remains: KILL_ARCHIVE.

## v4.1 - 2026-06-15 Rerun Audit

- Re-ran `python -m py_compile src\run_experiment.py` and the full `python src\run_experiment.py`.
- Confirmed active view selection remains the strongest non-oracle combined-stress baseline.
- Confirmed proposed-minus-active-view task-success difference is `-0.28075 +/- 0.07128`.
- Confirmed proposed action-critical RMSE, collision rate, planning regret, and probe damage are all worse than active view selection.
- Updated child docs and paper source to keep the v4 KILL_ARCHIVE decision evidence-bound.

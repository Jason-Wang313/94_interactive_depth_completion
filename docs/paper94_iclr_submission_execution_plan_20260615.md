# Paper 94 ICLR-Main Submission Execution Plan

Date: 2026-06-15
Paper: `94_interactive_depth_completion`
Repository: `https://github.com/Jason-Wang313/94_interactive_depth_completion`

## Goal

Rebuild and audit Paper 94 under an ICLR-main submission standard, while refusing to upgrade the paper unless action-critical physical probing beats strong non-contact and uncertainty baselines on the closed-loop manipulation objective, not merely on a local depth-completion intuition.

## Current Starting State

- The repository is on `main` at commit `46eeef668fd02733165bdc7416e81a92f16229a7`.
- The existing v4 audit is terminally negative: `KILL_ARCHIVE`.
- Existing evidence reports that `active_view_selection` dominates the proposed method under combined interactive stress.
- Existing evidence reports worse proposed task success, action-critical RMSE, collision rate, planning regret, and probe damage.
- `C:/Users/wangz/Downloads/94.pdf` exists.
- `C:/Users/wangz/Desktop/94.pdf` does not exist and must not be created.

## Execution Steps

1. Re-run `python -m py_compile src/run_experiment.py`.
2. Re-run `python src/run_experiment.py` and save the full console transcript to the batch log directory.
3. Verify that the rerun regenerates aggregate metrics, per-task metrics, seed/task metrics, ablations, stress sweeps, pairwise stats, failure cases, LaTeX tables, and figures.
4. Independently audit the result CSVs with pandas instead of trusting the prose summary.
5. Compare `proposed_action_critical_interactive_depth` against the strongest non-oracle baselines on:
   - combined-stress task success;
   - action-critical depth RMSE;
   - occluded-region RMSE;
   - collision-boundary F1;
   - collision rate;
   - manipulation failure rate;
   - probe cost;
   - probe damage;
   - planning regret to oracle;
   - maximum-stress robustness.
6. Check whether internal ablations isolate the action-critical physical-probing mechanism.
7. Update the paper and documentation with measured claims only.
8. Rebuild `paper/main.pdf` with `pdflatex` and copy the final artifact only to `C:/Users/wangz/Downloads/94.pdf`.
9. Scan the LaTeX log for real warnings/errors and fix recoverable typesetting problems.
10. Update the root batch ledgers after the child repo is correct.
11. Commit, push, and verify the public GitHub repository.
12. Confirm the child git tree is clean, `origin/main` matches local `HEAD`, the numbered PDF exists in Downloads, and no Desktop PDF exists.

## Submission-Readiness Gates

Paper 94 may be marked `STRONG_REVISE` only if all gates pass:

1. The proposed action-critical physical probing method beats the strongest non-oracle baseline on combined-stress task success.
2. It also beats or clearly matches the strongest baseline on action-critical depth RMSE.
3. It lowers collisions or planning regret without excessive probe cost.
4. It does not introduce unacceptable probe damage.
5. Core ablations degrade in the expected directions.
6. Maximum-stress curves do not reverse in favor of active view selection, learned completion, ensemble completion, Gaussian uncertainty, visuo-tactile probing, or uncertainty-guided probing.
7. The paper clearly labels the evidence as local simulated evidence and does not imply robot hardware validation.

If active view selection remains stronger on task success, RMSE, collision safety, regret, or damage, the terminal decision remains `KILL_ARCHIVE`.

## Expected Honest Outcome

The prior v4 evidence already suggests a likely `KILL_ARCHIVE` decision because active view selection recovers enough geometry without contact damage and dominates the proposed method on the main closed-loop gates. The continuation rerun must verify that result from regenerated evidence rather than preserving it by inertia.

## Deliverables

- Updated rerun log in `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/`.
- Updated Paper 94 result CSVs, LaTeX tables, and figures if regenerated content changes.
- Updated child documentation and paper source with the rerun audit.
- Final numbered PDF at `C:/Users/wangz/Downloads/94.pdf` only.
- Updated root ledgers through Paper 94.
- Public GitHub repo pushed and verified clean.

# ICLR Main Gate

Paper: 94 interactive_depth_completion

Submission-hardening version: v4

Gate verdict: KILL_ARCHIVE

Evidence digest: v4 deterministic active-perception benchmark, seven seeds, four tasks, five splits, nine methods, ablations, stress sweep, paired confidence intervals, and failure cases.

Fatal blockers:

- The proposed method is dominated by active view selection under combined interactive stress.
- Proposed task success is 0.514 +/- 0.106 vs 0.795 +/- 0.080 for active view selection.
- Proposed action-critical RMSE is 0.056 vs 0.043 for active view selection.
- Proposed collision rate is 0.123 vs 0.048 for active view selection.
- Proposed probe damage is 0.153 vs 0.000 for active view selection.
- The evidence is still local simulation rather than real robot or high-fidelity simulator validation.

The only honest main-conference-safe decision is to archive rather than overclaim.

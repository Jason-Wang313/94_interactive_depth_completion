# Experiment Rigor Checklist

## Completed In v4

- [x] Concrete pre-execution rebuild plan.
- [x] Hostile prior-work pressure from the shared robotics literature pool.
- [x] Paper-specific active-perception manipulation benchmark.
- [x] Four tasks: occluded bin grasping, shelf insertion, transparent container lifting, and leaf-occluded fruit grasping.
- [x] Five splits: nominal, missing-depth shift, occlusion shift, transparent/specular shift, and combined interactive stress.
- [x] Nine methods including raw depth, learned completion, Gaussian-splat uncertainty, ensemble completion, active view selection, visuo-tactile probing, uncertainty-guided probing, proposed action-critical probing, and oracle depth.
- [x] Seven deterministic seeds.
- [x] Per-task/per-seed metrics.
- [x] 95 percent confidence intervals.
- [x] Paired task/seed comparison against the strongest non-oracle baseline.
- [x] Ablations for action criticality, physical probing, uncertainty calibration, probe cost model, uncertainty-only probing, and action-only probing.
- [x] Stress sweep across combined missing depth, occlusion, specularity, probe noise, clearance, and damage risk.
- [x] Failure-case analysis.
- [x] Numeric hygiene audit: no NaN or Inf values in generated CSVs.
- [x] Paper-specific figures and LaTeX tables.

## Still Missing For ICLR Main

- [ ] Real robot validation.
- [ ] High-fidelity simulator benchmark.
- [ ] Trained model checkpoints.
- [ ] Implemented real external competing systems.
- [ ] Full manual related-work synthesis beyond the local hostile pool.
- [ ] Hardware videos or qualitative rollouts.

Decision: KILL_ARCHIVE after v4.1 rerun. The local benchmark is rigorous enough to falsify the generated claim, not enough to revive it as an ICLR-main submission.

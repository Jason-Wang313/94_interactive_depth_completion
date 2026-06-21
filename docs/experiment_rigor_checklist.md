# Experiment Rigor Checklist

## Completed In v5

- [x] Frozen pre-execution plan: `docs/paper94_expanded_submission_plan_20260622.md`.
- [x] Hostile prior-work pressure from the shared robotics literature pool.
- [x] Paper-specific interactive-depth manipulation benchmark.
- [x] Six tasks: occluded bin grasping, shelf insertion, transparent container lifting, leaf-occluded fruit grasping, drawer slot alignment, and deformable bag lifting.
- [x] Eight splits: nominal depth, missing-depth shift, occlusion shift, transparent/specular shift, probe-noise shift, tight-clearance shift, low-signal depth stress, and combined interactive stress.
- [x] Fourteen methods including raw depth, learned completion, Gaussian uncertainty, ensemble completion, active view selection, next-best-view planning, visuotactile probing, uncertainty-guided probing, diffusion depth policy, foundation prior, robust clearance MPC, v4, v5, and oracle.
- [x] Ten deterministic seeds.
- [x] Main rollout table with 215,040 rows.
- [x] Dataset factor table with 15,360 rows.
- [x] Seed metrics, aggregate metrics, and paired confidence intervals.
- [x] Ablation protocol with 76,800 rollout rows and 10 ablations/variants.
- [x] Stress sweep with 604,800 raw rows.
- [x] Fixed-risk deployment sweep with 69,120 raw rows.
- [x] 24 indexed negative cases.
- [x] Numeric hygiene through validator row-count checks.
- [x] Paper-specific figures and 25-page ICLR-style PDF.
- [x] Bright boxed clickable citations and 180-entry bibliography.
- [x] Public compressed stress artifact plus manifest.

## Still Missing For ICLR Main

- [ ] Real robot validation.
- [ ] Accepted high-fidelity simulator benchmark.
- [ ] Trained model checkpoints.
- [ ] Integrated external baseline codebases.
- [ ] Hardware videos or qualitative rollouts.
- [ ] Independent reproduction.
- [ ] A gate-clearing method that beats active view selection and robust clearance MPC under the frozen criteria.

Decision: KILL_ARCHIVE after v5. The local benchmark is rigorous enough to falsify the generated claim, not enough to revive it as an ICLR-main submission.

# Reproducibility Checklist

## What Reproduces

- [x] `python src/run_experiment.py`
- [x] `python scripts/generate_manuscript.py`
- [x] `python scripts/validate_submission_artifacts.py`
- [x] `results/rollouts.csv`
- [x] `results/dataset_summary.csv`
- [x] `results/raw_seed_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/hard_aggregate_seed_metrics.csv`
- [x] `results/hard_aggregate_metrics.csv`
- [x] `results/hard_aggregate_pairwise_stats.csv`
- [x] `results/ablation_rollouts.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/ablation_metric_long.csv`
- [x] `results/stress_sweep_raw.csv` locally.
- [x] `results/stress_sweep_raw.csv.gz` publicly.
- [x] `results/STRESS_SWEEP_RAW_MANIFEST.md`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/stress_sweep_metric_long.csv`
- [x] `results/fixed_risk_raw.csv`
- [x] `results/fixed_risk_seed_metrics.csv`
- [x] `results/fixed_risk_metrics.csv`
- [x] `results/fixed_risk_pairwise.csv`
- [x] `results/negative_cases.csv`
- [x] `figures/interactive_depth_hard_success_regret_v5.png`
- [x] `figures/interactive_depth_map_metrics_v5.png`
- [x] `figures/interactive_depth_ablation_v5.png`
- [x] `figures/interactive_depth_stress_sweep_v5.png`
- [x] `figures/interactive_depth_fixed_risk_v5.png`
- [x] `figures/interactive_depth_pareto_v5.png`
- [x] `paper/main.tex`
- [x] `paper/references.bib`
- [x] Canonical PDF target: `C:/Users/wangz/Downloads/94.pdf`
- [x] PDF SHA256: `122B4E1F84A7BBA741DC56FEB2F26A2C001F25D986880057D18D7AB796BF71F3`

## Validation

- [x] Local raw-CSV validation passed.
- [x] Public `.csv.gz` fallback validation passed.
- [x] Visual PDF QA passed on representative pages.
- [x] No `C:/Users/wangz/Desktop/94.pdf` leak.

## What Does Not Reproduce

- [ ] Real robot results.
- [ ] High-fidelity simulator runs.
- [ ] Trained model checkpoints.
- [ ] Integrated external baseline codebases.
- [ ] Hardware videos.

This is reproducible as a negative evidence audit and archive memo, not as an ICLR-main robotics system paper.

# Stress Sweep Raw Artifact Manifest

Paper 94 generates a large stress-sweep rollout table. The public repository tracks the compressed artifact so GitHub accepts the repo while preserving the raw evidence.

- Raw local file: `results/stress_sweep_raw.csv`
- Raw row count: `604800`
- Raw size: `177619570` bytes
- Raw SHA256: `0A70EED2646524997EFF2378A2FAA140AE530C26A29CB88ED62B7107AEEA0638`
- Tracked compressed file: `results/stress_sweep_raw.csv.gz`
- Compressed size: `57206823` bytes
- Compressed SHA256: `44A2260BF8CEE95EA5D1B5F2898FAD4662C42A4D3AA0C7916E06D1B25CA0419E`

To reproduce the exact public artifact after running `python src/run_experiment.py`, gzip `results/stress_sweep_raw.csv` and compare the row count plus hashes above. The submission validator accepts either the uncompressed local CSV or the compressed public artifact.

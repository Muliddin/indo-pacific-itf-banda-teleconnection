# Phase 3C v1.1 – Sequential/Single-Mediator Decomposition & Collinearity Diagnostics

This package diagnoses why indirect effects can appear in single-mediator models but attenuate in the parallel Qout+Ekman model.

## Analyses
- single-mediator Qout models;
- single-mediator full-Ekman models;
- 12-month moving-block bootstrap;
- mediator correlation matrix;
- two-predictor VIF;
- commonality/shared-variance decomposition after controlling the climate driver and the other climate index;
- comparison of single versus parallel indirect effects;
- diagnostic classification: independent mediation, shared-variance/suppression, mixed, or no robust mediation.

## Important
This package **does not lower or change** the Phase 3C v1.0 mediation thresholds. Its purpose is explanatory diagnosis.

## Run
```bash
cd ~/Downloads/Phase3C_v1.1_SingleMediator_CollinearityDiagnostics
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_phase3c_v1.1.sh
```

Default input:
`../Phase3C_Parallel_Mediation_PathAnalysis_v1.0`

## Main outputs
- `reports/single_mediator_models.csv`
- `reports/mediator_correlation_matrix.csv`
- `reports/mediator_vif_diagnostics.csv`
- `reports/commonality_shared_variance.csv`
- `reports/single_vs_parallel_indirect_comparison.csv`
- `reports/mediation_collinearity_diagnostic_classification.csv`
- `reports/phase3c_v11_summary.json`
- `figures/single_vs_parallel_indirect_effects.png`
- `figures/commonality_decomposition.png`

### Interpretation
A significant single-mediator indirect effect that substantially attenuates and loses significance in the parallel model is flagged as evidence consistent with overlapping/shared mediator variance or suppression. This is not proof that either mediator is causal.

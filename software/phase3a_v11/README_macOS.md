# Phase3A_v1.1_LagRobustness

Patch layer for Phase3A v1.0. It does not overwrite Stage 1 results.

## Outputs
- positive-lag-only (0..+12) ordinary and partial correlations
- AR(1)-adjusted p-values for partial correlations
- Benjamini-Hochberg FDR for ordinary and partial correlation families
- four preprocessing sensitivity combinations
- Niño3.4 and DMI lag heatmaps
- `stage1_freeze_decision.csv`

## Primary interpretation convention
Positive lag means climate index leads ITF response. Negative lags from v1.0 are diagnostic only and are not used for driver→response freeze decisions.

## Preprocessing sensitivity matrix
1. raw index × detrended ITF anomaly
2. raw index × undetrended ITF anomaly
3. detrended index × detrended ITF anomaly
4. detrended index × undetrended ITF anomaly

## Automatic freeze rule
A primary ordinary-correlation pathway is marked FREEZE only when:
- best positive-lag ordinary correlation passes pair-wise FDR at alpha=0.05;
- |r| >= 0.15;
- at least 75% of preprocessing variants agree on sign;
- spread of best lags across preprocessing variants <= 4 months.

Partial-correlation significance is reported as a separate robustness diagnostic and does not automatically veto FREEZE; if it fails, the pathway should be interpreted as potentially sharing ENSO–IOD covariance.

## Run
```bash
cd ~/Downloads/Phase3A_v1.1_LagRobustness
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash run_phase3a_v1.1.sh
```

If the Phase3A v1.0 folder differs, edit `config/lag_robustness_config.yaml`.

Key files:
- `reports/positive_lag_ENSO_IOD_to_ITF.csv`
- `reports/positive_lag_best_lags.csv`
- `reports/preprocessing_sensitivity_all_lags.csv`
- `reports/preprocessing_sensitivity_best_lags.csv`
- `figures/heatmap_nino34_r.png`
- `figures/heatmap_nino34_partial_r.png`
- `figures/heatmap_dmi_r.png`
- `figures/heatmap_dmi_partial_r.png`
- `reports/stage1_freeze_decision.csv`

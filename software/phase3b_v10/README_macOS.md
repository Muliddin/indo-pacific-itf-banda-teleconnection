# Phase3B_ITF_OHC_Upwelling_Coupling_v1.0

Purpose: quantify **ITF transport → Banda Sea OHC/upwelling coupling** before mediation/pathway analysis.

## Core analyses
- lagged ITF→Banda correlation, 0..+12 months;
- partial coupling controlling Niño3.4 and DMI simultaneously;
- AR(1)-adjusted effective sample size;
- pair-wise and global Benjamini-Hochberg FDR;
- seasonal-year stratification;
- four detrending combinations;
- canonical/conditional/review classification;
- ordinary and partial-coupling heatmaps.

## Predictors
Makassar, Lombok, Ombai, Timor, and total-major-outflow transport anomalies.

## Responses
OHC300, OHC700, SST, MLD, wind stress, wind-stress curl, and current Ekman-pumping proxy anomalies.

## Run on macOS
```bash
cd ~/Downloads/Phase3B_ITF_OHC_Upwelling_Coupling_v1.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_phase3b.sh
```

Default inputs:
- `../Phase3A_Teleconnection_Analysis_v1.0`
- `../Phase3A_Stage2_v1.1_EventAware_SeasonalRobustness`

## Main outputs
- `data/processed/coupling_master_1993_2025.csv`
- `reports/lagged_ITF_to_Banda.csv`
- `reports/lagged_ITF_to_Banda_best_lags.csv`
- `reports/seasonal_year_ITF_to_Banda.csv`
- `reports/detrending_sensitivity_all_lags.csv`
- `reports/detrending_sensitivity_best_lags.csv`
- `reports/canonical_ITF_Banda_coupling.csv`
- `reports/phase3b_summary.json`
- `figures/heatmap_*_r.png`
- `figures/heatmap_*_partial.png`

## Canonical rule
A pair is `CANONICAL` when ordinary and partial pair-wise FDR pass, |r|>=0.20, >=75% detrending variants preserve sign, and best-lag spread <=4 months. Ordinary-significant relationships that fail some robustness/partial criteria become `CONDITIONAL`; the remainder are `REVIEW`.

Positive lag means **ITF transport leads Banda Sea response**.

Mediation remains explicitly deferred until Phase 3B is reviewed.

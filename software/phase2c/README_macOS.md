# Phase 2C – Data Preprocessing & Harmonization v1.0

Transforms Phase 2B production data into analysis-ready monthly datasets for 1993–2025.

Key outputs:
- combined GLORYS and ERA5 monthly NetCDF
- DUACS daily → monthly mean
- Niño3.4/DMI with z-scores
- OHC 0–300 m and 0–700 m
- SST, MLD, wind-stress magnitude/curl, Ekman-pumping diagnostic proxy
- monthly climatological anomalies
- harmonized 396-row monthly table

Scientific defaults:
- OHC uses rho0=1025 kg m-3, cp=3990 J kg-1 K-1, Tref=0°C
- climatology baseline 1993–2020 (configurable)
- DUACS monthly means are explicitly derived with xarray resampling
- Phase 2B raw files remain unchanged
- ITF/ARLINDO section transport is not invented here; explicit section geometry belongs in the next transport module

Before running, edit `config/preprocessing_config.yaml` if your Phase 2B folder is not the sibling:
`../Phase2B_Data_Acquisition_Pipeline_v1.2_final_macOS`

Run on macOS:
```bash
cd ~/Downloads/Phase2C_Preprocessing_Harmonization_v1.0_macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
caffeinate -dimsu bash run_phase2c.sh
```

Main output:
`data/processed/timeseries/harmonized_monthly_1993_2025.csv`

QC:
`reports/phase2c_qc_report.json`

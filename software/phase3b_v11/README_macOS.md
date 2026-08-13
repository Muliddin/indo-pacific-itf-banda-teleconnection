# Phase 3B v1.1 – Mechanistic Directionality & Full Ekman Pumping

This package is the final mechanistic gate before formal mediation/path analysis.

## 1. Full Ekman pumping
The pipeline computes the classical full Ekman pumping velocity on the ERA5 grid:

`w_E = d/dx[tau_y/(rho0 f)] - d/dy[tau_x/(rho0 f)]`

with:
- rho0 = 1025 kg m-3
- f = 2 Omega sin(latitude)
- spherical x/y metric factors
- SST-based ocean masking when ERA5 SST is present
- cosine-latitude area weighting
- 1993–2020 monthly climatological anomalies
- linear detrending over 1993–2025

This replaces the Phase 2C proxy `curl(tau)/(rho0*f)` for publication-level upwelling interpretation.

## 2. Directionality
For every wind–ITF and wind–ocean pair, the pipeline scans both directions over lags 0..12 months:
- wind forcing -> ITF/OHC/SST/MLD
- ITF/OHC/SST/MLD -> wind forcing

Significance uses AR(1)-adjusted effective sample size and Benjamini–Hochberg FDR within each direction.

Directionality results are associative diagnostics, not proof of causality.

## 3. Mechanistic pathway registry
Pathways are classified into:
- `oceanic`
- `atmospheric`
- `directionality/common-forcing`

The registry is designed to prevent statistically significant but physically reversed links such as `ITF -> wind-stress curl` from being treated as causal outcomes.

## Run on macOS
```bash
cd ~/Downloads/Phase3B_v1.1_Mechanistic_Directionality_FullEkman
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_phase3b_v1.1.sh
```

Default sibling inputs:
- `../Phase2C_Preprocessing_Harmonization_v1.0_macOS`
- `../Phase3A_Teleconnection_Analysis_v1.0`
- `../Phase3B_ITF_OHC_Upwelling_Coupling_v1.0`

The ERA5 source NetCDF is auto-discovered below the Phase 2C root by searching for a file containing both `avg_iews` and `avg_inss`, preferring a 396-month file.

## Key outputs
- `data/processed/full_ekman_pumping_banda_1993_2025.csv`
- `data/processed/mechanistic_master_1993_2025.csv`
- `reports/mechanistic_directionality_all_lags.csv`
- `reports/mechanistic_directionality_best.csv`
- `reports/mechanistic_pathway_registry.csv`
- `reports/phase3b_v11_summary.json`
- `figures/directionality_*.png`

## Interpretation
Use full Ekman pumping, not the old proxy, in publication-level upwelling pathways. Formal mediation should begin only after the pathway registry is reviewed.

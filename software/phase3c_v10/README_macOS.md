# Phase3C_Parallel_Mediation_PathAnalysis_v1.0

Primary question:
How much of the ENSO/IOD association with Banda Sea OHC is statistically consistent with an **oceanic ITF pathway** versus an **atmospheric full-Ekman pathway**?

## Primary models
Four pre-specified models:
- Niño3.4 → {Qout, full Ekman} → OHC300
- Niño3.4 → {Qout, full Ekman} → OHC700
- DMI → {Qout, full Ekman} → OHC300
- DMI → {Qout, full Ekman} → OHC700

Niño3.4 models control DMI; DMI models control Niño3.4.

## Lag-aware alignment
For each outcome, the common outcome horizon is the longest frozen mediator→outcome lag.
For OHC300/OHC700:
- Qout is sampled one month before the outcome;
- full Ekman is sampled contemporaneously with the outcome;
- both pathways are fitted in one parallel-mediator outcome model.

This keeps both mediators tied to one common outcome timestamp rather than comparing effects from incompatible target months.

## Effects reported
- `a_qout`, `a_ekman`
- `b_qout`, `b_ekman`
- Qout indirect = a_qout × b_qout
- Ekman indirect = a_ekman × b_ekman
- total indirect
- direct effect c'
- total effect c
- decomposition error
- R² for mediator and outcome equations

All coefficients are standardized within each aligned sample.

## Inference
Primary monthly models use a 12-month moving-block bootstrap (default 5000 replicates).
SON/JJA sensitivity resamples outcome years, not individual months.
Benjamini–Hochberg FDR is applied to indirect-effect bootstrap p-values.

## Sensitivity analyses
- Qout replaced one-at-a-time by Makassar, Ombai, or Timor;
- SON and JJA;
- SST and MLD as secondary outcomes.

## Automatic freeze
A primary indirect pathway must pass:
- bootstrap CI excludes zero;
- FDR q <= 0.05;
- |indirect effect| >= 0.01;
- bootstrap sign stability >= 0.80.

Qout additionally requires >=2/3 section-level sign agreement for `FREEZE`.
Ekman additionally requires seasonal sign support and at least one SON/JJA q<=0.10.
Otherwise a primary-passing pathway is `CONDITIONAL`; failed primary inference is `REVIEW`.

## Run
```bash
cd ~/Downloads/Phase3C_Parallel_Mediation_PathAnalysis_v1.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_phase3c.sh
```

Default inputs:
- `../Phase3A_Teleconnection_Analysis_v1.0`
- `../Phase3B_v1.1_Mechanistic_Directionality_FullEkman`

## Key outputs
- `data/processed/mediation_master_1993_2025.csv`
- `reports/primary_parallel_mediation.csv`
- `reports/section_level_mediation_sensitivity.csv`
- `reports/seasonal_SON_JJA_mediation_sensitivity.csv`
- `reports/secondary_outcome_mediation.csv`
- `reports/mediation_robustness_freeze.csv`
- `reports/phase3c_summary.json`
- `figures/mediation_*.png`

These are lag-aware statistical mediation/path models. They provide evidence consistent with hypothesized mechanisms but should not be described as proof of causality without the structural assumptions stated in the manuscript.

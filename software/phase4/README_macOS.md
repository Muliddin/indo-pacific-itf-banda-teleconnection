# Phase 4 v1.0 — Synthesis, Figures, Robustness Summary & Manuscript Architecture

This package integrates frozen Phase 2D/3A/3B/3C outputs. It does **not** run new hypothesis tests.

## Run
```bash
cd ~/Downloads/Phase4_Synthesis_Manuscript_v1.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_phase4.sh
```

If your folder names differ, edit `config/phase4_config.yaml`.

## Evidence hierarchy
- ROBUST_CORE — permitted for primary association/robustness claims.
- CONDITIONAL_SUPPORTING — must retain season/lag/model qualification.
- EXPLORATORY_CONTEXTUAL — context only; no confirmatory causal claim.

## Principal outputs
- `reports/evidence_registry.csv`
- `reports/robustness_matrix.csv`
- `reports/phase4_summary.json`
- `tables/Table_1...Table_6...`
- `figures/Figure_1...Figure_5...`
- `manuscript/Results_Discussion_DRAFT.md`

The manuscript draft deliberately uses non-causal language because formal Phase 3C mediation was not robust.

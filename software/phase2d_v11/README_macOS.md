# Phase 2D v1.1 – Native-Grid Section Transport

Uses existing Phase 2D v1.0 GLORYS corridor files. No redownload is needed for Makassar/Lombok/Ombai.

Run:
```bash
cd ~/Downloads/Phase2D_v1.1_NativeGrid_Transport_macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python compute_native_grid_transport.py --phase2d-v1-root ../Phase2D_ITF_Transport_v1.0_macOS
python scripts/evaluate_and_select_canonical.py
python scripts/validate_canonical.py --phase2d-v1-root ../Phase2D_ITF_Transport_v1.0_macOS
```

Canonical selection uses:
- 35% anchor proximity
- 25% temporal robustness to the 7-section ensemble median
- 25% wet-column continuity
- 15% literature consistency

Eligibility guardrails:
- wet-column fraction >= 0.50
- correlation to ensemble median >= 0.90

The literature term is deliberately low-weight so the chosen section is not simply calibrated to observations.

Main outputs:
- `reports/native_grid_candidate_scores.csv`
- `reports/canonical_selection.json`
- `reports/canonical_validation_summary.csv`
- `data/processed/canonical/itf_transport_CANONICAL_1993_2025.csv`

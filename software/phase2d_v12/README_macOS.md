# Phase 2D v1.2 — Timor Passage + Total Major Outflow

Timor is oblique, so it is treated separately from the zonal/meridional native sections.

Primary-source anchors:
- four Timor moorings in INSTANT;
- reported width ~80 km;
- western sill ~1890 m;
- 2004–2006 mean Timor outflow benchmark ~7.5 Sv.

Geometry caution:
The INSTANT web table renders the fourth longitude as 123°52'E, inconsistent with the first three western-sill longitudes and stated 80-km width. v1.2 therefore constructs an 80-km oblique transect using the first-three-mooring cluster and tests offsets -3..+3.

Run:
```bash
cd ~/Downloads/Phase2D_v1.2_Timor_TotalOutflow_macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
copernicusmarine login

caffeinate -dimsu python scripts/download_timor_corridor.py
python scripts/compute_timor_candidates.py
python scripts/select_timor_canonical.py
python scripts/build_validate_total_outflow.py --phase2d-v11-root ../Phase2D_v1.1_NativeGrid_Transport_macOS
```

Review:
- reports/timor_candidate_scores.csv
- reports/timor_canonical_selection.json
- reports/total_outflow_validation_2004_2006.csv

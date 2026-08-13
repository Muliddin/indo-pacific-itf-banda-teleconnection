# Phase4.1_Manuscript_Audit_Submission_v1.0

Reads the frozen Phase 4 v1.0 synthesis and produces a submission-facing audit layer.

## Outputs
- `reports/claim_evidence_matrix.csv`
- `reports/final_figure_table_manifest.csv`
- `reports/main_vs_supplementary_architecture.csv`
- `reports/claim_language_audit.csv`
- `reports/phase4_1_summary.json`
- `manuscript/Manuscript_Outline.md`
- `manuscript/Results_Discussion_v2_AUDITED.md`

## Run
```bash
cd ~/Downloads/Phase4.1_Manuscript_Audit_Submission_v1.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_phase4_1.sh
```

Default input:
`../Phase4_Synthesis_Manuscript_v1.0`

This phase does not re-estimate statistics or relax thresholds. It maps frozen evidence to permitted manuscript language and submission placement.

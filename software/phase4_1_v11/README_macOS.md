# Phase4.1_v1.1_Final_Publication_Set

Final curation layer for the manuscript. It reads frozen Phase 4 and Phase 4.1 outputs and performs **no new hypothesis testing**.

## Outputs
### Main figures
- Figure 1: ITF validation
- Figure 2: ENSO/IOD→ITF frozen effects
- Figure 3: seasonal-year + event structure
- Figure 4: ITF/atmosphere–Banda coupling
- Figure 5: integrated conceptual synthesis + mediation constraint

### Main tables
- Table 1: concise ITF validation
- Table 2: robust core ENSO/IOD→ITF findings
- Table 3: seasonal/event + Banda coupling synthesis

### Submission support
- `captions/Figure_Captions.md`
- `captions/Table_Notes.md`
- `reports/submission_manifest.csv`
- `reports/publication_set_summary.json`

## Run
```bash
cd ~/Downloads/Phase4.1_v1.1_Final_Publication_Set
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_publication_set.sh
```

Default inputs:
- `../Phase4_Synthesis_Manuscript_v1.0`
- `../Phase4.1_Manuscript_Audit_Submission_v1.0`

This package preserves the frozen evidence hierarchy. Conditional findings remain explicitly conditional, and non-robust formal mediation remains a constraint rather than a causal result.

import json,pandas as pd
from common import ROOT,log
def main():
    L=log("06_summary")
    p=pd.read_csv(ROOT/"reports/mechanistic_pathway_registry.csv")
    rep={
        "n_pathways":len(p),
        "n_atmospheric_candidates":int(p.status.astype(str).str.contains("ATMOSPHERIC_CANDIDATE").sum()),
        "n_oceanic_mediation_candidates":int(p.status.astype(str).str.contains("OCEANIC_MEDIATION_CANDIDATE|OCEANIC_CANDIDATE_STRONG",regex=True).sum()),
        "n_common_forcing_or_ambiguous":int(p.status.astype(str).str.contains("COMMON_FORCING|AMBIGUOUS",regex=True).sum()),
        "note":"Full Ekman pumping uses curl(tau/(rho0*f)) on the ERA5 grid with SST ocean masking. Directionality is associative, not proof of causality."
    }
    (ROOT/"reports/phase3b_v11_summary.json").write_text(json.dumps(rep,indent=2))
    print(json.dumps(rep,indent=2))
    L.info("Summary complete")
if __name__=="__main__":main()

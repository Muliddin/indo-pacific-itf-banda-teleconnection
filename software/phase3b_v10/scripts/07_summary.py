import json,pandas as pd
from common import ROOT,log
def main():
    L=log("07_summary")
    c=pd.read_csv(ROOT/"reports/canonical_ITF_Banda_coupling.csv")
    rep={
        "n_pairs":len(c),
        "n_canonical":int((c.coupling_status=="CANONICAL").sum()),
        "n_conditional":int((c.coupling_status=="CONDITIONAL").sum()),
        "n_review":int((c.coupling_status=="REVIEW").sum()),
        "note":"Phase 3B estimates ITF→Banda coupling and partial coupling controlling Niño3.4+DMI. Mediation remains deferred."
    }
    (ROOT/"reports/phase3b_summary.json").write_text(json.dumps(rep,indent=2),encoding="utf-8")
    print(json.dumps(rep,indent=2))
    L.info("Summary complete")
if __name__=="__main__":
    main()

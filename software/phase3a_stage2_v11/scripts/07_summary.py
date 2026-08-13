import json,pandas as pd
from common import ROOT,log
def main():
    L=log("07_summary")
    f=pd.read_csv(ROOT/"reports/stage2_freeze_decision.csv")
    rep={
        "n_freeze":int((f.freeze_status=="FREEZE").sum()),
        "n_conditional":int((f.freeze_status=="CONDITIONAL").sum()),
        "n_review":int((f.freeze_status=="REVIEW").sum()),
        "note":"Stage 2 v1.1 uses seasonal-year aggregation and independent event episodes; mediation remains deferred."
    }
    (ROOT/"reports/stage2_v11_summary.json").write_text(json.dumps(rep,indent=2),encoding="utf-8")
    print(json.dumps(rep,indent=2))
    L.info("Summary complete")
if __name__=="__main__":
    main()

import json,pandas as pd
from common import ROOT,log
def main():
    L=log("08_summary")
    f=pd.read_csv(ROOT/"reports/mediation_robustness_freeze.csv")
    p=pd.read_csv(ROOT/"reports/primary_parallel_mediation.csv")
    rep={
        "primary_models":len(p),
        "pathway_tests":len(f),
        "n_freeze":int((f.freeze_status=="FREEZE").sum()),
        "n_conditional":int((f.freeze_status=="CONDITIONAL").sum()),
        "n_review":int((f.freeze_status=="REVIEW").sum()),
        "note":"Effects are standardized linear path coefficients with Niño3.4/DMI mutual adjustment and lag-aware alignment. Bootstrap inference preserves temporal dependence; results support mechanistic mediation evidence but do not by themselves prove causality."
    }
    (ROOT/"reports/phase3c_summary.json").write_text(json.dumps(rep,indent=2),encoding="utf-8")
    print(json.dumps(rep,indent=2));L.info("Summary complete")
if __name__=="__main__":main()

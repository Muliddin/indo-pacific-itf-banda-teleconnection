import json,pandas as pd
from common import ROOT,log
def main():
    L=log("07_summary")
    d=pd.read_csv(ROOT/"reports/mediation_collinearity_diagnostic_classification.csv")
    rep={
        "n_diagnostics":len(d),
        "n_independent_mediation_supported":int((d.diagnostic_status=="INDEPENDENT_MEDIATION_SUPPORTED").sum()),
        "n_shared_variance_or_suppression_supported":int((d.diagnostic_status=="SHARED_VARIANCE_OR_SUPPRESSION_SUPPORTED").sum()),
        "n_no_robust_mediation":int((d.diagnostic_status=="NO_ROBUST_MEDIATION").sum()),
        "note":"This phase diagnoses why single-mediator and parallel-mediator effects differ. It does not relax Phase 3C v1.0 inferential thresholds."
    }
    (ROOT/"reports/phase3c_v11_summary.json").write_text(json.dumps(rep,indent=2),encoding="utf-8")
    print(json.dumps(rep,indent=2));L.info("Summary complete")
if __name__=="__main__":main()

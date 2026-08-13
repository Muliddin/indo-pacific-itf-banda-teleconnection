from common import *
def main():
    m=pd.read_csv(ROOT/"reports/submission_manifest.csv")
    rep={"phase":"Phase4.1 v1.1 - Final Publication Set","version":"v1.1",
         "main_figures":int(((m.artifact_type=="figure")&(m.placement=="MAIN")).sum()),
         "main_tables":int(((m.artifact_type=="table")&(m.placement=="MAIN")).sum()),
         "all_artifacts_exist":bool(m.exists.all()),
         "statistical_reestimation":False,
         "causal_policy":"No causal mediation claim; evidence hierarchy preserved.",
         "status":"PASS" if m.exists.all() else "FAIL"}
    (ROOT/"reports/publication_set_summary.json").write_text(json.dumps(rep,indent=2),encoding="utf-8")
    print(json.dumps(rep,indent=2))
if __name__=="__main__":main()

import pandas as pd,numpy as np
from common import ROOT,cfg,resolve,vif_for_two,log
def main():
    c=cfg();L=log("02_collinearity");r=resolve(c["inputs"]["phase3c_v10_root"])
    df=pd.read_csv(r/"data/processed/mediation_master_1993_2025.csv",parse_dates=["time"])
    q=c["mediators"]["qout"];e=c["mediators"]["ekman"]
    corr=df[[q,e,"nino34","dmi"]].corr()
    corr.to_csv(ROOT/"reports/mediator_correlation_matrix.csv")
    vif=vif_for_two(df[q],df[e])
    rows=[{"predictor":q,"paired_with":e,"pairwise_r":df[q].corr(df[e]),"vif_two_predictor":vif},
          {"predictor":e,"paired_with":q,"pairwise_r":df[q].corr(df[e]),"vif_two_predictor":vif}]
    out=pd.DataFrame(rows)
    warn=float(c["analysis"]["vif_warning"]);high=float(c["analysis"]["vif_high"])
    out["vif_flag"]=out.vif_two_predictor.map(lambda x:"HIGH" if x>=high else "WARNING" if x>=warn else "LOW")
    out.to_csv(ROOT/"reports/mediator_vif_diagnostics.csv",index=False)
    print(corr.to_string());print(out.to_string(index=False));L.info("Collinearity diagnostics complete")
if __name__=="__main__":main()

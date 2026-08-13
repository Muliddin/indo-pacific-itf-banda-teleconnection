import numpy as np,pandas as pd
from common import ROOT,cfg,corr_ar1,partial_corr_two_controls,bh_fdr,log
def main():
    c=cfg();L=log("02_lagged")
    df=pd.read_csv(ROOT/"data/processed/coupling_master_1993_2025.csv",parse_dates=["time"])
    rows=[]
    for base in c["transport_predictors"]:
        pred=base+"_anom_dt"
        for resp in c["banda_responses"]:
            response=resp+"_dt"
            for lag in range(int(c["analysis"]["lag_min_months"]),int(c["analysis"]["lag_max_months"])+1):
                y=df[response].shift(-lag)
                r,n,ne,p=corr_ar1(df[pred],y)
                pr,pn,pne,pp=partial_corr_two_controls(df[pred],y,df.nino34,df.dmi)
                rows.append({
                    "predictor":pred,"response":response,
                    "lag_months_itf_leads":lag,
                    "r":r,"n":n,"effective_n_ar1":ne,"p_ar1":p,
                    "partial_r_ctrl_nino34_dmi":pr,
                    "partial_n":pn,"partial_effective_n_ar1":pne,
                    "p_partial_ar1":pp
                })
    out=pd.DataFrame(rows)
    out["q_fdr_global"]=bh_fdr(out.p_ar1.to_numpy())
    out["q_partial_fdr_global"]=bh_fdr(out.p_partial_ar1.to_numpy())
    out["q_fdr_within_pair"]=np.nan
    out["q_partial_fdr_within_pair"]=np.nan
    for _,ids in out.groupby(["predictor","response"]).groups.items():
        out.loc[ids,"q_fdr_within_pair"]=bh_fdr(out.loc[ids,"p_ar1"].to_numpy())
        out.loc[ids,"q_partial_fdr_within_pair"]=bh_fdr(out.loc[ids,"p_partial_ar1"].to_numpy())
    (ROOT/"reports").mkdir(parents=True,exist_ok=True)
    out.to_csv(ROOT/"reports/lagged_ITF_to_Banda.csv",index=False)

    best=[]
    for (pred,resp),g in out.groupby(["predictor","response"]):
        a=g.loc[g.r.abs().idxmax()]
        b=g.loc[g.partial_r_ctrl_nino34_dmi.abs().idxmax()]
        best.append({
            "predictor":pred,"response":resp,
            "best_lag_r":int(a.lag_months_itf_leads),
            "r_best":a.r,"q_pair_best":a.q_fdr_within_pair,
            "best_lag_partial":int(b.lag_months_itf_leads),
            "partial_r_best":b.partial_r_ctrl_nino34_dmi,
            "q_partial_pair_best":b.q_partial_fdr_within_pair
        })
    best=pd.DataFrame(best)
    best.to_csv(ROOT/"reports/lagged_ITF_to_Banda_best_lags.csv",index=False)
    print(best.to_string(index=False))
    L.info("Lagged ITF->Banda complete")
if __name__=="__main__":
    main()

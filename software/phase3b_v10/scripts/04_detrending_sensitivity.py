import numpy as np,pandas as pd
from common import ROOT,cfg,corr_ar1,partial_corr_two_controls,bh_fdr,log
def main():
    c=cfg();L=log("04_sensitivity")
    df=pd.read_csv(ROOT/"data/processed/coupling_master_1993_2025.csv",parse_dates=["time"])
    combos=[
        ("itf_dt__banda_dt",True,True),
        ("itf_raw__banda_dt",False,True),
        ("itf_dt__banda_raw",True,False),
        ("itf_raw__banda_raw",False,False),
    ]
    rows=[]
    for base in c["transport_predictors"]:
        for resp in c["banda_responses"]:
            for prep,itfdt,bandadt in combos:
                pred=base+"_anom_dt" if itfdt else base+"_anom"
                response=resp+"_dt" if bandadt else resp
                for lag in range(int(c["analysis"]["lag_min_months"]),int(c["analysis"]["lag_max_months"])+1):
                    y=df[response].shift(-lag)
                    r,n,ne,p=corr_ar1(df[pred],y)
                    pr,pn,pne,pp=partial_corr_two_controls(df[pred],y,df.nino34,df.dmi)
                    rows.append({
                        "predictor_base":base,"response_base":resp,
                        "preprocessing":prep,"lag_months_itf_leads":lag,
                        "r":r,"p_ar1":p,
                        "partial_r_ctrl_nino34_dmi":pr,
                        "p_partial_ar1":pp
                    })
    out=pd.DataFrame(rows)
    out["q_pair"]=np.nan
    out["q_partial_pair"]=np.nan
    for _,ids in out.groupby(["predictor_base","response_base","preprocessing"]).groups.items():
        out.loc[ids,"q_pair"]=bh_fdr(out.loc[ids,"p_ar1"].to_numpy())
        out.loc[ids,"q_partial_pair"]=bh_fdr(out.loc[ids,"p_partial_ar1"].to_numpy())
    out.to_csv(ROOT/"reports/detrending_sensitivity_all_lags.csv",index=False)

    best=[]
    for (pred,resp,prep),g in out.groupby(["predictor_base","response_base","preprocessing"]):
        a=g.loc[g.r.abs().idxmax()]
        b=g.loc[g.partial_r_ctrl_nino34_dmi.abs().idxmax()]
        best.append({
            "predictor_base":pred,"response_base":resp,"preprocessing":prep,
            "best_lag_r":int(a.lag_months_itf_leads),
            "r_best":a.r,"q_pair_best":a.q_pair,
            "best_lag_partial":int(b.lag_months_itf_leads),
            "partial_r_best":b.partial_r_ctrl_nino34_dmi,
            "q_partial_pair_best":b.q_partial_pair
        })
    best=pd.DataFrame(best)
    best.to_csv(ROOT/"reports/detrending_sensitivity_best_lags.csv",index=False)
    print(best.to_string(index=False))
    L.info("Detrending sensitivity complete")
if __name__=="__main__":
    main()

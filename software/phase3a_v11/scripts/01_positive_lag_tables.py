import numpy as np,pandas as pd
from common import ROOT,cfg,resolve,bh_fdr,partial_corr_stats,log
def main():
    c=cfg(); L=log("01_positive_lags")
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    df=pd.read_csv(p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",parse_dates=["time"])
    lag0=int(c["analysis"]["lag_min_causal"]); lag1=int(c["analysis"]["lag_max_causal"])
    rows=[]
    for idx,other in [("nino34","dmi"),("dmi","nino34")]:
        for base in c["transport_targets"]:
            target=base+"_anom_dt"
            for lag in range(lag0,lag1+1):
                y=df[target].shift(-lag)
                z=pd.DataFrame({"x":df[idx],"y":y}).dropna()
                r=z.x.corr(z.y)
                pr,n,ne,pp=partial_corr_stats(df[idx],y,df[other])
                # import ordinary p from v1.0 if exact key available
                rows.append({"index":idx,"target":target,"lag_months_index_leads":lag,
                             "r":r,"partial_r":pr,"n_partial":n,"effective_n_partial_ar1":ne,
                             "p_partial_ar1":pp})
    out=pd.DataFrame(rows)
    out["q_partial_global"]=bh_fdr(out.p_partial_ar1.to_numpy())
    out["q_partial_within_pair"]=np.nan
    for _,ids in out.groupby(["index","target"]).groups.items():
        out.loc[ids,"q_partial_within_pair"]=bh_fdr(out.loc[ids,"p_partial_ar1"].to_numpy())
    out["partial_significant_pair_fdr"]=out.q_partial_within_pair<=float(c["analysis"]["fdr_alpha"])

    # merge ordinary-correlation p/q from v1.0 positive lags
    old=pd.read_csv(p3/"reports/lagged_ENSO_IOD_to_ITF.csv")
    old=old[(old.lag_months_index_leads>=lag0)&(old.lag_months_index_leads<=lag1)]
    keep=["index","target","lag_months_index_leads","p_ar1","q_fdr_within_pair","q_fdr_global"]
    out=out.merge(old[keep],on=["index","target","lag_months_index_leads"],how="left",validate="one_to_one")
    out.to_csv(ROOT/"reports/positive_lag_ENSO_IOD_to_ITF.csv",index=False)

    best=[]
    for (idx,target),g in out.groupby(["index","target"]):
        a=g.loc[g.r.abs().idxmax()]
        b=g.loc[g.partial_r.abs().idxmax()]
        best.append({
            "index":idx,"target":target,
            "best_positive_lag_r":int(a.lag_months_index_leads),"r_best_positive":a.r,
            "p_ar1_best_positive":a.p_ar1,"q_pair_best_positive":a.q_fdr_within_pair,
            "best_positive_lag_partial_r":int(b.lag_months_index_leads),
            "partial_r_best_positive":b.partial_r,
            "p_partial_ar1_best_positive":b.p_partial_ar1,
            "q_partial_pair_best_positive":b.q_partial_within_pair,
        })
    best=pd.DataFrame(best)
    best.to_csv(ROOT/"reports/positive_lag_best_lags.csv",index=False)
    print(best.to_string(index=False))
    L.info("Positive-lag tables complete")
if __name__=="__main__":main()

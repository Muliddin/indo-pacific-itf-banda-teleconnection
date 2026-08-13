import pandas as pd, numpy as np
from common import ROOT,cfg,resolve,season_info,corr_ar1,bh_fdr,log
def main():
    c=cfg();L=log("01_seasonal_year")
    p10=resolve(c["inputs"]["phase3a_v10_root"])
    df=pd.read_csv(p10/"data/processed/analysis_master_anom_detrended_1993_2025.csv",parse_dates=["time"])
    info=df.time.map(season_info)
    df["season"]=[x[0] for x in info]
    df["season_year"]=[x[1] for x in info]
    rows=[]
    for idx in ["nino34","dmi"]:
        for target,lag in c["stage1_frozen_lags"].get(idx,{}).items():
            tmp=df[["time","season","season_year",idx,target]].copy()
            tmp["response_shifted"]=tmp[target].shift(-int(lag))
            agg=tmp.groupby(["season","season_year"],as_index=False).agg(
                index_mean=(idx,"mean"),
                response_mean=("response_shifted","mean"),
                n_months=("time","count")
            )
            agg=agg[agg.n_months>=2]
            for season,g in agg.groupby("season"):
                r,n,ne,p=corr_ar1(g.index_mean,g.response_mean)
                rows.append({
                    "index":idx,"target":target,"frozen_lag":lag,"season":season,
                    "n_season_years":n,"r":r,"effective_n_ar1":ne,"p_ar1":p
                })
    out=pd.DataFrame(rows)
    out["q_fdr_global"]=bh_fdr(out.p_ar1.to_numpy())
    out["q_fdr_within_index"]=np.nan
    for _,ids in out.groupby("index").groups.items():
        out.loc[ids,"q_fdr_within_index"]=bh_fdr(out.loc[ids,"p_ar1"].to_numpy())
    out["significant_fdr"]=out.q_fdr_global<=float(c["analysis"]["fdr_alpha"])
    out.to_csv(ROOT/"reports/seasonal_year_correlations.csv",index=False)
    print(out.to_string(index=False))
    L.info("Seasonal-year correlations complete")
if __name__=="__main__":
    main()

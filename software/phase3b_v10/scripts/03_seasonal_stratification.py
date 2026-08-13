import pandas as pd,numpy as np
from common import ROOT,cfg,season_info,corr_ar1,partial_corr_two_controls,bh_fdr,log
def main():
    c=cfg();L=log("03_seasonal")
    df=pd.read_csv(ROOT/"data/processed/coupling_master_1993_2025.csv",parse_dates=["time"])
    best=pd.read_csv(ROOT/"reports/lagged_ITF_to_Banda_best_lags.csv")
    info=df.time.map(season_info)
    df["season"]=[x[0] for x in info]
    df["season_year"]=[x[1] for x in info]
    rows=[]
    for _,b in best.iterrows():
        pred=b.predictor; resp=b.response; lag=int(b.best_lag_r)
        tmp=df[["time","season","season_year",pred,resp,"nino34","dmi"]].copy()
        tmp["response_shifted"]=tmp[resp].shift(-lag)
        agg=tmp.groupby(["season","season_year"],as_index=False).agg(
            predictor_mean=(pred,"mean"),
            response_mean=("response_shifted","mean"),
            nino34_mean=("nino34","mean"),
            dmi_mean=("dmi","mean"),
            n_months=("time","count")
        )
        agg=agg[agg.n_months>=2]
        for season,g in agg.groupby("season"):
            r,n,ne,p=corr_ar1(g.predictor_mean,g.response_mean)
            pr,pn,pne,pp=partial_corr_two_controls(
                g.predictor_mean,g.response_mean,g.nino34_mean,g.dmi_mean
            )
            rows.append({
                "predictor":pred,"response":resp,"frozen_best_lag":lag,
                "season":season,"n_season_years":n,
                "r":r,"p_ar1":p,
                "partial_r_ctrl_nino34_dmi":pr,
                "p_partial_ar1":pp
            })
    out=pd.DataFrame(rows)
    out["q_fdr_global"]=bh_fdr(out.p_ar1.to_numpy())
    out["q_partial_fdr_global"]=bh_fdr(out.p_partial_ar1.to_numpy())
    out.to_csv(ROOT/"reports/seasonal_year_ITF_to_Banda.csv",index=False)
    print(out.to_string(index=False))
    L.info("Seasonal-year coupling complete")
if __name__=="__main__":
    main()

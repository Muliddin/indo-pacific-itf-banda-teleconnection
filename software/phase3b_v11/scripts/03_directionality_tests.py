import numpy as np,pandas as pd
from common import ROOT,cfg,corr_ar1,bh_fdr,log

def scan(df,a,b,maxlag):
    rows=[]
    for lag in range(maxlag+1):
        # a leads b by lag
        y=df[b].shift(-lag)
        r,n,ne,p=corr_ar1(df[a],y)
        rows.append({"leader":a,"follower":b,"lag_months_leader_leads":lag,
                     "r":r,"n":n,"effective_n_ar1":ne,"p_ar1":p})
    return rows

def main():
    c=cfg();L=log("03_directionality")
    df=pd.read_csv(ROOT/"data/processed/mechanistic_master_1993_2025.csv",parse_dates=["time"])
    maxlag=int(c["analysis"]["lag_max_months"])
    winds=[w for w in c["wind_candidates"] if w in df.columns]
    transports=[v for v in c["transport"] if v in df.columns]
    oceans=[v for v in c["ocean_responses"] if v in df.columns]
    rows=[]

    for w in winds:
        for q in transports:
            rows += scan(df,w,q,maxlag)
            rows += scan(df,q,w,maxlag)
        for y in oceans:
            rows += scan(df,w,y,maxlag)
            rows += scan(df,y,w,maxlag)

    out=pd.DataFrame(rows)
    out["q_fdr_within_direction"]=np.nan
    for _,ids in out.groupby(["leader","follower"]).groups.items():
        out.loc[ids,"q_fdr_within_direction"]=bh_fdr(out.loc[ids,"p_ar1"].to_numpy())
    out["q_fdr_global"]=bh_fdr(out.p_ar1.to_numpy())
    out.to_csv(ROOT/"reports/mechanistic_directionality_all_lags.csv",index=False)

    best=[]
    for (a,b),g in out.groupby(["leader","follower"]):
        z=g.loc[g.r.abs().idxmax()]
        best.append({"leader":a,"follower":b,
                     "best_lag":int(z.lag_months_leader_leads),
                     "r_best":z.r,"q_direction_best":z.q_fdr_within_direction})
    best=pd.DataFrame(best)
    best.to_csv(ROOT/"reports/mechanistic_directionality_best.csv",index=False)
    print(best.to_string(index=False))
    L.info("Directionality analysis complete")

if __name__=="__main__":main()

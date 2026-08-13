import numpy as np,pandas as pd
from scipy import stats
from common import ROOT,cfg,resolve,effective_n_ar1,bh_fdr,partial_corr_stats,log
def corr_p(x,y):
    z=pd.DataFrame({"x":x,"y":y}).dropna(); r=z.x.corr(z.y); ne=effective_n_ar1(z.x,z.y)
    if not np.isfinite(r) or not np.isfinite(ne):return r,np.nan
    t=r*np.sqrt((ne-2)/max(1e-12,1-r*r)); return r,2*stats.t.sf(abs(t),df=ne-2)
def main():
    c=cfg();L=log("02_preprocessing_sensitivity")
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    df=pd.read_csv(p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",parse_dates=["time"])
    combos=[
        ("index_raw__itf_dt",False,True),
        ("index_raw__itf_raw",False,False),
        ("index_dt__itf_dt",True,True),
        ("index_dt__itf_raw",True,False),
    ]
    rows=[]
    for idx,other in [("nino34","dmi"),("dmi","nino34")]:
        for base in c["transport_targets"]:
            for combo,idxdt,itfdt in combos:
                ix=idx+"_dt" if idxdt else idx
                oth=other+"_dt" if idxdt else other
                ty=base+"_anom_dt" if itfdt else base+"_anom"
                for lag in range(int(c["analysis"]["lag_min_causal"]),int(c["analysis"]["lag_max_causal"])+1):
                    y=df[ty].shift(-lag)
                    r,p=corr_p(df[ix],y)
                    pr,n,ne,pp=partial_corr_stats(df[ix],y,df[oth])
                    rows.append({"index":idx,"target_base":base,"preprocessing":combo,"lag_months_index_leads":lag,
                                 "r":r,"p_ar1":p,"partial_r":pr,"p_partial_ar1":pp})
    out=pd.DataFrame(rows)
    out["q_pair"]=np.nan; out["q_partial_pair"]=np.nan
    for _,ids in out.groupby(["index","target_base","preprocessing"]).groups.items():
        out.loc[ids,"q_pair"]=bh_fdr(out.loc[ids,"p_ar1"].to_numpy())
        out.loc[ids,"q_partial_pair"]=bh_fdr(out.loc[ids,"p_partial_ar1"].to_numpy())
    out.to_csv(ROOT/"reports/preprocessing_sensitivity_all_lags.csv",index=False)

    best=[]
    for (idx,target,combo),g in out.groupby(["index","target_base","preprocessing"]):
        a=g.loc[g.r.abs().idxmax()]; b=g.loc[g.partial_r.abs().idxmax()]
        best.append({"index":idx,"target":target,"preprocessing":combo,
                     "best_lag_r":int(a.lag_months_index_leads),"r_best":a.r,"q_pair_best":a.q_pair,
                     "best_lag_partial":int(b.lag_months_index_leads),"partial_r_best":b.partial_r,
                     "q_partial_pair_best":b.q_partial_pair})
    best=pd.DataFrame(best)
    best.to_csv(ROOT/"reports/preprocessing_sensitivity_best_lags.csv",index=False)
    print(best.to_string(index=False))
    L.info("Preprocessing sensitivity complete")
if __name__=="__main__":main()

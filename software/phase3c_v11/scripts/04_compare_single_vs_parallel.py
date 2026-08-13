import pandas as pd,numpy as np
from common import ROOT,cfg,resolve,log
def ratio(par,single):
    return abs(par)/abs(single) if np.isfinite(single) and single!=0 else np.nan
def main():
    c=cfg();L=log("04_compare");r=resolve(c["inputs"]["phase3c_v10_root"])
    s=pd.read_csv(ROOT/"reports/single_mediator_models.csv")
    p=pd.read_csv(r/"reports/primary_parallel_mediation.csv")
    rows=[]
    for _,x in s.iterrows():
        z=p[(p.driver==x.driver)&(p.outcome==x.outcome)]
        if z.empty:continue
        z=z.iloc[0]
        pe=float(z.indirect_qout if x.mediator=="qout" else z.indirect_ekman)
        pq=float(z.indirect_qout_q_fdr if x.mediator=="qout" else z.indirect_ekman_q_fdr)
        rr=ratio(pe,float(x.indirect))
        rows.append({"driver":x.driver,"outcome":x.outcome,"mediator":x.mediator,
                     "single_indirect":x.indirect,"single_ci_low":x.indirect_ci_low,"single_ci_high":x.indirect_ci_high,
                     "single_q_fdr":x.indirect_q_fdr,"parallel_indirect":pe,"parallel_q_fdr":pq,
                     "parallel_to_single_abs_ratio":rr,
                     "attenuation_fraction":1-rr if np.isfinite(rr) else np.nan,
                     "single_significant":bool(x.indirect_q_fdr<=float(c["analysis"]["fdr_alpha"])),
                     "parallel_significant":bool(pq<=float(c["analysis"]["fdr_alpha"]))})
    out=pd.DataFrame(rows)
    thr=float(c["analysis"]["attenuation_flag_ratio"])
    out["overlap_suppression_flag"]=out.parallel_to_single_abs_ratio.lt(thr)&out.single_significant
    out.to_csv(ROOT/"reports/single_vs_parallel_indirect_comparison.csv",index=False)
    print(out.to_string(index=False));L.info("Single vs parallel comparison complete")
if __name__=="__main__":main()

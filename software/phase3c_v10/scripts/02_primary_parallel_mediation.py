import pandas as pd
from common import ROOT,cfg,align_parallel,fit_parallel,bootstrap_model,boot_summary,bh_fdr,log

def main():
    c=cfg();L=log("02_primary")
    df=pd.read_csv(ROOT/"data/processed/mediation_master_1993_2025.csv",parse_dates=["time"])
    rows=[]; boot_records=[]
    niter=int(c["analysis"]["bootstrap_iterations"]); block=int(c["analysis"]["block_length_months"]); seed=int(c["analysis"]["random_seed"])
    for driver,dcfg in c["drivers"].items():
        covar=dcfg["covariate"]
        for oname,ocfg in c["primary_outcomes"].items():
            y=ocfg["variable"]; l1=int(ocfg["mediator_to_outcome_lags"]["qout"]); l2=int(ocfg["mediator_to_outcome_lags"]["ekman"])
            d=align_parallel(df,driver,covar,c["mediators"]["qout"],c["mediators"]["ekman"],y,l1,l2)
            pt=fit_parallel(d)
            boots=bootstrap_model(d,niter,block,seed,seasonal=False)
            rec={"driver":driver,"covariate":covar,"outcome":oname,"outcome_variable":y,
                 "qout_to_outcome_lag":l1,"ekman_to_outcome_lag":l2,"common_horizon_months":int(d.horizon_months.iloc[0]),**pt}
            for eff in ["indirect_qout","indirect_ekman","total_indirect","direct_effect","total_effect"]:
                lo,hi,p,stab=boot_summary(pt,boots,eff)
                rec[f"{eff}_ci_low"]=lo;rec[f"{eff}_ci_high"]=hi;rec[f"{eff}_boot_p"]=p;rec[f"{eff}_sign_stability"]=stab
            rows.append(rec)
            b=boots.copy();b["driver"]=driver;b["outcome"]=oname;boot_records.append(b)
    out=pd.DataFrame(rows)
    for eff in ["indirect_qout","indirect_ekman","total_indirect","direct_effect","total_effect"]:
        out[f"{eff}_q_fdr"]=bh_fdr(out[f"{eff}_boot_p"].to_numpy())
    out.to_csv(ROOT/"reports/primary_parallel_mediation.csv",index=False)
    if boot_records:
        pd.concat(boot_records,ignore_index=True).to_csv(ROOT/"data/processed/primary_bootstrap_effects.csv",index=False)
    print(out.to_string(index=False));L.info("Primary parallel mediation complete")
if __name__=="__main__":main()

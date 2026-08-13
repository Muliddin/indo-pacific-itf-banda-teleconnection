import pandas as pd
from common import ROOT,cfg,resolve,align_single,fit_single,bootstrap_single,boot_summary,bh_fdr,log
def main():
    c=cfg();L=log("01_single");r=resolve(c["inputs"]["phase3c_v10_root"])
    df=pd.read_csv(r/"data/processed/mediation_master_1993_2025.csv",parse_dates=["time"])
    rows=[];niter=int(c["analysis"]["bootstrap_iterations"]);block=int(c["analysis"]["block_length_months"]);seed=int(c["analysis"]["random_seed"])
    for drv,dc in c["drivers"].items():
        cov=dc["covariate"]
        for on,oc in c["outcomes"].items():
            for mn,mv in c["mediators"].items():
                lag=int(oc["lags"][mn]);d=align_single(df,drv,cov,mv,oc["variable"],lag)
                pt=fit_single(d);boots=bootstrap_single(d,niter,block,seed)
                rec={"driver":drv,"covariate":cov,"outcome":on,"mediator":mn,"lag_mediator_to_outcome":lag,**pt}
                for eff in ["indirect","direct","total"]:
                    lo,hi,p,stab=boot_summary(boots,eff)
                    rec[f"{eff}_ci_low"]=lo;rec[f"{eff}_ci_high"]=hi;rec[f"{eff}_boot_p"]=p;rec[f"{eff}_sign_stability"]=stab
                rows.append(rec)
    out=pd.DataFrame(rows)
    for eff in ["indirect","direct","total"]:out[f"{eff}_q_fdr"]=bh_fdr(out[f"{eff}_boot_p"].to_numpy())
    out.to_csv(ROOT/"reports/single_mediator_models.csv",index=False)
    print(out.to_string(index=False));L.info("Single mediator models complete")
if __name__=="__main__":main()

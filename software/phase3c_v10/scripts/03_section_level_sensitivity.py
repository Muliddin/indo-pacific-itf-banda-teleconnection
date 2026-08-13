import pandas as pd
from common import ROOT,cfg,align_parallel,fit_parallel,bootstrap_model,boot_summary,bh_fdr,log

def main():
    c=cfg();L=log("03_section_sensitivity")
    df=pd.read_csv(ROOT/"data/processed/mediation_master_1993_2025.csv",parse_dates=["time"])
    rows=[];niter=int(c["analysis"]["bootstrap_iterations"]);block=int(c["analysis"]["block_length_months"]);seed=int(c["analysis"]["random_seed"])
    for driver,dcfg in c["drivers"].items():
        covar=dcfg["covariate"]
        for oname,ocfg in c["primary_outcomes"].items():
            y=ocfg["variable"]
            for sec,svar in c["section_sensitivity"].items():
                l1=int(c["section_to_outcome_lags"][oname][sec]);l2=int(ocfg["mediator_to_outcome_lags"]["ekman"])
                d=align_parallel(df,driver,covar,svar,c["mediators"]["ekman"],y,l1,l2)
                pt=fit_parallel(d);boots=bootstrap_model(d,niter,block,seed,False)
                rec={"driver":driver,"covariate":covar,"outcome":oname,"section":sec,"section_variable":svar,
                     "section_to_outcome_lag":l1,"ekman_to_outcome_lag":l2,**pt}
                for eff in ["indirect_qout","indirect_ekman","total_indirect"]:
                    lo,hi,p,stab=boot_summary(pt,boots,eff)
                    rec[f"{eff}_ci_low"]=lo;rec[f"{eff}_ci_high"]=hi;rec[f"{eff}_boot_p"]=p;rec[f"{eff}_sign_stability"]=stab
                rows.append(rec)
    out=pd.DataFrame(rows)
    for eff in ["indirect_qout","indirect_ekman","total_indirect"]:
        out[f"{eff}_q_fdr"]=bh_fdr(out[f"{eff}_boot_p"].to_numpy())
    out.to_csv(ROOT/"reports/section_level_mediation_sensitivity.csv",index=False)
    print(out.to_string(index=False));L.info("Section sensitivity complete")
if __name__=="__main__":main()

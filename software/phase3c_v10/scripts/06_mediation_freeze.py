import numpy as np,pandas as pd
from common import ROOT,cfg,log

def sgn(x):
    return 1 if x>0 else -1 if x<0 else 0

def main():
    c=cfg();L=log("06_freeze")
    p=pd.read_csv(ROOT/"reports/primary_parallel_mediation.csv")
    sec=pd.read_csv(ROOT/"reports/section_level_mediation_sensitivity.csv")
    seas=pd.read_csv(ROOT/"reports/seasonal_SON_JJA_mediation_sensitivity.csv")
    alpha=float(c["analysis"]["fdr_alpha"]);mine=float(c["analysis"]["min_abs_indirect_effect"]);mins=float(c["analysis"]["min_sign_stability_fraction"])
    rows=[]
    for _,r in p.iterrows():
        for med,eff in [("qout","indirect_qout"),("ekman","indirect_ekman"),("parallel_total","total_indirect")]:
            val=float(r[eff]);q=float(r[f"{eff}_q_fdr"]);stab=float(r[f"{eff}_sign_stability"])
            ci_excludes=bool(r[f"{eff}_ci_low"]>0 or r[f"{eff}_ci_high"]<0)
            primary_pass=(q<=alpha and abs(val)>=mine and stab>=mins and ci_excludes)
            robust=np.nan;detail=""
            if med=="qout":
                z=sec[(sec.driver==r.driver)&(sec.outcome==r.outcome)]
                if len(z):
                    signs=[sgn(v) for v in z.indirect_qout]
                    robust=np.mean([x==sgn(val) for x in signs])
                    detail=f"section_sign_agreement={robust:.2f}"
                support=bool(np.isfinite(robust) and robust>=2/3)
            elif med=="ekman":
                z=seas[(seas.driver==r.driver)&(seas.outcome==r.outcome)]
                if len(z):
                    signs=[sgn(v) for v in z.indirect_ekman]
                    robust=np.mean([x==sgn(val) for x in signs])
                    sig_any=bool((z.indirect_ekman_q_fdr<=0.10).any())
                    detail=f"season_sign_agreement={robust:.2f};season_q<=0.10_any={sig_any}"
                    support=bool(robust>=0.5 and sig_any)
                else:support=False
            else:
                z=seas[(seas.driver==r.driver)&(seas.outcome==r.outcome)]
                robust=np.mean([sgn(v)==sgn(val) for v in z.total_indirect]) if len(z) else np.nan
                support=bool(np.isfinite(robust) and robust>=0.5)
                detail=f"season_total_sign_agreement={robust:.2f}" if np.isfinite(robust) else ""
            if primary_pass and support:status="FREEZE"
            elif primary_pass:status="CONDITIONAL"
            else:status="REVIEW"
            rows.append({
                "driver":r.driver,"outcome":r.outcome,"mediated_path":med,
                "effect":val,"ci_low":r[f"{eff}_ci_low"],"ci_high":r[f"{eff}_ci_high"],
                "q_fdr":q,"sign_stability":stab,"primary_pass":primary_pass,
                "robustness_metric":robust,"robustness_detail":detail,"freeze_status":status
            })
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/mediation_robustness_freeze.csv",index=False)
    print(out.to_string(index=False));L.info("Mediation freeze table complete")
if __name__=="__main__":main()

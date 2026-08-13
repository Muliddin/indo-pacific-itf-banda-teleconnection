import numpy as np,pandas as pd
from common import ROOT,cfg,log
def sign(x):
    if not np.isfinite(x) or x==0:return 0
    return 1 if x>0 else -1
def main():
    c=cfg();L=log("04_freeze")
    primary=pd.read_csv(ROOT/"reports/positive_lag_best_lags.csv")
    sens=pd.read_csv(ROOT/"reports/preprocessing_sensitivity_best_lags.csv")
    rows=[]
    for _,p in primary.iterrows():
        idx=p["index"]; target_full=p["target"]; target=target_full.replace("_anom_dt","")
        s=sens[(sens["index"]==idx)&(sens["target"]==target)]
        signs=[sign(v) for v in s.r_best]
        modal=max(set(signs),key=sign) if signs else 0
        agree=np.mean([x==modal for x in signs]) if signs else np.nan
        lagspread=(s.best_lag_r.max()-s.best_lag_r.min()) if len(s) else np.nan
        primary_sig=(p.q_pair_best_positive<=float(c["analysis"]["fdr_alpha"]))
        partial_sig=(p.q_partial_pair_best_positive<=float(c["analysis"]["fdr_alpha"]))
        effect_ok=abs(p.r_best_positive)>=float(c["analysis"]["min_abs_r_for_freeze"])
        sign_ok=agree>=float(c["analysis"]["min_preprocessing_sign_agreement_fraction"])
        lag_ok=lagspread<=float(c["analysis"]["max_best_lag_spread_months"])
        freeze=bool(primary_sig and effect_ok and sign_ok and lag_ok)
        status="FREEZE" if freeze else "REVIEW"
        reasons=[]
        if not primary_sig:reasons.append("primary correlation not pair-FDR significant")
        if not partial_sig:reasons.append("partial correlation not pair-FDR significant")
        if not effect_ok:reasons.append("effect size below threshold")
        if not sign_ok:reasons.append("preprocessing sign instability")
        if not lag_ok:reasons.append("best-lag spread exceeds threshold")
        rows.append({
            "index":idx,"target":target,
            "best_positive_lag":int(p.best_positive_lag_r),"r_best_positive":p.r_best_positive,
            "q_pair_best_positive":p.q_pair_best_positive,
            "best_positive_lag_partial":int(p.best_positive_lag_partial_r),
            "partial_r_best_positive":p.partial_r_best_positive,
            "q_partial_pair_best_positive":p.q_partial_pair_best_positive,
            "preprocessing_sign_agreement_fraction":agree,
            "preprocessing_best_lag_spread_months":lagspread,
            "primary_fdr_pass":primary_sig,"partial_fdr_pass":partial_sig,
            "effect_size_pass":effect_ok,"sign_robustness_pass":sign_ok,"lag_robustness_pass":lag_ok,
            "freeze_status":status,"review_notes":"; ".join(reasons)
        })
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/stage1_freeze_decision.csv",index=False)
    print(out.to_string(index=False))
    L.info("Freeze decision complete")
if __name__=="__main__":main()

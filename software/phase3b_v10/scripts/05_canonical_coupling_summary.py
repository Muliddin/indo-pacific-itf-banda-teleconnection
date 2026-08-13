import numpy as np,pandas as pd
from common import ROOT,cfg,log
def sgn(x):
    if not np.isfinite(x) or x==0:
        return 0
    return 1 if x>0 else -1
def main():
    c=cfg();L=log("05_canonical")
    best=pd.read_csv(ROOT/"reports/lagged_ITF_to_Banda_best_lags.csv")
    sens=pd.read_csv(ROOT/"reports/detrending_sensitivity_best_lags.csv")
    rows=[]
    for _,b in best.iterrows():
        pred=b.predictor.replace("_anom_dt","")
        resp=b.response.replace("_dt","")
        s=sens[(sens.predictor_base==pred)&(sens.response_base==resp)]
        signs=[sgn(v) for v in s.r_best]
        modal=max(set(signs),key=signs.count) if signs else 0
        agree=np.mean([x==modal for x in signs]) if signs else np.nan
        lagspread=s.best_lag_r.max()-s.best_lag_r.min() if len(s) else np.nan

        ordinary_sig=bool(b.q_pair_best<=float(c["analysis"]["fdr_alpha"]))
        partial_sig=bool(b.q_partial_pair_best<=float(c["analysis"]["fdr_alpha"]))
        effect=bool(abs(b.r_best)>=float(c["analysis"]["min_abs_r_canonical"]))
        sign_robust=bool(agree>=0.75)
        lag_robust=bool(lagspread<=4)

        if ordinary_sig and partial_sig and effect and sign_robust and lag_robust:
            status="CANONICAL"
        elif ordinary_sig and effect:
            status="CONDITIONAL"
        else:
            status="REVIEW"

        rows.append({
            "predictor":pred,"response":resp,
            "best_lag_itf_leads":int(b.best_lag_r),
            "r_best":b.r_best,"q_pair_best":b.q_pair_best,
            "best_lag_partial":int(b.best_lag_partial),
            "partial_r_best":b.partial_r_best,
            "q_partial_pair_best":b.q_partial_pair_best,
            "preprocessing_sign_agreement_fraction":agree,
            "preprocessing_best_lag_spread_months":lagspread,
            "ordinary_fdr_pass":ordinary_sig,
            "partial_fdr_pass":partial_sig,
            "effect_size_pass":effect,
            "sign_robustness_pass":sign_robust,
            "lag_robustness_pass":lag_robust,
            "coupling_status":status
        })
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/canonical_ITF_Banda_coupling.csv",index=False)
    print(out.to_string(index=False))
    L.info("Canonical coupling summary complete")
if __name__=="__main__":
    main()

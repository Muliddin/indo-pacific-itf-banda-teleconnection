import pandas as pd,numpy as np
from common import ROOT,cfg,log
def main():
    c=cfg();L=log("05_classify")
    comp=pd.read_csv(ROOT/"reports/single_vs_parallel_indirect_comparison.csv")
    com=pd.read_csv(ROOT/"reports/commonality_shared_variance.csv")
    vif=pd.read_csv(ROOT/"reports/mediator_vif_diagnostics.csv")
    pair_r=float(vif.pairwise_r.iloc[0]);v=float(vif.vif_two_predictor.iloc[0])
    rows=[]
    for _,r in comp.iterrows():
        cc=com[(com.driver==r.driver)&(com.outcome==r.outcome)]
        shared=float(cc.shared_qout_ekman.iloc[0]) if len(cc) else np.nan
        unique_q=float(cc.unique_qout.iloc[0]) if len(cc) else np.nan
        unique_e=float(cc.unique_ekman.iloc[0]) if len(cc) else np.nan
        if r.single_significant and not r.parallel_significant and bool(r.overlap_suppression_flag):
            status="SHARED_VARIANCE_OR_SUPPRESSION_SUPPORTED"
        elif r.single_significant and r.parallel_significant:
            status="INDEPENDENT_MEDIATION_SUPPORTED"
        elif not r.single_significant and not r.parallel_significant:
            status="NO_ROBUST_MEDIATION"
        else:
            status="MIXED"
        rows.append({"driver":r.driver,"outcome":r.outcome,"mediator":r.mediator,
                     "single_indirect":r.single_indirect,"single_q_fdr":r.single_q_fdr,
                     "parallel_indirect":r.parallel_indirect,"parallel_q_fdr":r.parallel_q_fdr,
                     "parallel_to_single_abs_ratio":r.parallel_to_single_abs_ratio,
                     "mediator_pair_r":pair_r,"mediator_vif":v,
                     "shared_added_r2":shared,"unique_qout_r2":unique_q,"unique_ekman_r2":unique_e,
                     "diagnostic_status":status})
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/mediation_collinearity_diagnostic_classification.csv",index=False)
    print(out.to_string(index=False));L.info("Diagnostic classification complete")
if __name__=="__main__":main()

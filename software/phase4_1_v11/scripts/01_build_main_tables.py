from common import *
def main():
    c=cfg();L=log("01_tables");p4=resolve(c["inputs"]["phase4_root"])
    # Table 1: validation summary
    total=pd.read_csv(p4/"tables/Table_1_total_outflow_validation.csv")
    sec=pd.read_csv(p4/"tables/Table_S1_ITF_section_validation.csv")
    t1=sec[["section_id","canonical_mean_2004_2006_sv","reference_mean_2004_2006_sv","relative_bias_percent"]].copy()
    t1.loc[len(t1)]=["TOTAL_OUTFLOW",
                     total.loc[0,"model_total_outflow_2004_2006_sv"],
                     total.loc[0,"instant_reference_sv"],
                     total.loc[0,"relative_bias_percent"]]
    t1.to_csv(ROOT/"tables/Table_1_ITF_validation_summary.csv",index=False)

    # Table 2: only robust core Stage 1 + concise fields
    s1=pd.read_csv(p4/"tables/Table_2_ENSO_IOD_ITF_lagged.csv")
    cols=[c for c in ["index","target","best_positive_lag","r_best_positive","q_pair_best_positive","best_positive_lag_partial","partial_r_best_positive","q_partial_pair_best_positive","freeze_status","review_notes"] if c in s1.columns]
    t2=s1[s1["freeze_status"]=="FREEZE"][cols].copy()
    t2.to_csv(ROOT/"tables/Table_2_Core_ENSO_IOD_ITF_findings.csv",index=False)

    # Table 3: synthesis of seasonal robust core + ITF-Banda conditional/canonical
    seas=pd.read_csv(p4/"tables/Table_3_seasonal_event_robustness.csv")
    coup=pd.read_csv(p4/"tables/Table_4_ITF_Banda_coupling.csv")
    skeep=seas[seas["freeze_status"]=="FREEZE"].copy()
    skeep["finding_group"]="seasonal_event"
    cstatus="coupling_status" if "coupling_status" in coup.columns else "freeze_status"
    ckeep=coup[coup[cstatus].isin(["CANONICAL","CONDITIONAL"])].copy()
    ckeep["finding_group"]="ITF_Banda_coupling"
    # normalize selected columns
    rows=[]
    for _,r in skeep.iterrows():
        rows.append({"finding_group":"seasonal_event","driver":r.get("index",""),
                     "target":r.get("target",""),"season":r.get("season",""),
                     "lag":r.get("frozen_lag",""),"effect":r.get("effect",r.get("r",np.nan)),
                     "q_fdr":r.get("q_fdr",np.nan),"status":"FREEZE"})
    for _,r in ckeep.iterrows():
        rows.append({"finding_group":"ITF_Banda_coupling","driver":r.get("predictor",""),
                     "target":r.get("response",""),"season":"",
                     "lag":r.get("best_lag_itf_leads",""),"effect":r.get("r_best",np.nan),
                     "q_fdr":r.get("q_pair_best",np.nan),"status":r.get(cstatus,"")})
    pd.DataFrame(rows).to_csv(ROOT/"tables/Table_3_Seasonal_and_Banda_Coupling_Synthesis.csv",index=False)
    L.info("Main tables written")
if __name__=="__main__":main()

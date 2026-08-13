from common import *
def main():
    c=cfg();L=log("00_preflight")
    p4=resolve(c["inputs"]["phase4_root"]);p41=resolve(c["inputs"]["phase4_1_root"])
    req=[
        p4/"tables/Table_1_total_outflow_validation.csv",
        p4/"tables/Table_2_ENSO_IOD_ITF_lagged.csv",
        p4/"tables/Table_3_seasonal_event_robustness.csv",
        p4/"tables/Table_4_ITF_Banda_coupling.csv",
        p4/"tables/Table_5_parallel_mediation.csv",
        p4/"tables/Table_S1_ITF_section_validation.csv",
        p4/"tables/Table_S2_commonality.csv",
        p41/"reports/claim_evidence_matrix.csv",
        p41/"reports/main_vs_supplementary_architecture.csv",
    ]
    rows=[];missing=[]
    for p in req:
        ok=p.exists();rows.append({"path":str(p),"exists":ok})
        if not ok:missing.append(str(p))
    pd.DataFrame(rows).to_csv(ROOT/"reports/preflight_inputs.csv",index=False)
    if missing:raise FileNotFoundError("Missing inputs:\n"+"\n".join(missing))
    L.info("Preflight PASS")
if __name__=="__main__":main()

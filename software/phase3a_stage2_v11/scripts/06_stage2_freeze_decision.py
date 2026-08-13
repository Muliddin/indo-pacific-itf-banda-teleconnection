import pandas as pd
from common import ROOT,cfg,log
def main():
    c=cfg();L=log("06_freeze")
    sy=pd.read_csv(ROOT/"reports/seasonal_year_correlations.csv")
    comp=pd.read_csv(ROOT/"reports/event_level_composites.csv")
    flags=pd.read_csv(ROOT/"reports/compound_event_robustness.csv")
    rows=[]
    for _,r in sy.iterrows():
        sig=bool(r.q_fdr_global<=float(c["analysis"]["fdr_alpha"]))
        effect=abs(r.r)>=float(c["analysis"]["min_abs_r_freeze"])
        status="FREEZE" if sig and effect else "CONDITIONAL" if sig or effect else "REVIEW"
        rows.append({
            "analysis_type":"seasonal_year","index":r["index"],"target":r["target"],"season":r["season"],
            "effect":r["r"],"q_fdr":r["q_fdr_global"],"sample_n":r["n_season_years"],
            "freeze_status":status
        })
    for _,r in comp.iterrows():
        fa=flags.loc[flags.event_class==r.group_a,"sample_size_flag"]
        fb=flags.loc[flags.event_class==r.group_b,"sample_size_flag"]
        sa=fa.iloc[0] if len(fa) else "INSUFFICIENT"
        sb=fb.iloc[0] if len(fb) else "INSUFFICIENT"
        sig=bool(r.q_fdr<=float(c["analysis"]["fdr_alpha"]))
        enough=(sa=="ADEQUATE" and sb=="ADEQUATE")
        limited=(sa!="INSUFFICIENT" and sb!="INSUFFICIENT")
        status="FREEZE" if sig and enough else "CONDITIONAL" if sig and limited else "REVIEW"
        rows.append({
            "analysis_type":"event_composite",
            "index":f"{r.group_a}_vs_{r.group_b}",
            "target":r.target,"season":"",
            "effect":r.difference_a_minus_b,"q_fdr":r.q_fdr,
            "sample_n":f"{r.n_events_a}/{r.n_events_b}",
            "freeze_status":status
        })
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/stage2_freeze_decision.csv",index=False)
    print(out.to_string(index=False))
    L.info("Stage2 freeze decision complete")
if __name__=="__main__":
    main()

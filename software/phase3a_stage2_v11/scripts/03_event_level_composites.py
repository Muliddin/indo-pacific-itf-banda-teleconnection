import pandas as pd, numpy as np
from common import ROOT,cfg,episode_bootstrap_diff,permutation_p,bh_fdr,log
def main():
    c=cfg();L=log("03_event_composites")
    ev=pd.read_csv(ROOT/"data/processed/event_episode_registry.csv",parse_dates=["start","end"])
    contrasts=[
        ("el_nino","la_nina"),
        ("positive_iod","negative_iod"),
        ("el_nino_pos_iod","la_nina_neg_iod")
    ]
    rows=[]
    for target in c["transport_targets"]:
        col=target+"_event_mean"
        for a,b in contrasts:
            aa=ev.loc[ev.event_class==a,col].dropna().to_numpy()
            bb=ev.loc[ev.event_class==b,col].dropna().to_numpy()
            if len(aa)<2 or len(bb)<2:
                continue
            obs,lo,hi=episode_bootstrap_diff(
                aa,bb,int(c["analysis"]["bootstrap_iterations"]),int(c["analysis"]["random_seed"])
            )
            p=permutation_p(
                aa,bb,int(c["analysis"]["permutation_iterations"]),int(c["analysis"]["random_seed"])
            )
            rows.append({
                "target":target,"group_a":a,"group_b":b,
                "n_events_a":len(aa),"n_events_b":len(bb),
                "mean_a":aa.mean(),"mean_b":bb.mean(),
                "difference_a_minus_b":obs,
                "bootstrap_ci_low":lo,"bootstrap_ci_high":hi,
                "permutation_p":p
            })
    out=pd.DataFrame(rows)
    out["q_fdr"]=bh_fdr(out.permutation_p.to_numpy())
    out["significant_fdr"]=out.q_fdr<=float(c["analysis"]["fdr_alpha"])
    out.to_csv(ROOT/"reports/event_level_composites.csv",index=False)
    print(out.to_string(index=False))
    L.info("Event-level composites complete")
if __name__=="__main__":
    main()

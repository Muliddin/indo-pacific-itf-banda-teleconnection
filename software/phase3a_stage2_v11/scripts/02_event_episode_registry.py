import pandas as pd, numpy as np
from common import ROOT,cfg,resolve,persistence_runs,log
def main():
    c=cfg();L=log("02_episode_registry")
    p10=resolve(c["inputs"]["phase3a_v10_root"])
    df=pd.read_csv(p10/"data/processed/analysis_master_anom_detrended_1993_2025.csv",parse_dates=["time"])
    th=c["event_thresholds"];m=int(th["persistence_months"])
    specs={
        "el_nino": df.nino34>=float(th["nino34_warm"]),
        "la_nina": df.nino34<=float(th["nino34_cold"]),
        "positive_iod": df.dmi>=float(th["dmi_positive"]),
        "negative_iod": df.dmi<=float(th["dmi_negative"]),
    }
    masks={}
    for name,cond in specs.items():
        keep=np.zeros(len(df),bool)
        for i,j in persistence_runs(cond):
            if j-i>=m:
                keep[i:j]=True
        masks[name]=keep

    classes={
        "el_nino": masks["el_nino"] & ~masks["positive_iod"] & ~masks["negative_iod"],
        "la_nina": masks["la_nina"] & ~masks["positive_iod"] & ~masks["negative_iod"],
        "positive_iod": masks["positive_iod"] & ~masks["el_nino"] & ~masks["la_nina"],
        "negative_iod": masks["negative_iod"] & ~masks["el_nino"] & ~masks["la_nina"],
        "el_nino_pos_iod": masks["el_nino"] & masks["positive_iod"],
        "el_nino_neg_iod": masks["el_nino"] & masks["negative_iod"],
        "la_nina_pos_iod": masks["la_nina"] & masks["positive_iod"],
        "la_nina_neg_iod": masks["la_nina"] & masks["negative_iod"],
    }

    rows=[];eid=1
    for cls,mask in classes.items():
        for i,j in persistence_runs(mask):
            sub=df.iloc[i:j]
            if len(sub)<1:
                continue
            row={
                "event_id":f"E{eid:03d}",
                "event_class":cls,
                "start":sub.time.iloc[0],
                "end":sub.time.iloc[-1],
                "duration_months":len(sub),
                "mean_nino34":sub.nino34.mean(),
                "mean_dmi":sub.dmi.mean(),
                "peak_nino34_abs":sub.nino34.abs().max(),
                "peak_dmi_abs":sub.dmi.abs().max(),
            }
            for target in c["transport_targets"]:
                row[target+"_event_mean"]=sub[target].mean()
            rows.append(row);eid+=1
    out=pd.DataFrame(rows).sort_values(["start","event_class"])
    out.to_csv(ROOT/"data/processed/event_episode_registry.csv",index=False,date_format="%Y-%m-%d")
    counts=out.event_class.value_counts().rename_axis("event_class").reset_index(name="n_events")
    counts.to_csv(ROOT/"reports/event_episode_counts.csv",index=False)
    print(counts.to_string(index=False))
    L.info("Event episode registry complete")
if __name__=="__main__":
    main()

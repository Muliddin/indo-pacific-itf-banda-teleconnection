import pandas as pd
from common import ROOT,cfg,log
def main():
    c=cfg();L=log("04_sample_flags")
    ev=pd.read_csv(ROOT/"data/processed/event_episode_registry.csv")
    counts=ev.event_class.value_counts()
    rows=[]
    for cls,n in counts.items():
        if n>=int(c["analysis"]["min_events_freeze"]):
            status="ADEQUATE"
        elif n>=int(c["analysis"]["min_events_conditional"]):
            status="LIMITED"
        else:
            status="INSUFFICIENT"
        rows.append({"event_class":cls,"n_independent_events":int(n),"sample_size_flag":status})
    out=pd.DataFrame(rows).sort_values("event_class")
    out.to_csv(ROOT/"reports/compound_event_robustness.csv",index=False)
    print(out.to_string(index=False))
    L.info("Sample-size flags complete")
if __name__=="__main__":
    main()

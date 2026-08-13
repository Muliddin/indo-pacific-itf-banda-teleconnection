import pandas as pd
from common import ROOT,cfg,phase2b_root,expected_time,log
def main():
    c=cfg(); L=log("03_climate_indices"); p2b=phase2b_root(c)
    n=pd.read_csv(p2b/"data/raw/noaa_indices/nino34_canonical.csv",parse_dates=["time"])
    d=pd.read_csv(p2b/"data/raw/noaa_indices/dmi_canonical.csv",parse_dates=["time"])
    x=n.merge(d,on="time",how="outer").sort_values("time").reset_index(drop=True)
    exp=expected_time(c)
    if len(x)!=len(exp) or len(exp.difference(pd.DatetimeIndex(x.time))): raise RuntimeError("Climate index calendar mismatch")
    if x[["nino34","dmi"]].isna().any().any(): raise RuntimeError("Climate indices contain missing values")
    for v in ["nino34","dmi"]: x[v+"_z"]=(x[v]-x[v].mean())/x[v].std(ddof=1)
    out=ROOT/c["outputs"]["climate_indices_csv"]; out.parent.mkdir(parents=True,exist_ok=True)
    x.to_csv(out,index=False,date_format="%Y-%m-%d"); L.info("Wrote %s rows=%d",out,len(x)); print(out)
if __name__=="__main__": main()

import pandas as pd
from common import ROOT,cfg,resolve,log
def main():
    c=cfg();L=log("01_build_master")
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    pb=resolve(c["inputs"]["phase3b_v11_root"])
    a=pd.read_csv(p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",parse_dates=["time"])
    e=pd.read_csv(pb/"data/processed/full_ekman_pumping_banda_1993_2025.csv",parse_dates=["time"])
    x=a.merge(e[["time","full_ekman_pumping_banda_anom_dt"]],on="time",validate="one_to_one")
    needed=["time","nino34","dmi",c["mediators"]["qout"],c["mediators"]["ekman"]]
    needed += [v["variable"] for v in c["primary_outcomes"].values()]
    needed += [v["variable"] for v in c["secondary_outcomes"].values()]
    needed += list(c["section_sensitivity"].values())
    missing=[v for v in needed if v not in x.columns]
    if missing:raise RuntimeError(f"Missing mediation variables: {missing}")
    out=x[needed].copy()
    if len(out)!=396 or out.isna().any().any():
        raise RuntimeError(f"Mediation master invalid rows={len(out)} missing={out.columns[out.isna().any()].tolist()}")
    p=ROOT/"data/processed/mediation_master_1993_2025.csv"
    out.to_csv(p,index=False,date_format="%Y-%m-%d")
    print(p);L.info("Mediation master rows=%d cols=%d",len(out),len(out.columns))
if __name__=="__main__":main()

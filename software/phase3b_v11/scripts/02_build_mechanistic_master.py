import pandas as pd
from common import ROOT,cfg,resolve,log
def main():
    c=cfg();L=log("02_build")
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    m=pd.read_csv(p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",parse_dates=["time"])
    e=pd.read_csv(ROOT/"data/processed/full_ekman_pumping_banda_1993_2025.csv",parse_dates=["time"])
    x=m.merge(e[["time","full_ekman_pumping","full_ekman_pumping_banda_anom",
                 "full_ekman_pumping_banda_anom_dt"]],on="time",validate="one_to_one")
    if len(x)!=396 or x.isna().any().any():
        bad=x.columns[x.isna().any()].tolist()
        raise RuntimeError(f"Mechanistic master failed: rows={len(x)}, missing={bad}")
    out=ROOT/"data/processed/mechanistic_master_1993_2025.csv"
    x.to_csv(out,index=False,date_format="%Y-%m-%d")
    print(out)
    L.info("Mechanistic master rows=%d cols=%d",len(x),len(x.columns))
if __name__=="__main__":main()

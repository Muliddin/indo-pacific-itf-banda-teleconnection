import pandas as pd
from common import ROOT,cfg,resolve,log
def main():
    c=cfg();L=log("01_build_table")
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    df=pd.read_csv(p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",parse_dates=["time"])
    keep=["time","nino34","dmi","nino34_dt","dmi_dt"]
    for base in c["transport_predictors"]:
        keep += [base,base+"_anom",base+"_anom_dt"]
    for resp in c["banda_responses"]:
        keep += [resp,resp+"_dt"]
    keep=[x for x in keep if x in df.columns]
    out=df[keep].copy()
    if len(out)!=396:
        raise RuntimeError(f"Expected 396 rows, got {len(out)}")
    if out.time.duplicated().any():
        raise RuntimeError("Duplicate timestamps in coupling table")
    if out.isna().any().any():
        raise RuntimeError(f"Missing values in {out.columns[out.isna().any()].tolist()}")
    p=ROOT/"data/processed/coupling_master_1993_2025.csv"
    p.parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(p,index=False,date_format="%Y-%m-%d")
    L.info("Coupling table rows=%d cols=%d",len(out),len(out.columns))
    print(p)
if __name__=="__main__":
    main()

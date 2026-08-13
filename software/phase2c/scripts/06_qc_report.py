import json, pandas as pd, xarray as xr
from common import ROOT,cfg,log
def main():
    c=cfg(); L=log("06_qc"); checks=[]
    for k in ["glorys_monthly","era5_monthly","duacs_monthly","derived_gridded"]:
        p=ROOT/c["outputs"][k]
        try:
            with xr.open_dataset(p) as ds: checks.append({"file":str(p.relative_to(ROOT)),"ok":True,"dims":{a:int(b) for a,b in ds.sizes.items()},"vars":list(ds.data_vars)})
        except Exception as e: checks.append({"file":str(p.relative_to(ROOT)),"ok":False,"error":str(e)})
    for k in ["climate_indices_csv","regional_indices_csv","harmonized_timeseries"]:
        p=ROOT/c["outputs"][k]
        try:
            df=pd.read_csv(p); checks.append({"file":str(p.relative_to(ROOT)),"ok":True,"rows":len(df),"columns":list(df.columns),"missing_cells":int(df.isna().sum().sum())})
        except Exception as e: checks.append({"file":str(p.relative_to(ROOT)),"ok":False,"error":str(e)})
    out=ROOT/"reports/phase2c_qc_report.json"; out.write_text(json.dumps(checks,indent=2),encoding="utf-8")
    bad=[x for x in checks if not x["ok"]]; L.info("QC checks=%d failures=%d",len(checks),len(bad))
    if bad: raise SystemExit(3)
    print(out)
if __name__=="__main__": main()

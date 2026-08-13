import numpy as np, pandas as pd, xarray as xr
from common import ROOT,cfg,log,assert_monthly_time
def awmean(da):
    return da.weighted(np.cos(np.deg2rad(da.latitude))).mean(("latitude","longitude"),skipna=True)
def main():
    c=cfg(); L=log("05_harmonize")
    climate=pd.read_csv(ROOT/c["outputs"]["climate_indices_csv"],parse_dates=["time"])
    regional=pd.read_csv(ROOT/c["outputs"]["regional_indices_csv"],parse_dates=["time"])
    d=xr.open_dataset(ROOT/c["outputs"]["duacs_monthly"]); assert_monthly_time(d,"DUACS")
    du=xr.Dataset({"sla_banda":awmean(d.sla),"adt_banda":awmean(d.adt),"ugos_banda":awmean(d.ugos),
                   "vgos_banda":awmean(d.vgos),"ugosa_banda":awmean(d.ugosa),"vgosa_banda":awmean(d.vgosa)}).to_dataframe().reset_index()
    du["time"]=pd.to_datetime(du.time).dt.to_period("M").dt.to_timestamp()
    x=climate.merge(regional,on="time",how="inner").merge(du,on="time",how="inner").sort_values("time")
    if len(x)!=int(c["analysis"]["expected_months"]): raise RuntimeError(f"Harmonized rows={len(x)}")
    if x.time.duplicated().any(): raise RuntimeError("Duplicate timestamps")
    out=ROOT/c["outputs"]["harmonized_timeseries"]; out.parent.mkdir(parents=True,exist_ok=True)
    x.to_csv(out,index=False,date_format="%Y-%m-%d"); d.close()
    L.info("Harmonized rows=%d cols=%d -> %s",len(x),len(x.columns),out); print(out)
if __name__=="__main__": main()

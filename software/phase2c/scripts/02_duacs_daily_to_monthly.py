import xarray as xr
from common import cfg,phase2b_root,log,normalize_month_start,assert_monthly_time,write_netcdf
def main():
    c=cfg(); L=log("02_duacs_monthly"); p2b=phase2b_root(c)
    files=[p for p in sorted((p2b/"data/raw/duacs").glob("duacs_daily_banda_*.nc")) if "_TEST" not in p.name and ".partial" not in p.name]
    if not files: raise RuntimeError("No production DUACS daily files found")
    L.info("DUACS annual daily files=%d",len(files))
    ds=xr.open_mfdataset(files,combine="by_coords",parallel=False)
    monthly=normalize_month_start(ds.resample(time="MS").mean(skipna=True,keep_attrs=True))
    assert_monthly_time(monthly,"DUACS monthly")
    monthly.attrs["phase2c_processing"]="Daily DUACS resampled to monthly mean with xarray"
    out=write_netcdf(monthly,c["outputs"]["duacs_monthly"])
    ds.close(); monthly.close(); print(out)
if __name__=="__main__": main()

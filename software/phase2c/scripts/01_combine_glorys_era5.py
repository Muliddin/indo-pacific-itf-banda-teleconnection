#!/usr/bin/env python3
import numpy as np
import pandas as pd
import xarray as xr
from common import cfg, phase2b_root, log, normalize_month_start, assert_monthly_time, write_netcdf

ERA5_EXPECTED = [
    "sst", "avg_iews", "avg_inss", "avg_ishf",
    "avg_slhtf", "avg_snswrf", "avg_snlwrf"
]

def combine_glorys(folder):
    files=[p for p in sorted(folder.glob("glorys_banda_monthly_*.nc"))
           if "_TEST" not in p.name and ".partial" not in p.name]
    if not files:
        raise RuntimeError("GLORYS: no production files found")
    L=log("01_combine")
    L.info("GLORYS files=%d",len(files))
    ds=xr.open_mfdataset(files,combine="by_coords",parallel=False)
    ds=normalize_month_start(ds)
    _,idx=np.unique(ds["time"].values,return_index=True)
    ds=ds.isel(time=sorted(idx))
    assert_monthly_time(ds,"GLORYS")
    return ds

def normalize_era5_annual(path, logger):
    ds=xr.open_dataset(path)

    if "valid_time" in ds.coords or "valid_time" in ds.dims:
        ds=ds.rename({"valid_time":"time"})
    elif "time" not in ds.coords and "time" not in ds.dims:
        raise RuntimeError(
            f"{path.name}: no time coordinate; coords={list(ds.coords)} dims={list(ds.dims)}"
        )

    original=pd.to_datetime(ds["time"].values)
    month_start=pd.DatetimeIndex(original).to_period("M").to_timestamp()
    ds=ds.assign_coords(time=month_start)

    # Multiple within-month timestamps (e.g. 00:00 and 06:00) become one
    # monthly label. first(skipna=True) preserves the valid value from
    # complementary parameter groups.
    ds=ds.groupby("time").first(skipna=True)

    missing=set(ERA5_EXPECTED)-set(ds.data_vars)
    if missing:
        raise RuntimeError(f"{path.name}: missing ERA5 variables {sorted(missing)}")

    if ds.sizes.get("time",0)!=12:
        raise RuntimeError(
            f"{path.name}: expected 12 months after normalization, got {ds.sizes.get('time',0)}"
        )

    for v in ERA5_EXPECTED:
        counts=ds[v].count(dim=["latitude","longitude"])
        if bool((counts==0).any()):
            bad=ds["time"].where(counts==0,drop=True)
            bad_dates=pd.to_datetime(bad.values).strftime("%Y-%m").tolist()
            raise RuntimeError(f"{path.name}: {v} has no valid cells at {bad_dates}")

    logger.info("%s: %d raw timestamps -> %d monthly timestamps",
                path.name,len(original),ds.sizes["time"])
    return ds

def combine_era5(folder):
    files=[p for p in sorted(folder.glob("era5_banda_monthly_*.nc"))
           if "_TEST" not in p.name and ".partial" not in p.name]
    if not files:
        raise RuntimeError("ERA5: no production files found")
    L=log("01_combine")
    L.info("ERA5 files=%d",len(files))
    annual=[]
    for p in files:
        annual.append(normalize_era5_annual(p,L))

    combined=xr.concat(
        annual,
        dim="time",
        data_vars="all",
        coords="minimal",
        compat="override",
        join="exact"
    ).sortby("time")

    t=pd.DatetimeIndex(pd.to_datetime(combined["time"].values))
    if t.duplicated().any():
        raise RuntimeError("ERA5 duplicate months remain after normalization")

    assert_monthly_time(combined,"ERA5")

    for v in ERA5_EXPECTED:
        counts=combined[v].count(dim=["latitude","longitude"])
        if bool((counts==0).any()):
            bad=combined["time"].where(counts==0,drop=True)
            bad_dates=pd.to_datetime(bad.values).strftime("%Y-%m").tolist()
            raise RuntimeError(f"ERA5 combined {v}: zero valid cells at {bad_dates[:10]}")

    return combined, annual

def main():
    c=cfg()
    p2b=phase2b_root(c)

    g=combine_glorys(p2b/"data/raw/glorys")
    gp=write_netcdf(g,c["outputs"]["glorys_monthly"])
    g.close()

    e,annual=combine_era5(p2b/"data/raw/era5")
    ep=write_netcdf(e,c["outputs"]["era5_monthly"])
    e.close()
    for ds in annual:
        try: ds.close()
        except Exception: pass

    print("COMBINE SUCCESS")
    print("GLORYS:",gp)
    print("ERA5  :",ep)

if __name__=="__main__":
    main()

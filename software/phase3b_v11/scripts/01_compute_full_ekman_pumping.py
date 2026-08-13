import numpy as np,pandas as pd,xarray as xr
from common import ROOT,cfg,resolve,find_era5_gridded,monthly_anomaly,linear_detrend,log

def main():
    c=cfg();L=log("01_full_ekman")
    p2=resolve(c["inputs"]["phase2c_root"])
    vx=c["variables"]["era5_tau_x"];vy=c["variables"]["era5_tau_y"];vsst=c["variables"]["era5_sst"]
    src=find_era5_gridded(p2,vx,vy)
    ds=xr.open_dataset(src)

    if "valid_time" in ds.coords and "time" not in ds.coords:
        ds=ds.rename({"valid_time":"time"})
    if "latitude" not in ds.coords or "longitude" not in ds.coords:
        raise RuntimeError("ERA5 source must have latitude/longitude")

    ds=ds.sel(time=slice(c["analysis"]["start"],c["analysis"]["end"]))
    if ds.sizes.get("time",0)!=396:
        raise RuntimeError(f"Expected 396 months, found {ds.sizes.get('time',0)}")

    rho=float(c["analysis"]["rho0_kg_m3"])
    om=float(c["analysis"]["omega_rad_s"])
    R=float(c["analysis"]["earth_radius_m"])
    latr=np.deg2rad(ds.latitude)
    f=2*om*np.sin(latr)
    f=xr.where(abs(f)<1e-6,np.nan,f)

    tx=ds[vx].astype("float64")
    ty=ds[vy].astype("float64")
    qx=tx/(rho*f)
    qy=ty/(rho*f)

    # differentiate() returns derivative per degree; convert to derivative per radian.
    dqydlon=qy.differentiate("longitude")*(180.0/np.pi)
    dqx_dlat=qx.differentiate("latitude")*(180.0/np.pi)
    dqydx=dqydlon/(R*np.cos(latr))
    dqxdy=dqx_dlat/R
    wek=(dqydx-dqxdy).rename("full_ekman_pumping")

    if vsst in ds:
        ocean=ds[vsst].notnull()
        if "time" in ocean.dims:
            ocean=ocean.any("time")
        wek=wek.where(ocean)

    weights=np.cos(latr)
    regional=wek.weighted(weights).mean(("latitude","longitude"),skipna=True)
    df=regional.to_dataframe().reset_index()
    df["time"]=pd.to_datetime(df.time).dt.to_period("M").dt.to_timestamp()

    an=monthly_anomaly(df.full_ekman_pumping,df.time,
        c["analysis"]["climatology_start"],c["analysis"]["climatology_end"])
    dt,slope=linear_detrend(an,df.time)
    df["full_ekman_pumping_banda_anom"]=an
    df["full_ekman_pumping_banda_anom_dt"]=dt
    df["trend_per_year"]=slope

    out=ROOT/"data/processed/full_ekman_pumping_banda_1993_2025.csv"
    out.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(out,index=False,date_format="%Y-%m-%d")
    L.info("ERA5 source: %s",src)
    L.info("Full Ekman -> %s",out)
    print(df.head().to_string(index=False))
    print("WROTE",out)
    ds.close()

if __name__=="__main__":main()

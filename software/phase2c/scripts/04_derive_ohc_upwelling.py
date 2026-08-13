import numpy as np
import pandas as pd
import xarray as xr
from common import ROOT,cfg,log,assert_monthly_time,write_netcdf

def layer_edges(z):
    z=np.asarray(z,float)
    e=np.empty(len(z)+1)
    e[1:-1]=(z[:-1]+z[1:])/2
    e[0]=max(0.0,z[0]-(z[1]-z[0])/2)
    e[-1]=z[-1]+(z[-1]-z[-2])/2
    return e

def ohc(thetao,max_depth,rho,cp,tref):
    z=thetao.depth.values
    e=layer_edges(z)
    eff=np.maximum(0,np.minimum(e[1:],max_depth)-e[:-1])
    dz=xr.DataArray(eff,coords={"depth":thetao.depth},dims=["depth"])
    out=(rho*cp*((thetao-tref)*dz).sum("depth",skipna=True)).rename(f"ohc_{int(max_depth)}m")
    out.attrs["units"]="J m-2"
    return out

def awmean(da):
    return da.weighted(np.cos(np.deg2rad(da.latitude))).mean(("latitude","longitude"),skipna=True)

def curl_tau(taux,tauy,R):
    deg_to_rad=np.pi/180.0
    coslat=np.cos(np.deg2rad(taux.latitude))
    coslat=xr.where(np.abs(coslat)<1e-8,np.nan,coslat)

    dtauy_dlon_deg=tauy.differentiate("longitude")
    dtaux_dlat_deg=taux.differentiate("latitude")

    dtauy_dx=dtauy_dlon_deg/(R*coslat*deg_to_rad)
    dtaux_dy=dtaux_dlat_deg/(R*deg_to_rad)

    curl=(dtauy_dx-dtaux_dy).rename("wind_stress_curl")
    curl.attrs["units"]="N m-3"
    return curl

def main():
    c=cfg(); L=log("04_derive")
    g=xr.open_dataset(ROOT/c["outputs"]["glorys_monthly"],chunks={"time":12})
    e=xr.open_dataset(ROOT/c["outputs"]["era5_monthly"],chunks={"time":12})
    assert_monthly_time(g,"GLORYS"); assert_monthly_time(e,"ERA5")

    oc=c["ohc"]; up=c["upwelling"]
    rho=float(oc["rho0_kg_m3"]); cp=float(oc["cp_j_kg_k"]); tref=float(oc["reference_temperature_c"])

    o300=ohc(g.thetao,float(oc["primary_max_depth_m"]),rho,cp,tref)
    o700=ohc(g.thetao,float(oc["sensitivity_max_depth_m"]),rho,cp,tref)
    sst=g.thetao.isel(depth=0,drop=True).rename("sst_glorys")
    mld=g.mlotst.rename("mld")

    taux=e.avg_iews.rename("taux")
    tauy=e.avg_inss.rename("tauy")
    taumag=np.hypot(taux,tauy).rename("wind_stress_magnitude")
    curl=curl_tau(taux,tauy,float(up["earth_radius_m"]))

    omega=float(up["earth_omega_s_1"]); rho0=float(up["rho0_kg_m3"])
    f=2*omega*np.sin(np.deg2rad(curl.latitude))
    f=xr.DataArray(f,coords={"latitude":curl.latitude},dims=["latitude"])
    f=f.where(np.abs(f)>=float(up["minimum_abs_coriolis_s_1"]))

    wek=(curl/(rho0*f)).rename("ekman_pumping_proxy")
    wek.attrs["units"]="m s-1"
    wek.attrs["note"]="Diagnostic proxy curl(tau)/(rho0*f), not full curl(tau/(rho*f))."

    derived=xr.Dataset({
        "ohc_300m":o300,
        "ohc_700m":o700,
        "sst_glorys":sst,
        "mld":mld,
        "wind_stress_magnitude":taumag,
        "wind_stress_curl":curl,
        "ekman_pumping_proxy":wek,
    })
    gout=write_netcdf(derived,c["outputs"]["derived_gridded"])

    ts=xr.Dataset({
        "ohc300_banda":awmean(o300),
        "ohc700_banda":awmean(o700),
        "sst_banda":awmean(sst),
        "mld_banda":awmean(mld),
        "tau_banda":awmean(taumag),
        "curl_tau_banda":awmean(curl),
        "wek_banda":awmean(wek),
    }).to_dataframe().reset_index()

        # ---------------------------------------------------------
    # Monthly climatology and anomalies
    # ---------------------------------------------------------

    t = pd.to_datetime(ts["time"])

    base = (
        (t >= pd.Timestamp(c["analysis"]["climatology_start"]))
        &
        (t <= pd.Timestamp(c["analysis"]["climatology_end"]))
    )

    if base.sum() == 0:
        raise RuntimeError(
            "Climatology baseline contains zero months."
        )

    regional_vars = [
        "ohc300_banda",
        "ohc700_banda",
        "sst_banda",
        "mld_banda",
        "tau_banda",
        "curl_tau_banda",
        "wek_banda",
    ]

    for v in regional_vars:

        if v not in ts.columns:
            raise RuntimeError(
                f"Expected regional variable '{v}' not found. "
                f"Available columns: {list(ts.columns)}"
            )

        ts[v] = pd.to_numeric(
            ts[v],
            errors="coerce"
        )

        if ts[v].isna().any():
            bad_times = (
                ts.loc[ts[v].isna(), "time"]
                .astype(str)
                .tolist()[:10]
            )

            raise RuntimeError(
                f"{v} contains missing/non-numeric values. "
                f"First affected timestamps: {bad_times}"
            )

        tmp = pd.DataFrame({
            "time": t[base].to_numpy(),
            "value": ts.loc[base, v].to_numpy(),
        })

        tmp["month"] = tmp["time"].dt.month

        climatology = (
            tmp
            .groupby("month")["value"]
            .mean()
        )

        month_number = t.dt.month

        ts[v + "_anom"] = (
            ts[v].to_numpy()
            -
            month_number.map(climatology).to_numpy()
        )
    
    pout=ROOT/c["outputs"]["regional_indices_csv"]
    pout.parent.mkdir(parents=True,exist_ok=True)
    ts.to_csv(pout,index=False,date_format="%Y-%m-%d")

    g.close(); e.close(); derived.close()
    L.info("Derived outputs: %s ; %s",gout,pout)
    print("DERIVED METRICS SUCCESS")
    print(gout)
    print(pout)

if __name__=="__main__":
    main()

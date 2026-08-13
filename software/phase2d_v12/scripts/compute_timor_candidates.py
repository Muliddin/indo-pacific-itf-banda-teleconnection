from pathlib import Path
import csv
import numpy as np,pandas as pd,xarray as xr
ROOT=Path(__file__).resolve().parents[1];R=6371000.0
def dz(z,maxd):
    z=np.asarray(z,float);e=np.empty(len(z)+1);e[1:-1]=(z[:-1]+z[1:])/2
    e[0]=max(0,z[0]-(z[1]-z[0])/2);e[-1]=z[-1]+(z[-1]-z[-2])/2
    return np.maximum(0,np.minimum(e[1:],maxd)-e[:-1])
def endpoint(clat,clon,az,km):
    az=np.deg2rad(az);dy=km*1000*np.cos(az);dx=km*1000*np.sin(az)
    return clat+np.rad2deg(dy/R),clon+np.rad2deg(dx/(R*np.cos(np.deg2rad(clat))))
def transect(clat,clon,az,Lkm,off):
    # perpendicular offset ~1 native GLORYS cell per step
    p_lat,p_lon=endpoint(clat,clon,az+90,off*9.25)
    a=endpoint(p_lat,p_lon,az,-Lkm/2);b=endpoint(p_lat,p_lon,az,Lkm/2)
    return a,b
def widths(n,Lm):
    d=Lm/(n-1);w=np.full(n,d);w[0]=w[-1]=d/2;return w
def main():
    (ROOT / "data" / "processed" / "candidates").mkdir(
        parents=True,
        exist_ok=True
    )

    (ROOT / "data" / "processed" / "canonical").mkdir(
        parents=True,
        exist_ok=True
    )

    (ROOT / "reports").mkdir(
        parents=True,
        exist_ok=True
    )
    with (ROOT/"timor_section_registry_v1.2.csv").open(encoding="utf-8") as f:r=next(csv.DictReader(f))
    files=[p for p in sorted((ROOT/"data/raw/timor").glob("glorys_timor_*.nc")) if ".partial" not in p.name]
    if not files:raise SystemExit("No Timor raw files")
    ds=xr.open_mfdataset(files,combine="by_coords",parallel=False)
    clat=float(r["center_lat"]);clon=float(r["center_lon"]);az=float(r["azimuth_deg_east_of_north"]);Lkm=float(r["section_length_km"]);maxd=float(r["integration_max_depth_m"])
    # right normal to tangent; for az=158°, points SW-ish toward Indian Ocean
    azr=np.deg2rad(az);ne=np.cos(azr);nn=-np.sin(azr)
    frames=[]
    for off in range(-3,4):
        (la1,lo1),(la2,lo2)=transect(clat,clon,az,Lkm,off)
        n=25;s=np.linspace(0,1,n);lats=la1+s*(la2-la1);lons=lo1+s*(lo2-lo1)
        sec=xr.DataArray(np.arange(n),dims="section")
        lat=xr.DataArray(lats,dims="section",coords={"section":sec});lon=xr.DataArray(lons,dims="section",coords={"section":sec})
        u=ds.uo.interp(latitude=lat,longitude=lon,method="nearest");v=ds.vo.interp(latitude=lat,longitude=lon,method="nearest")
        vn=u*ne+v*nn
        dza=xr.DataArray(dz(ds.depth.values,maxd),coords={"depth":ds.depth},dims=["depth"]);wa=xr.DataArray(widths(n,Lkm*1000),coords={"section":sec},dims=["section"])
        q=((vn*(dza*wa)).where(vn.notnull()).sum(("depth","section"),skipna=True)/1e6)
        dz300=xr.DataArray(dz(ds.depth.values,300),coords={"depth":ds.depth},dims=["depth"])
        q300=((vn*(dz300*wa)).where(vn.notnull()).sum(("depth","section"),skipna=True)/1e6)
        wet=vn.notnull().any("depth").mean("section")
        out=xr.Dataset({"transport_indian_positive_sv":q,"transport_literature_sign_sv":-q,
                        "transport_0_300m_indian_positive_sv":q300,"transport_below_300m_indian_positive_sv":q-q300,
                        "wet_column_fraction":wet})
        df=out.to_dataframe().reset_index();df["time"]=pd.to_datetime(df.time).dt.to_period("M").dt.to_timestamp()
        df["offset_grid_cells"]=off;df["section_id"]="timor"
        df["endpoint1_lat"]=la1;df["endpoint1_lon"]=lo1;df["endpoint2_lat"]=la2;df["endpoint2_lon"]=lo2
        p=ROOT/"data/processed/candidates"/f"transport_timor_offset_{off:+d}.csv";df.to_csv(p,index=False,date_format="%Y-%m-%d");frames.append(df);print("WROTE",p)
    pd.concat(frames).to_csv(ROOT/"data/processed/timor_candidates_1993_2025.csv",index=False,date_format="%Y-%m-%d");ds.close()
if __name__=="__main__":main()

from pathlib import Path
import argparse,time
import copernicusmarine,xarray as xr
ROOT=Path(__file__).resolve().parents[1]
DATASET="cmems_mod_glo_phy_my_0.083deg_P1M-m"
BBOX=(122.20,123.20,-11.85,-10.75)
MAXDEPTH=2000.0
def valid(p):
    if not p.exists() or p.stat().st_size<1024:return False
    try:
        with xr.open_dataset(p) as ds:return all(v in ds for v in ["uo","vo"]) and "time" in ds.coords
    except:return False
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--start-year",type=int,default=1993);ap.add_argument("--end-year",type=int,default=2025);a=ap.parse_args()
    out=ROOT/"data/raw/timor";out.mkdir(parents=True,exist_ok=True);W,E,S,N=BBOX
    for y in range(a.start_year,a.end_year+1):
        final=out/f"glorys_timor_{y}.nc";tmp=out/f"glorys_timor_{y}.partial.nc"
        if valid(final):print("SKIP",final);continue
        delay=15
        for i in range(1,6):
            try:
                tmp.unlink(missing_ok=True)
                copernicusmarine.subset(dataset_id=DATASET,variables=["uo","vo"],minimum_longitude=W,maximum_longitude=E,
                    minimum_latitude=S,maximum_latitude=N,minimum_depth=0,maximum_depth=MAXDEPTH,
                    start_datetime=f"{y}-01-01",end_datetime=f"{y}-12-31",
                    output_filename=tmp.name,output_directory=str(out),file_format="netcdf",coordinates_selection_method="inside")
                if not valid(tmp):raise RuntimeError("download validation failed")
                tmp.replace(final);print("WROTE",final);break
            except Exception:
                if i==5:raise
                time.sleep(delay);delay*=2
if __name__=="__main__":main()

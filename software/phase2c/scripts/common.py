from pathlib import Path
import logging, yaml, pandas as pd, xarray as xr

ROOT=Path(__file__).resolve().parents[1]

def cfg():
    return yaml.safe_load((ROOT/"config/preprocessing_config.yaml").read_text(encoding="utf-8"))

def phase2b_root(c=None):
    c=c or cfg()
    p=Path(c["project"]["phase2b_root"])
    return p if p.is_absolute() else (ROOT/p).resolve()

def log(name):
    (ROOT/"logs").mkdir(parents=True,exist_ok=True)
    L=logging.getLogger(name)
    if L.handlers: return L
    L.setLevel(logging.INFO)
    fmt=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh=logging.FileHandler(ROOT/"logs"/f"{name}.log",encoding="utf-8"); fh.setFormatter(fmt)
    sh=logging.StreamHandler(); sh.setFormatter(fmt)
    L.addHandler(fh); L.addHandler(sh)
    return L

def expected_time(c=None):
    c=c or cfg()
    return pd.date_range(c["analysis"]["start"],c["analysis"]["end"],freq=c["analysis"]["frequency"])

def normalize_month_start(ds):
    # Normalize time coordinate names across GLORYS / ERA5 / DUACS
    if "time" in ds.coords:
        time_name = "time"
    elif "valid_time" in ds.coords:
        time_name = "valid_time"
    elif "time" in ds.dims:
        time_name = "time"
    elif "valid_time" in ds.dims:
        time_name = "valid_time"
    else:
        raise RuntimeError(
            f"No recognizable time coordinate. "
            f"coords={list(ds.coords)}, dims={list(ds.dims)}"
        )

    # Rename ERA5 valid_time -> time
    if time_name != "time":
        ds = ds.rename({time_name: "time"})

    t = pd.to_datetime(ds["time"].values)

    ds = ds.assign_coords(
        time=pd.DatetimeIndex(t).to_period("M").to_timestamp()
    )

    return ds.sortby("time")

def assert_monthly_time(ds, label, c=None):
    c = c or cfg()

    if "time" not in ds.coords and "time" not in ds.dims:
        raise RuntimeError(
            f"{label}: no 'time' coordinate after normalization. "
            f"coords={list(ds.coords)}, dims={list(ds.dims)}"
        )

    exp = expected_time(c)
    got = pd.DatetimeIndex(pd.to_datetime(ds["time"].values))

    if len(got) != len(exp):
        raise RuntimeError(
            f"{label}: expected {len(exp)} months, got {len(got)}"
        )

    miss = exp.difference(got)
    extra = got.difference(exp)

    if len(miss) or len(extra):
        raise RuntimeError(
            f"{label}: calendar mismatch; "
            f"missing={list(miss[:5])}; "
            f"extra={list(extra[:5])}"
        )

def write_netcdf(ds,path):
    p=Path(path)
    if not p.is_absolute(): p=ROOT/p
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.stem+".write_tmp.nc")
    tmp.unlink(missing_ok=True)
    ds.to_netcdf(tmp,engine="netcdf4")
    tmp.replace(p)
    return p

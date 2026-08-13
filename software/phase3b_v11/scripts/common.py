from pathlib import Path
import logging, yaml, numpy as np, pandas as pd
from scipy import stats
ROOT=Path(__file__).resolve().parents[1]

def cfg():
    return yaml.safe_load((ROOT/"config/mechanistic_config.yaml").read_text())

def resolve(p):
    p=Path(p)
    return p if p.is_absolute() else (ROOT/p).resolve()

def log(name):
    (ROOT/"logs").mkdir(parents=True,exist_ok=True)
    L=logging.getLogger(name)
    if L.handlers:return L
    L.setLevel(logging.INFO)
    fmt=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh=logging.FileHandler(ROOT/"logs"/f"{name}.log");fh.setFormatter(fmt)
    sh=logging.StreamHandler();sh.setFormatter(fmt)
    L.addHandler(fh);L.addHandler(sh)
    return L

def bh_fdr(pvals):
    p=np.asarray(pvals,float);q=np.full_like(p,np.nan)
    v=np.isfinite(p);pv=p[v]
    if len(pv)==0:return q
    order=np.argsort(pv);rank=pv[order];m=len(rank)
    adj=rank*m/np.arange(1,m+1)
    adj=np.minimum.accumulate(adj[::-1])[::-1]
    adj=np.minimum(adj,1.0)
    back=np.empty_like(adj);back[order]=adj;q[v]=back
    return q

def effective_n_ar1(x,y):
    d=pd.DataFrame({"x":x,"y":y}).dropna()
    n=len(d)
    if n<4:return np.nan
    rx=d.x.autocorr(1);ry=d.y.autocorr(1)
    if not np.isfinite(rx):rx=0.0
    if not np.isfinite(ry):ry=0.0
    den=1+rx*ry
    return float(max(3,min(n,n*(1-rx*ry)/den if den!=0 else n)))

def corr_ar1(x,y):
    d=pd.DataFrame({"x":x,"y":y}).dropna()
    r=d.x.corr(d.y);ne=effective_n_ar1(d.x,d.y)
    if not np.isfinite(r) or not np.isfinite(ne):return r,len(d),ne,np.nan
    t=r*np.sqrt((ne-2)/max(1e-12,1-r*r))
    return r,len(d),ne,2*stats.t.sf(abs(t),df=max(1,ne-2))

def monthly_anomaly(series,time,start,end):
    z=pd.DataFrame({"time":pd.to_datetime(time),"x":pd.to_numeric(series,errors="coerce")})
    m=(z.time>=pd.Timestamp(start))&(z.time<=pd.Timestamp(end))
    clim=z.loc[m].assign(month=z.loc[m,"time"].dt.month).groupby("month").x.mean()
    return z.x-z.time.dt.month.map(clim).to_numpy()

def linear_detrend(series,time):
    y=pd.to_numeric(series,errors="coerce").to_numpy(float)
    t=pd.to_datetime(time)
    x=(t-t.min()).dt.days.to_numpy(float)/365.2425
    m=np.isfinite(y)&np.isfinite(x)
    b=np.polyfit(x[m],y[m],1)
    return y-(b[0]*x+b[1]),float(b[0])

def find_era5_gridded(root,varx,vary):
    import xarray as xr
    cand=[]
    for p in sorted(Path(root).rglob("*.nc")):
        try:
            with xr.open_dataset(p) as ds:
                if varx in ds and vary in ds:
                    tn="time" if "time" in ds.coords else "valid_time" if "valid_time" in ds.coords else None
                    nt=int(ds.sizes.get(tn,0)) if tn else 0
                    cand.append(((nt>=396,nt,p.stat().st_size),p))
        except Exception:
            pass
    if not cand:
        raise RuntimeError(f"No gridded ERA5 file with {varx},{vary} below {root}")
    cand.sort(key=lambda x:x[0],reverse=True)
    return cand[0][1]

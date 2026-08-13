from pathlib import Path
import logging, yaml, numpy as np, pandas as pd
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]

def cfg():
    return yaml.safe_load((ROOT/"config/coupling_config.yaml").read_text(encoding="utf-8"))

def resolve(p):
    p=Path(p)
    return p if p.is_absolute() else (ROOT/p).resolve()

def log(name):
    (ROOT/"logs").mkdir(parents=True,exist_ok=True)
    L=logging.getLogger(name)
    if L.handlers:
        return L
    L.setLevel(logging.INFO)
    fmt=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh=logging.FileHandler(ROOT/"logs"/f"{name}.log",encoding="utf-8")
    fh.setFormatter(fmt)
    sh=logging.StreamHandler()
    sh.setFormatter(fmt)
    L.addHandler(fh);L.addHandler(sh)
    return L

def bh_fdr(pvals):
    p=np.asarray(pvals,float)
    q=np.full_like(p,np.nan)
    valid=np.isfinite(p)
    pv=p[valid]
    if len(pv)==0:
        return q
    order=np.argsort(pv)
    ranked=pv[order]
    m=len(ranked)
    adj=ranked*m/np.arange(1,m+1)
    adj=np.minimum.accumulate(adj[::-1])[::-1]
    adj=np.minimum(adj,1.0)
    back=np.empty_like(adj)
    back[order]=adj
    q[valid]=back
    return q

def effective_n_ar1(x,y):
    z=pd.DataFrame({"x":x,"y":y}).dropna()
    n=len(z)
    if n<4:
        return np.nan
    rx=z.x.autocorr(1); ry=z.y.autocorr(1)
    if not np.isfinite(rx): rx=0.0
    if not np.isfinite(ry): ry=0.0
    den=1+rx*ry
    ne=n*(1-rx*ry)/den if den!=0 else n
    return float(max(3,min(n,ne)))

def corr_ar1(x,y):
    z=pd.DataFrame({"x":x,"y":y}).dropna()
    r=z.x.corr(z.y)
    ne=effective_n_ar1(z.x,z.y)
    if not np.isfinite(r) or not np.isfinite(ne):
        return r,len(z),ne,np.nan
    t=r*np.sqrt((ne-2)/max(1e-12,1-r*r))
    p=2*stats.t.sf(abs(t),df=max(1,ne-2))
    return r,len(z),ne,p

def partial_corr_two_controls(x,y,z1,z2):
    d=pd.DataFrame({"x":x,"y":y,"z1":z1,"z2":z2}).dropna()
    if len(d)<10:
        return np.nan,len(d),np.nan,np.nan
    Z=np.column_stack([np.ones(len(d)),d.z1.to_numpy(),d.z2.to_numpy()])
    bx=np.linalg.lstsq(Z,d.x.to_numpy(),rcond=None)[0]
    by=np.linalg.lstsq(Z,d.y.to_numpy(),rcond=None)[0]
    rx=d.x.to_numpy()-Z@bx
    ry=d.y.to_numpy()-Z@by
    r=np.corrcoef(rx,ry)[0,1]
    ne=effective_n_ar1(rx,ry)
    if not np.isfinite(r) or not np.isfinite(ne):
        return r,len(d),ne,np.nan
    df=max(1.0,ne-4.0)
    t=r*np.sqrt(df/max(1e-12,1-r*r))
    p=2*stats.t.sf(abs(t),df=df)
    return r,len(d),ne,p

def season_info(t):
    m=t.month
    if m in [12,1,2]:
        return ("DJF",t.year+1 if m==12 else t.year)
    if m in [3,4,5]:
        return ("MAM",t.year)
    if m in [6,7,8]:
        return ("JJA",t.year)
    return ("SON",t.year)

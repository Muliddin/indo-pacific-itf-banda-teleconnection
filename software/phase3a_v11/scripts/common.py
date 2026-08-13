from pathlib import Path
import logging, yaml, numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def cfg():
    return yaml.safe_load((ROOT/"config/lag_robustness_config.yaml").read_text(encoding="utf-8"))

def resolve(p):
    p=Path(p)
    return p if p.is_absolute() else (ROOT/p).resolve()

def log(name):
    (ROOT/"logs").mkdir(parents=True,exist_ok=True)
    L=logging.getLogger(name)
    if L.handlers:return L
    L.setLevel(logging.INFO)
    fmt=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh=logging.FileHandler(ROOT/"logs"/f"{name}.log",encoding="utf-8"); fh.setFormatter(fmt)
    sh=logging.StreamHandler(); sh.setFormatter(fmt)
    L.addHandler(fh); L.addHandler(sh)
    return L

def bh_fdr(pvals):
    p=np.asarray(pvals,dtype=float)
    q=np.full_like(p,np.nan)
    valid=np.isfinite(p)
    pv=p[valid]
    if len(pv)==0:return q
    order=np.argsort(pv); ranked=pv[order]; m=len(ranked)
    adj=ranked*m/np.arange(1,m+1)
    adj=np.minimum.accumulate(adj[::-1])[::-1]
    adj=np.minimum(adj,1.0)
    back=np.empty_like(adj); back[order]=adj
    q[valid]=back
    return q

def effective_n_ar1(x,y):
    z=pd.DataFrame({"x":x,"y":y}).dropna()
    n=len(z)
    if n<4:return np.nan
    rx=z.x.autocorr(1); ry=z.y.autocorr(1)
    if not np.isfinite(rx):rx=0.0
    if not np.isfinite(ry):ry=0.0
    den=1+rx*ry
    ne=n*(1-rx*ry)/den if den!=0 else n
    return float(max(3,min(n,ne)))

def residualize(y,z):
    d=pd.DataFrame({"y":y,"z":z}).dropna()
    coef=np.polyfit(d.z,d.y,1)
    out=pd.Series(index=d.index,dtype=float)
    out.loc[d.index]=d.y-(coef[0]*d.z+coef[1])
    return out

def partial_corr_stats(x,y,z):
    d=pd.DataFrame({"x":x,"y":y,"z":z}).dropna()
    if len(d)<8:return np.nan,len(d),np.nan,np.nan
    bx=np.polyfit(d.z,d.x,1); by=np.polyfit(d.z,d.y,1)
    rx=d.x-(bx[0]*d.z+bx[1]); ry=d.y-(by[0]*d.z+by[1])
    r=rx.corr(ry)
    ne=effective_n_ar1(rx,ry)
    if not np.isfinite(r) or not np.isfinite(ne):return r,len(d),ne,np.nan
    # one control variable -> use effective df approx ne-3
    df=max(1.0,ne-3.0)
    t=r*np.sqrt(df/max(1e-12,1-r*r))
    from scipy import stats
    p=2*stats.t.sf(abs(t),df=df)
    return r,len(d),ne,p

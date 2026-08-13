from pathlib import Path
import logging, yaml, numpy as np, pandas as pd
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]

def cfg():
    return yaml.safe_load((ROOT/"config/stage2_v11_config.yaml").read_text(encoding="utf-8"))

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
    L.addHandler(fh)
    L.addHandler(sh)
    return L

def season_info(t):
    m=t.month
    if m in [12,1,2]:
        return ("DJF", t.year+1 if m==12 else t.year)
    if m in [3,4,5]:
        return ("MAM", t.year)
    if m in [6,7,8]:
        return ("JJA", t.year)
    return ("SON", t.year)

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
    d=pd.DataFrame({"x":x,"y":y}).dropna()
    n=len(d)
    if n<4:
        return np.nan
    rx=d.x.autocorr(1)
    ry=d.y.autocorr(1)
    if not np.isfinite(rx): rx=0.0
    if not np.isfinite(ry): ry=0.0
    den=1+rx*ry
    ne=n*(1-rx*ry)/den if den!=0 else n
    return float(max(3,min(n,ne)))

def corr_ar1(x,y):
    d=pd.DataFrame({"x":x,"y":y}).dropna()
    r=d.x.corr(d.y)
    ne=effective_n_ar1(d.x,d.y)
    if not np.isfinite(r) or not np.isfinite(ne):
        return r,len(d),ne,np.nan
    tt=r*np.sqrt((ne-2)/max(1e-12,1-r*r))
    p=2*stats.t.sf(abs(tt),df=max(1,ne-2))
    return r,len(d),ne,p

def persistence_runs(mask):
    mask=np.asarray(mask,bool)
    runs=[]
    i=0
    while i<len(mask):
        if not mask[i]:
            i+=1
            continue
        j=i
        while j<len(mask) and mask[j]:
            j+=1
        runs.append((i,j))
        i=j
    return runs

def episode_bootstrap_diff(a,b,n_iter=5000,seed=42):
    rng=np.random.default_rng(seed)
    a=np.asarray(a,float); b=np.asarray(b,float)
    obs=np.mean(a)-np.mean(b)
    boot=[]
    for _ in range(n_iter):
        aa=rng.choice(a,size=len(a),replace=True)
        bb=rng.choice(b,size=len(b),replace=True)
        boot.append(np.mean(aa)-np.mean(bb))
    lo,hi=np.percentile(boot,[2.5,97.5])
    return obs,float(lo),float(hi)

def permutation_p(a,b,n_iter=5000,seed=42):
    rng=np.random.default_rng(seed)
    a=np.asarray(a,float); b=np.asarray(b,float)
    obs=abs(np.mean(a)-np.mean(b))
    z=np.concatenate([a,b]); na=len(a); count=0
    for _ in range(n_iter):
        perm=rng.permutation(z)
        stat=abs(np.mean(perm[:na])-np.mean(perm[na:]))
        count += stat>=obs
    return (count+1)/(n_iter+1)

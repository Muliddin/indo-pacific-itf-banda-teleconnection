from pathlib import Path
import logging,yaml,numpy as np,pandas as pd
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[1]

def cfg():
    return yaml.safe_load((ROOT/"config/diagnostics_config.yaml").read_text(encoding="utf-8"))

def resolve(p):
    p=Path(p)
    return p if p.is_absolute() else (ROOT/p).resolve()

def log(name):
    (ROOT/"logs").mkdir(parents=True,exist_ok=True)
    L=logging.getLogger(name)
    if L.handlers:return L
    L.setLevel(logging.INFO)
    fmt=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh=logging.FileHandler(ROOT/"logs"/f"{name}.log",encoding="utf-8");fh.setFormatter(fmt)
    sh=logging.StreamHandler();sh.setFormatter(fmt);L.addHandler(fh);L.addHandler(sh);return L

def zscore(s):
    s=pd.Series(s,dtype=float);sd=s.std(ddof=1)
    return (s-s.mean())/sd if np.isfinite(sd) and sd>0 else s*0

def bh_fdr(p):
    p=np.asarray(p,float);q=np.full_like(p,np.nan);ok=np.isfinite(p);pv=p[ok]
    if not len(pv):return q
    order=np.argsort(pv);r=pv[order];m=len(r)
    adj=r*m/np.arange(1,m+1);adj=np.minimum.accumulate(adj[::-1])[::-1];adj=np.minimum(adj,1)
    back=np.empty_like(adj);back[order]=adj;q[ok]=back;return q

def moving_block_indices(n,block,rng):
    starts=np.arange(max(1,n-block+1));idx=[]
    while len(idx)<n:
        s=int(rng.choice(starts));idx.extend(range(s,min(s+block,n)))
    return np.asarray(idx[:n],int)

def align_single(df,driver,covar,med,outcome,lag):
    h=int(lag)
    return pd.DataFrame({
        "time":df.time,
        "X":df[driver],
        "C":df[covar],
        "M":df[med],
        "Y":df[outcome].shift(-h)
    }).dropna().reset_index(drop=True)

def fit_single(d):
    z=pd.DataFrame({c:zscore(d[c]) for c in ["X","C","M","Y"]})
    mf=sm.OLS(z.M,sm.add_constant(z[["X","C"]],has_constant="add")).fit()
    yf=sm.OLS(z.Y,sm.add_constant(z[["X","C","M"]],has_constant="add")).fit()
    tf=sm.OLS(z.Y,sm.add_constant(z[["X","C"]],has_constant="add")).fit()
    a=float(mf.params["X"]);b=float(yf.params["M"]);cp=float(yf.params["X"]);ct=float(tf.params["X"])
    return {"a":a,"b":b,"indirect":a*b,"direct":cp,"total":ct,
            "decomposition_error":ct-(cp+a*b),"r2_mediator":float(mf.rsquared),
            "r2_outcome":float(yf.rsquared),"n":len(z)}

def bootstrap_single(d,n_iter,block,seed):
    rng=np.random.default_rng(seed);rows=[]
    for _ in range(n_iter):
        ids=moving_block_indices(len(d),block,rng)
        try:rows.append(fit_single(d.iloc[ids].reset_index(drop=True)))
        except Exception:pass
    return pd.DataFrame(rows)

def boot_summary(boots,col):
    b=pd.to_numeric(boots[col],errors="coerce").dropna().to_numpy()
    if not len(b):return np.nan,np.nan,np.nan,np.nan
    lo,hi=np.percentile(b,[2.5,97.5]);n=len(b)
    p=2*min((np.sum(b<=0)+1)/(n+1),(np.sum(b>=0)+1)/(n+1))
    stab=max(np.mean(b>0),np.mean(b<0))
    return float(lo),float(hi),float(min(1,p)),float(stab)

def vif_for_two(x1,x2):
    r=pd.Series(x1).corr(pd.Series(x2))
    if not np.isfinite(r):return np.nan
    return float(1/(1-r*r)) if abs(r)<1 else np.inf

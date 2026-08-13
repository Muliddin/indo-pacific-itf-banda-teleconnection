from pathlib import Path
import logging, yaml, numpy as np, pandas as pd
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[1]

def cfg():
    return yaml.safe_load((ROOT/"config/mediation_config.yaml").read_text(encoding="utf-8"))

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
    sh=logging.StreamHandler();sh.setFormatter(fmt)
    L.addHandler(fh);L.addHandler(sh)
    return L

def zscore(x):
    x=pd.Series(x,dtype=float)
    s=x.std(ddof=1)
    return (x-x.mean())/s if np.isfinite(s) and s>0 else x*0.0

def bh_fdr(pvals):
    p=np.asarray(pvals,float);q=np.full_like(p,np.nan)
    ok=np.isfinite(p);pv=p[ok]
    if len(pv)==0:return q
    order=np.argsort(pv);ranked=pv[order];m=len(ranked)
    adj=ranked*m/np.arange(1,m+1)
    adj=np.minimum.accumulate(adj[::-1])[::-1]
    adj=np.minimum(adj,1.0)
    back=np.empty_like(adj);back[order]=adj;q[ok]=back
    return q

def season_of_month(m):
    return "DJF" if m in [12,1,2] else "MAM" if m in [3,4,5] else "JJA" if m in [6,7,8] else "SON"

def align_parallel(df,driver,covar,m1,m2,outcome,lag_m1_y,lag_m2_y):
    # Common outcome horizon relative to driver baseline. Each mediator is sampled
    # at the time required by its empirically frozen mediator->outcome lag.
    horizon=max(int(lag_m1_y),int(lag_m2_y))
    out=pd.DataFrame({
        "time_driver":df.time,
        "X":df[driver],
        "C":df[covar],
        "M1":df[m1].shift(-(horizon-int(lag_m1_y))),
        "M2":df[m2].shift(-(horizon-int(lag_m2_y))),
        "Y":df[outcome].shift(-horizon),
        "time_outcome":df.time.shift(-horizon),
    }).dropna().reset_index(drop=True)
    out["outcome_month"]=pd.to_datetime(out.time_outcome).dt.month
    out["outcome_year"]=pd.to_datetime(out.time_outcome).dt.year
    out["outcome_season"]=out.outcome_month.map(season_of_month)
    out["horizon_months"]=horizon
    return out

def fit_parallel(d):
    z=pd.DataFrame({c:zscore(d[c]) for c in ["X","C","M1","M2","Y"]})
    Xmc=sm.add_constant(z[["X","C"]],has_constant="add")
    m1fit=sm.OLS(z.M1,Xmc).fit()
    m2fit=sm.OLS(z.M2,Xmc).fit()
    yfit=sm.OLS(z.Y,sm.add_constant(z[["X","C","M1","M2"]],has_constant="add")).fit()
    totalfit=sm.OLS(z.Y,sm.add_constant(z[["X","C"]],has_constant="add")).fit()
    a1=float(m1fit.params["X"]);a2=float(m2fit.params["X"])
    b1=float(yfit.params["M1"]);b2=float(yfit.params["M2"])
    cp=float(yfit.params["X"]);ct=float(totalfit.params["X"])
    i1=a1*b1;i2=a2*b2
    return {
        "a_qout":a1,"a_ekman":a2,"b_qout":b1,"b_ekman":b2,
        "indirect_qout":i1,"indirect_ekman":i2,"total_indirect":i1+i2,
        "direct_effect":cp,"total_effect":ct,
        "decomposition_error":ct-(cp+i1+i2),
        "r2_m1":float(m1fit.rsquared),"r2_m2":float(m2fit.rsquared),
        "r2_outcome":float(yfit.rsquared),"n":len(z)
    }

def moving_block_indices(n,block,rng):
    starts=np.arange(max(1,n-block+1))
    idx=[]
    while len(idx)<n:
        s=int(rng.choice(starts))
        idx.extend(range(s,min(s+block,n)))
    return np.asarray(idx[:n],int)

def cluster_year_indices(years,rng):
    years=np.asarray(years)
    uniq=np.unique(years)
    chosen=rng.choice(uniq,size=len(uniq),replace=True)
    idx=[]
    for y in chosen:
        idx.extend(np.where(years==y)[0].tolist())
    return np.asarray(idx,int)

def bootstrap_model(d,n_iter,block,seed,seasonal=False):
    rng=np.random.default_rng(seed)
    vals=[]
    for _ in range(n_iter):
        ids=cluster_year_indices(d.outcome_year.to_numpy(),rng) if seasonal else moving_block_indices(len(d),block,rng)
        try:
            vals.append(fit_parallel(d.iloc[ids].reset_index(drop=True)))
        except Exception:
            continue
    return pd.DataFrame(vals)

def boot_summary(point,boots,effect):
    b=pd.to_numeric(boots[effect],errors="coerce").dropna().to_numpy()
    if len(b)==0:
        return np.nan,np.nan,np.nan,np.nan
    lo,hi=np.percentile(b,[2.5,97.5])
    n=len(b)
    p=2*min((np.sum(b<=0)+1)/(n+1),(np.sum(b>=0)+1)/(n+1))
    stability=max(np.mean(b>0),np.mean(b<0))
    return float(lo),float(hi),float(min(1,p)),float(stability)

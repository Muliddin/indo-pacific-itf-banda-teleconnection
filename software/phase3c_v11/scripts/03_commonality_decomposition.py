import pandas as pd,numpy as np,statsmodels.api as sm
from common import ROOT,cfg,resolve,zscore,log
def r2(y,X):
    d=pd.DataFrame({"Y":y,**X}).dropna()
    Y=zscore(d.Y);Z=pd.DataFrame({k:zscore(d[k]) for k in X})
    return float(sm.OLS(Y,sm.add_constant(Z,has_constant="add")).fit().rsquared)
def main():
    c=cfg();L=log("03_commonality");r=resolve(c["inputs"]["phase3c_v10_root"])
    df=pd.read_csv(r/"data/processed/mediation_master_1993_2025.csv",parse_dates=["time"])
    rows=[]
    for drv,dc in c["drivers"].items():
        cov=dc["covariate"]
        for on,oc in c["outcomes"].items():
            y=oc["variable"];q=c["mediators"]["qout"];e=c["mediators"]["ekman"]
            lagq=int(oc["lags"]["qout"]);lage=int(oc["lags"]["ekman"]);h=max(lagq,lage)
            d=pd.DataFrame({"Y":df[y].shift(-h),"X":df[drv],"C":df[cov],
                            "Q":df[q].shift(-(h-lagq)),"E":df[e].shift(-(h-lage))}).dropna()
            r_base=r2(d.Y,{"X":d.X,"C":d.C})
            r_q=r2(d.Y,{"X":d.X,"C":d.C,"Q":d.Q})
            r_e=r2(d.Y,{"X":d.X,"C":d.C,"E":d.E})
            r_qe=r2(d.Y,{"X":d.X,"C":d.C,"Q":d.Q,"E":d.E})
            unique_q=r_qe-r_e
            unique_e=r_qe-r_q
            total_added=r_qe-r_base
            shared=total_added-unique_q-unique_e
            rows.append({"driver":drv,"outcome":on,"n":len(d),"r2_base_climate":r_base,
                         "r2_plus_qout":r_q,"r2_plus_ekman":r_e,"r2_plus_both":r_qe,
                         "increment_qout_alone":r_q-r_base,"increment_ekman_alone":r_e-r_base,
                         "increment_both":total_added,"unique_qout":unique_q,"unique_ekman":unique_e,
                         "shared_qout_ekman":shared})
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/commonality_shared_variance.csv",index=False)
    print(out.to_string(index=False));L.info("Commonality decomposition complete")
if __name__=="__main__":main()

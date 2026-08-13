import pandas as pd
import matplotlib.pyplot as plt
from common import ROOT,log

def one(df,leader,prefix):
    x=df[df.leader==leader]
    if x.empty:return
    p=x.pivot(index="follower",columns="lag_months_leader_leads",values="r")
    fig,ax=plt.subplots(figsize=(12,6))
    im=ax.imshow(p.values,aspect="auto",origin="lower",vmin=-1,vmax=1)
    ax.set_xticks(range(len(p.columns)));ax.set_xticklabels(p.columns)
    ax.set_yticks(range(len(p.index)))
    ax.set_yticklabels([s.replace("_banda_anom_dt","").replace("_sv_anom_dt","") for s in p.index])
    ax.set_xlabel("Lag (months; leader leads follower)")
    ax.set_title(prefix)
    fig.colorbar(im,ax=ax,label="r")
    fig.tight_layout()
    tag=leader.replace("_banda_anom_dt","").replace("_sv_anom_dt","")
    fig.savefig(ROOT/"figures"/f"directionality_{tag}.png",dpi=180,bbox_inches="tight")
    plt.close(fig)

def main():
    L=log("05_heatmaps")
    d=pd.read_csv(ROOT/"reports/mechanistic_directionality_all_lags.csv")
    (ROOT/"figures").mkdir(parents=True,exist_ok=True)
    for leader in sorted(d.leader.unique()):
        if "full_ekman" in leader or "curl_tau" in leader or "tau_banda" in leader:
            one(d,leader,f"{leader}: wind forcing lead-lag relationships")
    L.info("Directionality heatmaps complete")
if __name__=="__main__":main()

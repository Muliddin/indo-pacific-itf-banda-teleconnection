import pandas as pd
import matplotlib.pyplot as plt
from common import ROOT,log
def draw(df,value,title,path):
    piv=df.pivot(index="target",columns="lag_months_index_leads",values=value)
    fig,ax=plt.subplots(figsize=(11,4.8))
    im=ax.imshow(piv.values,aspect="auto",origin="lower")
    ax.set_xticks(range(len(piv.columns))); ax.set_xticklabels(piv.columns)
    ax.set_yticks(range(len(piv.index))); ax.set_yticklabels([x.replace("transport_","").replace("_sv_anom_dt","") for x in piv.index])
    ax.set_xlabel("Lag (months; positive = index leads ITF)")
    ax.set_title(title)
    fig.colorbar(im,ax=ax,label=value)
    fig.tight_layout(); fig.savefig(path,dpi=180,bbox_inches="tight"); plt.close(fig)
def main():
    L=log("03_heatmaps")
    d=pd.read_csv(ROOT/"reports/positive_lag_ENSO_IOD_to_ITF.csv")
    for idx in ["nino34","dmi"]:
        x=d[d["index"]==idx].copy()
        draw(x,"r",f"{idx}: correlation with detrended ITF anomalies",ROOT/"figures"/f"heatmap_{idx}_r.png")
        draw(x,"partial_r",f"{idx}: partial correlation controlling other climate index",ROOT/"figures"/f"heatmap_{idx}_partial_r.png")
    L.info("Heatmaps complete")
if __name__=="__main__":main()

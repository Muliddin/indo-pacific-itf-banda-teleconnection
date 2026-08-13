import pandas as pd
import matplotlib.pyplot as plt
from common import ROOT,log

def heat(df,value,title,path):
    piv=df.pivot(index="response",columns="lag_months_itf_leads",values=value)
    fig,ax=plt.subplots(figsize=(12,6))
    im=ax.imshow(piv.values,aspect="auto",origin="lower",vmin=-1,vmax=1)
    ax.set_xticks(range(len(piv.columns)))
    ax.set_xticklabels(piv.columns)
    ax.set_yticks(range(len(piv.index)))
    ax.set_yticklabels([
        x.replace("_banda_anom_dt","").replace("_dt","")
        for x in piv.index
    ])
    ax.set_xlabel("Lag (months; positive = ITF leads Banda response)")
    ax.set_title(title)
    fig.colorbar(im,ax=ax,label=value)
    fig.tight_layout()
    fig.savefig(path,dpi=180,bbox_inches="tight")
    plt.close(fig)

def main():
    L=log("06_heatmaps")
    d=pd.read_csv(ROOT/"reports/lagged_ITF_to_Banda.csv")
    (ROOT/"figures").mkdir(parents=True,exist_ok=True)
    for pred in sorted(d.predictor.unique()):
        x=d[d.predictor==pred]
        tag=pred.replace("transport_","").replace("_sv_anom_dt","")
        heat(
            x,"r",
            f"{tag}: ITF→Banda lagged correlation",
            ROOT/"figures"/f"heatmap_{tag}_r.png"
        )
        heat(
            x,"partial_r_ctrl_nino34_dmi",
            f"{tag}: partial coupling controlling Niño3.4 + DMI",
            ROOT/"figures"/f"heatmap_{tag}_partial.png"
        )
    L.info("Canonical heatmaps complete")
if __name__=="__main__":
    main()

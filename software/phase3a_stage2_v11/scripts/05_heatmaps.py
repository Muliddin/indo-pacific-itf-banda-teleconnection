import pandas as pd
import matplotlib.pyplot as plt
from common import ROOT,log
def main():
    L=log("05_heatmaps")
    d=pd.read_csv(ROOT/"reports/seasonal_year_correlations.csv")
    for idx in ["nino34","dmi"]:
        x=d[d["index"]==idx]
        p=x.pivot(index="target",columns="season",values="r")
        order=[s for s in ["DJF","MAM","JJA","SON"] if s in p.columns]
        p=p[order]
        fig,ax=plt.subplots(figsize=(7,5))
        im=ax.imshow(p.values,aspect="auto",origin="lower",vmin=-1,vmax=1)
        ax.set_xticks(range(len(p.columns)));ax.set_xticklabels(p.columns)
        ax.set_yticks(range(len(p.index)))
        ax.set_yticklabels([v.replace("transport_","").replace("_sv_anom_dt","") for v in p.index])
        ax.set_title(f"{idx}: seasonal-year correlation at frozen lag")
        fig.colorbar(im,ax=ax,label="r")
        fig.tight_layout()
        fig.savefig(ROOT/"figures"/f"seasonal_year_heatmap_{idx}.png",dpi=180,bbox_inches="tight")
        plt.close(fig)
    L.info("Heatmaps complete")
if __name__=="__main__":
    main()

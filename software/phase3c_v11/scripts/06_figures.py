import pandas as pd
import matplotlib.pyplot as plt
from common import ROOT,log
def main():
    L=log("06_figures")
    d=pd.read_csv(ROOT/"reports/single_vs_parallel_indirect_comparison.csv")
    labels=[f"{a}-{b}-{m}" for a,b,m in zip(d.driver,d.outcome,d.mediator)]
    x=range(len(d))
    fig,ax=plt.subplots(figsize=(10,5))
    w=0.35
    ax.bar([i-w/2 for i in x],d.single_indirect,width=w,label="Single mediator")
    ax.bar([i+w/2 for i in x],d.parallel_indirect,width=w,label="Parallel mediator")
    ax.axhline(0,linewidth=0.8)
    ax.set_xticks(list(x));ax.set_xticklabels(labels,rotation=45,ha="right")
    ax.set_ylabel("Standardized indirect effect")
    ax.legend();fig.tight_layout()
    fig.savefig(ROOT/"figures"/"single_vs_parallel_indirect_effects.png",dpi=180,bbox_inches="tight")
    plt.close(fig)

    c=pd.read_csv(ROOT/"reports/commonality_shared_variance.csv")
    fig,ax=plt.subplots(figsize=(9,5))
    labs=[f"{a}-{b}" for a,b in zip(c.driver,c.outcome)]
    ax.bar(labs,c.unique_qout,label="Unique Qout")
    ax.bar(labs,c.unique_ekman,bottom=c.unique_qout,label="Unique Ekman")
    ax.bar(labs,c.shared_qout_ekman,bottom=c.unique_qout+c.unique_ekman,label="Shared")
    ax.set_ylabel("Incremental R²")
    ax.tick_params(axis="x",rotation=45)
    ax.legend();fig.tight_layout()
    fig.savefig(ROOT/"figures"/"commonality_decomposition.png",dpi=180,bbox_inches="tight")
    plt.close(fig)
    L.info("Figures complete")
if __name__=="__main__":main()

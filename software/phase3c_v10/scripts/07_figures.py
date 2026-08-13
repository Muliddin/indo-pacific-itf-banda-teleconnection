import pandas as pd
import matplotlib.pyplot as plt
from common import ROOT,log
def main():
    L=log("07_figures")
    d=pd.read_csv(ROOT/"reports/primary_parallel_mediation.csv")
    rows=[]
    for _,r in d.iterrows():
        rows += [
            {"model":f"{r.driver}->{r.outcome}","path":"Qout","effect":r.indirect_qout},
            {"model":f"{r.driver}->{r.outcome}","path":"Ekman","effect":r.indirect_ekman},
            {"model":f"{r.driver}->{r.outcome}","path":"Total indirect","effect":r.total_indirect},
            {"model":f"{r.driver}->{r.outcome}","path":"Direct","effect":r.direct_effect},
        ]
    x=pd.DataFrame(rows)
    for model,g in x.groupby("model"):
        fig,ax=plt.subplots(figsize=(7,4))
        ax.bar(g.path,g.effect)
        ax.axhline(0,linewidth=0.8)
        ax.set_ylabel("Standardized effect")
        ax.set_title(model.replace("->"," → "))
        ax.tick_params(axis="x",rotation=20)
        fig.tight_layout()
        tag=model.replace("->","_to_")
        fig.savefig(ROOT/"figures"/f"mediation_{tag}.png",dpi=180,bbox_inches="tight")
        plt.close(fig)
    L.info("Mediation figures complete")
if __name__=="__main__":main()

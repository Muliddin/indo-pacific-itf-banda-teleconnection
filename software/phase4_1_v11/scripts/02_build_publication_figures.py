from common import *
import matplotlib.pyplot as plt

def panel_label(ax,label):
    ax.text(-0.08,1.04,label,transform=ax.transAxes,fontweight="bold",fontsize=11)

def main():
    c=cfg();L=log("02_figures");p4=resolve(c["inputs"]["phase4_root"])
    dpi=int(c["figures"]["dpi"])

    # Figure 1: section + total validation
    sec=pd.read_csv(p4/"tables/Table_S1_ITF_section_validation.csv")
    total=pd.read_csv(p4/"tables/Table_1_total_outflow_validation.csv")
    fig,axs=plt.subplots(1,2,figsize=(11,4.8))
    x=np.arange(len(sec))
    axs[0].bar(x-0.18,sec.reference_mean_2004_2006_sv,0.36,label="Reference")
    axs[0].bar(x+0.18,sec.canonical_mean_2004_2006_sv,0.36,label="Native-grid")
    axs[0].set_xticks(x);axs[0].set_xticklabels(sec.section_id.str.title())
    axs[0].set_ylabel("Transport (Sv)");axs[0].legend();panel_label(axs[0],"a")
    axs[1].bar(["Reference","Model"],[total.instant_reference_sv.iloc[0],total.model_total_outflow_2004_2006_sv.iloc[0]])
    axs[1].set_ylabel("Total outflow (Sv)");panel_label(axs[1],"b")
    fig.tight_layout();fig.savefig(ROOT/"figures/Figure_1_ITF_Validation.png",dpi=dpi,bbox_inches="tight");plt.close(fig)

    # Figure 2: frozen ENSO/IOD effects
    s1=pd.read_csv(p4/"tables/Table_2_ENSO_IOD_ITF_lagged.csv")
    s1=s1[s1.freeze_status=="FREEZE"]
    fig,axs=plt.subplots(1,2,figsize=(11,5),sharey=False)
    for ax,(idx,g) in zip(axs,s1.groupby("index")):
        g=g.copy();vals=g["r_best_positive"];labels=g.target.str.replace("transport_","",regex=False).str.replace("_sv","",regex=False)
        ax.bar(np.arange(len(g)),vals)
        ax.axhline(0,lw=.8);ax.set_xticks(np.arange(len(g)));ax.set_xticklabels(labels,rotation=45,ha="right")
        ax.set_title(idx.upper());ax.set_ylabel("r at frozen positive lag")
        panel_label(ax,"a" if idx=="dmi" else "b")
    fig.tight_layout();fig.savefig(ROOT/"figures/Figure_2_ENSO_IOD_to_ITF.png",dpi=dpi,bbox_inches="tight");plt.close(fig)

    # Figure 3: seasonal robust heatmaps + event-level contrasts
    s2=pd.read_csv(p4/"tables/Table_3_seasonal_event_robustness.csv")
    sy=s2[s2.analysis_type=="seasonal_year"].copy()
    ev=s2[s2.analysis_type=="event_composite"].copy()
    fig,axs=plt.subplots(1,3,figsize=(13,5))
    for j,idx in enumerate(["nino34","dmi"]):
        g=sy[sy["index"]==idx]
        piv=g.pivot(index="target",columns="season",values="effect")
        order=[x for x in ["DJF","MAM","JJA","SON"] if x in piv.columns];piv=piv[order]
        im=axs[j].imshow(piv.values,aspect="auto",origin="lower",vmin=-1,vmax=1)
        axs[j].set_xticks(range(len(piv.columns)));axs[j].set_xticklabels(piv.columns)
        axs[j].set_yticks(range(len(piv.index)));axs[j].set_yticklabels([x.replace("transport_","").replace("_sv_anom_dt","") for x in piv.index],fontsize=8)
        axs[j].set_title(idx.upper());panel_label(axs[j],chr(97+j))
    gev=ev[ev.freeze_status.isin(["FREEZE","CONDITIONAL"])].copy()
    axs[2].barh(np.arange(len(gev)),gev.effect)
    axs[2].axvline(0,lw=.8)
    axs[2].set_yticks(np.arange(len(gev)));axs[2].set_yticklabels([f"{i}: {t.replace('transport_','').replace('_sv_anom_dt','')}" for i,t in zip(gev["index"],gev.target)],fontsize=7)
    axs[2].set_title("Event contrasts");panel_label(axs[2],"c")
    fig.colorbar(im,ax=axs[:2],label="Seasonal-year r",fraction=.025)
    fig.tight_layout();fig.savefig(ROOT/"figures/Figure_3_Seasonal_Event_Structure.png",dpi=dpi,bbox_inches="tight");plt.close(fig)

    # Figure 4: ITF-Banda + mechanistic atmosphere
    cpl=pd.read_csv(p4/"tables/Table_4_ITF_Banda_coupling.csv")
    mech=pd.read_csv(resolve(c["inputs"]["phase4_root"])/"reports/evidence_registry.csv")
    fig,axs=plt.subplots(1,2,figsize=(12,5))
    cc=cpl[cpl.get("coupling_status",pd.Series([""]*len(cpl))).isin(["CANONICAL","CONDITIONAL"])].copy()
    axs[0].barh(np.arange(len(cc)),cc.r_best)
    axs[0].axvline(0,lw=.8)
    axs[0].set_yticks(np.arange(len(cc)));axs[0].set_yticklabels([f"{p.replace('transport_','')}→{r.replace('_banda_anom','')}" for p,r in zip(cc.predictor,cc.response)],fontsize=7)
    axs[0].set_title("ITF–Banda coupling");panel_label(axs[0],"a")
    mm=mech[(mech.phase=="3B-v1.1")&(mech.evidence_tier=="ROBUST_CORE")].copy()
    axs[1].barh(np.arange(len(mm)),pd.to_numeric(mm.effect,errors="coerce"))
    axs[1].axvline(0,lw=.8)
    axs[1].set_yticks(np.arange(len(mm)));axs[1].set_yticklabels([f"{d}→{t}" for d,t in zip(mm.driver,mm.target)],fontsize=7)
    axs[1].set_title("Robust mechanistic directionality");panel_label(axs[1],"b")
    fig.tight_layout();fig.savefig(ROOT/"figures/Figure_4_ITF_Atmosphere_Banda_Coupling.png",dpi=dpi,bbox_inches="tight");plt.close(fig)

    # Figure 5: integrated DAG + mediation constraint
    med=pd.read_csv(p4/"tables/Table_5_parallel_mediation.csv")
    fig,axs=plt.subplots(1,2,figsize=(12,5))
    axs[0].axis("off")
    pos={"ENSO":(.1,.75),"IOD":(.1,.25),"ITF/Qout":(.48,.68),"Wind/Ekman":(.48,.28),"Banda OHC":(.85,.5)}
    for n,(x,y) in pos.items():axs[0].text(x,y,n,ha="center",va="center",bbox=dict(boxstyle="round,pad=.5",fc="white",ec="black"))
    from matplotlib.patches import FancyArrowPatch
    def ar(a,b,ls="-"):
        A=pos[a];B=pos[b];axs[0].add_patch(FancyArrowPatch(A,B,arrowstyle="-|>",mutation_scale=14,lw=1.8,linestyle=ls,shrinkA=32,shrinkB=32))
    for a in ["ENSO","IOD"]:
        ar(a,"ITF/Qout");ar(a,"Wind/Ekman")
    ar("ITF/Qout","Banda OHC","--");ar("Wind/Ekman","Banda OHC","--")
    axs[0].set_title("Integrated conceptual network");panel_label(axs[0],"a")
    x=np.arange(len(med));w=.25
    axs[1].bar(x-w,med.indirect_qout,w,label="Qout indirect")
    axs[1].bar(x,med.indirect_ekman,w,label="Ekman indirect")
    axs[1].bar(x+w,med.direct_effect,w,label="Direct")
    axs[1].axhline(0,lw=.8)
    axs[1].set_xticks(x);axs[1].set_xticklabels([f"{d}→{o}" for d,o in zip(med.driver,med.outcome)],rotation=45,ha="right")
    axs[1].set_ylabel("Standardized effect");axs[1].legend(fontsize=8)
    axs[1].set_title("Formal mediation constraint");panel_label(axs[1],"b")
    fig.tight_layout();fig.savefig(ROOT/"figures/Figure_5_Integrated_Synthesis.png",dpi=dpi,bbox_inches="tight");plt.close(fig)
    L.info("Five publication figures written")
if __name__=="__main__":main()

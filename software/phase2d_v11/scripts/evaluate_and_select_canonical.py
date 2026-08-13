from pathlib import Path
import csv,json
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; REG=ROOT/"section_registry_v1.1.csv"; C=ROOT/"data/processed/native_grid_candidates_1993_2025.csv"
REPORTS = ROOT / "reports"
CANONICAL = ROOT / "data" / "processed" / "canonical"

REPORTS.mkdir(parents=True, exist_ok=True)
CANONICAL.mkdir(parents=True, exist_ok=True)
def main():
    df=pd.read_csv(C,parse_dates=["time"])
    with REG.open(encoding="utf-8") as f: reg={r["section_id"]:r for r in csv.DictReader(f)}
    sums=[]; cans=[]; decisions={}
    for sid,g in df.groupby("section_id"):
        piv=g.pivot(index="time",columns="offset_grid_cells",values="transport_indian_positive_sv"); med=piv.median(axis=1); rr=[]
        ref=float(reg[sid]["reference_mean_2004_2006_sv"])
        for off in sorted(g.offset_grid_cells.unique()):
            x=g[g.offset_grid_cells==off]; p=x[(x.time>="2004-01-01")&(x.time<="2006-12-01")]
            m=float(p.transport_indian_positive_sv.mean()); corr=float(piv[off].corr(med)); wet=float(x.wet_column_fraction.mean())
            rel=100*(m-ref)/ref
            anchor=1-abs(int(off))/3; lit=1/(1+abs(rel)/25)
            score=.35*anchor+.25*max(0,corr)+.25*min(1,wet)+.15*lit
            rr.append({"section_id":sid,"offset_grid_cells":int(off),"candidate_coordinate":float(x.candidate_coordinate.iloc[0]),
                       "candidate_coordinate_name":x.candidate_coordinate_name.iloc[0],"mean_2004_2006_sv":m,
                       "reference_2004_2006_sv":ref,"relative_bias_percent":rel,"mean_1993_2025_sv":float(x.transport_indian_positive_sv.mean()),
                       "std_1993_2025_sv":float(x.transport_indian_positive_sv.std()),"wet_column_fraction":wet,
                       "wet_area_fraction":float(x.wet_area_fraction.mean()),"corr_to_ensemble_median":corr,
                       "anchor_distance_grid_cells":abs(int(off)),"canonical_score":score,
                       "eligible":wet>=.5 and corr>=.90})
        s=pd.DataFrame(rr); e=s[s.eligible]
        if e.empty: raise RuntimeError(f"{sid}: no eligible candidate")
        ch=e.sort_values(["canonical_score","anchor_distance_grid_cells"],ascending=[False,True]).iloc[0]
        off=int(ch.offset_grid_cells); s["selected_canonical"]=s.offset_grid_cells.eq(off); sums.append(s)
        x=g[g.offset_grid_cells==off].copy(); x["canonical_method"]="native_grid"; x["canonical_selection_score"]=float(ch.canonical_score); cans.append(x)
        decisions[sid]={k:(float(ch[k]) if isinstance(ch[k],(np.floating,float)) else int(ch[k]) if isinstance(ch[k],(np.integer,int)) else ch[k])
                        for k in ["offset_grid_cells","candidate_coordinate","canonical_score","mean_2004_2006_sv","reference_2004_2006_sv",
                                  "relative_bias_percent","wet_column_fraction","corr_to_ensemble_median"]}
    pd.concat(sums).to_csv(ROOT/"reports/native_grid_candidate_scores.csv",index=False)
    can=pd.concat(cans).sort_values(["time","section_id"]); p=ROOT/"data/processed/canonical/itf_transport_CANONICAL_1993_2025.csv"; p.parent.mkdir(parents=True,exist_ok=True)
    can.to_csv(p,index=False,date_format="%Y-%m-%d"); (ROOT/"reports/canonical_selection.json").write_text(json.dumps(decisions,indent=2),encoding="utf-8")
    print(json.dumps(decisions,indent=2)); print("WROTE",p)
if __name__=="__main__": main()

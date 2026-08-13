from pathlib import Path
import pandas as pd,numpy as np,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    d=pd.read_csv(ROOT/"data/processed/timor_candidates_1993_2025.csv",parse_dates=["time"])
    piv=d.pivot(index="time",columns="offset_grid_cells",values="transport_indian_positive_sv");med=piv.median(axis=1);rows=[]
    for off in sorted(d.offset_grid_cells.unique()):
        x=d[d.offset_grid_cells==off];p=x[(x.time>="2004-01-01")&(x.time<="2006-12-01")]
        m=p.transport_indian_positive_sv.mean();rel=100*(m-7.5)/7.5;corr=piv[off].corr(med);wet=x.wet_column_fraction.mean()
        anchor=1-abs(off)/3;lit=1/(1+abs(rel)/25);score=.35*anchor+.25*max(0,corr)+.25*min(1,wet)+.15*lit
        rows.append({"offset_grid_cells":off,"mean_2004_2006_sv":m,"reference_sv":7.5,"relative_bias_percent":rel,
                     "mean_1993_2025_sv":x.transport_indian_positive_sv.mean(),"std_1993_2025_sv":x.transport_indian_positive_sv.std(),
                     "wet_column_fraction":wet,"corr_to_ensemble_median":corr,"canonical_score":score,
                     "eligible":wet>=.5 and corr>=.90})
    s=pd.DataFrame(rows);e=s[s.eligible]
    if e.empty:raise RuntimeError("No eligible Timor candidate")
    ch=e.sort_values(["canonical_score","offset_grid_cells"],ascending=[False,True]).iloc[0];off=int(ch.offset_grid_cells)
    s["selected_canonical"]=s.offset_grid_cells.eq(off);s.to_csv(ROOT/"reports/timor_candidate_scores.csv",index=False)
    can=d[d.offset_grid_cells==off].copy();can["canonical_method"]="timor_oblique_native_nearest";can["canonical_selection_score"]=ch.canonical_score
    p=ROOT/"data/processed/canonical/transport_timor_CANONICAL_1993_2025.csv";can.to_csv(p,index=False,date_format="%Y-%m-%d")
    (ROOT/"reports/timor_canonical_selection.json").write_text(json.dumps(ch.to_dict(),indent=2,default=float),encoding="utf-8")
    print(ch.to_string());print("WROTE",p)
if __name__=="__main__":main()

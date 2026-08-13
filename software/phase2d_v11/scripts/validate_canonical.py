from pathlib import Path
import argparse,csv,pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--phase2d-v1-root",required=True); a=ap.parse_args()
    v1=Path(a.phase2d_v1_root).expanduser().resolve()
    c=pd.read_csv(ROOT/"data/processed/canonical/itf_transport_CANONICAL_1993_2025.csv",parse_dates=["time"])
    with (ROOT/"section_registry_v1.1.csv").open(encoding="utf-8") as f: reg={r["section_id"]:r for r in csv.DictReader(f)}
    L=pd.read_csv(v1/"data/processed/sensitivity/itf_transport_linear_1993_2025.csv",parse_dates=["time"])
    N=pd.read_csv(v1/"data/processed/sensitivity/itf_transport_nearest_1993_2025.csv",parse_dates=["time"])
    out=[]
    for sid,g in c.groupby("section_id"):
        p=g[(g.time>="2004-01-01")&(g.time<="2006-12-01")]; m=float(p.transport_indian_positive_sv.mean()); ref=float(reg[sid]["reference_mean_2004_2006_sv"])
        row={"section_id":sid,"canonical_offset":int(g.offset_grid_cells.iloc[0]),"canonical_mean_2004_2006_sv":m,
             "reference_mean_2004_2006_sv":ref,"bias_sv":m-ref,"relative_bias_percent":100*(m-ref)/ref,
             "canonical_mean_1993_2025_sv":float(g.transport_indian_positive_sv.mean()),"canonical_std_1993_2025_sv":float(g.transport_indian_positive_sv.std())}
        for name,d in [("linear",L),("nearest",N)]:
            q=d[d.section_id==sid][["time","transport_indian_positive_sv"]].rename(columns={"transport_indian_positive_sv":name})
            z=g[["time","transport_indian_positive_sv"]].rename(columns={"transport_indian_positive_sv":"canonical"}).merge(q,on="time")
            row[f"r_canonical_{name}"]=z.canonical.corr(z[name]); row[f"mean_diff_canonical_minus_{name}_sv"]=float((z.canonical-z[name]).mean())
        out.append(row)
    df=pd.DataFrame(out); p=ROOT/"reports/canonical_validation_summary.csv"; df.to_csv(p,index=False); print(df.to_string(index=False)); print("WROTE",p)
if __name__=="__main__": main()

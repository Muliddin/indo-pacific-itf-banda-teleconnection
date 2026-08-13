from pathlib import Path
import argparse,pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--phase2d-v11-root",required=True);a=ap.parse_args()
    v11=Path(a.phase2d_v11_root).expanduser().resolve()
    b=pd.read_csv(v11/"data/processed/canonical/itf_transport_CANONICAL_1993_2025.csv",parse_dates=["time"])
    t=pd.read_csv(ROOT/"data/processed/canonical/transport_timor_CANONICAL_1993_2025.csv",parse_dates=["time"])
    wide=b.pivot(index="time",columns="section_id",values="transport_indian_positive_sv")
    wide["timor"]=t.set_index("time").transport_indian_positive_sv
    wide["total_major_outflow_sv"]=wide[["lombok","ombai","timor"]].sum(axis=1)
    out=wide.reset_index();p=ROOT/"data/processed/canonical/major_outflow_CANONICAL_1993_2025.csv";out.to_csv(p,index=False,date_format="%Y-%m-%d")
    q=out[(out.time>="2004-01-01")&(out.time<="2006-12-01")];mean=q.total_major_outflow_sv.mean()
    r=pd.DataFrame([{"model_total_outflow_2004_2006_sv":mean,"instant_reference_sv":15.0,"bias_sv":mean-15,
                     "relative_bias_percent":100*(mean-15)/15,"lombok_mean_sv":q.lombok.mean(),
                     "ombai_mean_sv":q.ombai.mean(),"timor_mean_sv":q.timor.mean()}])
    rp=ROOT/"reports/total_outflow_validation_2004_2006.csv";r.to_csv(rp,index=False);print(r.to_string(index=False));print("WROTE",p);print("WROTE",rp)
if __name__=="__main__":main()

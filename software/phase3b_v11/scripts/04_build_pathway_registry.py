import numpy as np,pandas as pd
from common import ROOT,cfg,resolve,log

def row_for(best,a,b):
    z=best[(best.leader==a)&(best.follower==b)]
    return None if z.empty else z.iloc[0]

def main():
    c=cfg();L=log("04_pathways")
    best=pd.read_csv(ROOT/"reports/mechanistic_directionality_best.csv")
    p3b=resolve(c["inputs"]["phase3b_v10_root"])
    coupling=pd.read_csv(p3b/"reports/canonical_ITF_Banda_coupling.csv")

    winds=[w for w in c["wind_candidates"] if w in set(best.leader)|set(best.follower)]
    transports=c["transport"]
    oceans=c["ocean_responses"]
    alpha=float(c["analysis"]["fdr_alpha"])
    minr=float(c["analysis"]["min_abs_r_directionality"])
    rows=[]

    # Atmospheric directionality: wind <-> ITF
    for w in winds:
        for q in transports:
            fw=row_for(best,w,q); rev=row_for(best,q,w)
            if fw is None or rev is None: continue
            fw_sig=fw.q_direction_best<=alpha and abs(fw.r_best)>=minr
            rev_sig=rev.q_direction_best<=alpha and abs(rev.r_best)>=minr
            if fw_sig and (not rev_sig or abs(fw.r_best)>abs(rev.r_best)+0.05):
                status="ATMOSPHERIC_TO_ITF_SUPPORTED"
            elif rev_sig and (not fw_sig or abs(rev.r_best)>abs(fw.r_best)+0.05):
                status="REVERSE_LEAD_DIAGNOSTIC"
            elif fw_sig or rev_sig:
                status="BIDIRECTIONAL_OR_COMMON_FORCING"
            else:
                status="WEAK"
            rows.append({
                "pathway_class":"directionality",
                "driver":w,"mediator_or_target":q,"downstream_target":"",
                "forward_best_lag":int(fw.best_lag),"forward_r":fw.r_best,"forward_q":fw.q_direction_best,
                "reverse_best_lag":int(rev.best_lag),"reverse_r":rev.r_best,"reverse_q":rev.q_direction_best,
                "status":status
            })

    # Atmospheric pathway candidates: wind -> OHC/SST/MLD
    for w in winds:
        for y in oceans:
            fw=row_for(best,w,y); rev=row_for(best,y,w)
            if fw is None or rev is None: continue
            fw_sig=fw.q_direction_best<=alpha and abs(fw.r_best)>=minr
            reverse_dominates=(rev.q_direction_best<=alpha and abs(rev.r_best)>abs(fw.r_best)+0.05)
            status="ATMOSPHERIC_CANDIDATE" if fw_sig and not reverse_dominates else "AMBIGUOUS" if fw_sig else "REVIEW"
            rows.append({
                "pathway_class":"atmospheric",
                "driver":w,"mediator_or_target":y,"downstream_target":"",
                "forward_best_lag":int(fw.best_lag),"forward_r":fw.r_best,"forward_q":fw.q_direction_best,
                "reverse_best_lag":int(rev.best_lag),"reverse_r":rev.r_best,"reverse_q":rev.q_direction_best,
                "status":status
            })

    # Oceanic pathway candidates from Phase3B v1.0.
    for _,r in coupling.iterrows():
        if r.response not in [x.replace("_dt","") for x in oceans]:
            continue
        if r.predictor not in [x.replace("_anom_dt","") for x in transports]:
            continue
        if r.response.startswith(("ohc300","ohc700","sst","mld")):
            if r.coupling_status=="CANONICAL":
                st="OCEANIC_CANDIDATE_STRONG"
            elif r.coupling_status=="CONDITIONAL" and abs(r.r_best)>=minr:
                st="OCEANIC_MEDIATION_CANDIDATE"
            else:
                st="REVIEW"
            rows.append({
                "pathway_class":"oceanic",
                "driver":r.predictor,"mediator_or_target":r.response,"downstream_target":"",
                "forward_best_lag":int(r.best_lag_itf_leads),"forward_r":r.r_best,"forward_q":r.q_pair_best,
                "reverse_best_lag":np.nan,"reverse_r":np.nan,"reverse_q":np.nan,
                "status":st
            })

    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/mechanistic_pathway_registry.csv",index=False)
    print(out.to_string(index=False))
    L.info("Pathway registry complete")

if __name__=="__main__":main()

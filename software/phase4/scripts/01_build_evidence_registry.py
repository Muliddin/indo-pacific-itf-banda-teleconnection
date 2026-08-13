from common import *
def tier(s):
 s=str(s).upper()
 if 'FREEZE' in s or 'CANONICAL' in s or 'SUPPORTED' in s:return 'ROBUST_CORE'
 if 'CONDITIONAL' in s or 'CANDIDATE' in s:return 'CONDITIONAL_SUPPORTING'
 return 'EXPLORATORY_CONTEXTUAL'
def main():
 c=cfg();rows=[]
 specs=[('3A-v1.1','ENSO_IOD_to_ITF','phase3a_v11_root','reports/stage1_freeze_decision.csv','freeze_status'),('3A-Stage2-v1.1','seasonal_event','phase3a_stage2_v11_root','reports/stage2_freeze_decision.csv','freeze_status'),('3B-v1.0','ITF_to_Banda','phase3b_v10_root','reports/canonical_ITF_Banda_coupling.csv','coupling_status'),('3B-v1.1','mechanistic','phase3b_v11_root','reports/mechanistic_pathway_registry.csv','status'),('3C-v1.1','mediation','phase3c_v11_root','reports/mediation_collinearity_diagnostic_classification.csv','diagnostic_status')]
 for ph,dom,k,f,sc in specs:
  d=pd.read_csv(resolve(c['inputs'][k])/f)
  for i,r in d.iterrows():
   s=str(r.get(sc,'')); rows.append({'phase':ph,'domain':dom,'source_file':f,'source_row':i,'driver':r.get('index',r.get('driver',r.get('pathway_class',''))),'target':r.get('target',r.get('outcome',r.get('mediator_or_target',''))),'season':r.get('season',''),'lag':r.get('best_positive_lag',r.get('frozen_lag',r.get('forward_best_lag',''))),'effect':r.get('r_best_positive',r.get('r',r.get('forward_r',np.nan))),'q_fdr':r.get('q_pair_best_positive',r.get('q_fdr',r.get('forward_q',np.nan))),'status_original':s,'evidence_tier':tier(s)})
 out=pd.DataFrame(rows)
 out['permitted_claim']=out.evidence_tier.map({'ROBUST_CORE':'Primary association/robustness claim; no causal language.','CONDITIONAL_SUPPORTING':'Supporting claim with explicit qualification.','EXPLORATORY_CONTEXTUAL':'Context only; no confirmatory/causal claim.'})
 out.to_csv(ROOT/'reports/evidence_registry.csv',index=False)
 print(out.evidence_tier.value_counts())
if __name__=='__main__':main()

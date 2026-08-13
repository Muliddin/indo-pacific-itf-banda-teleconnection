from common import *
def main():
 c=cfg(); L=log('preflight')
 specs=[('phase2d_v11_root','reports/canonical_validation_summary.csv'),('phase2d_v12_root','reports/total_outflow_validation_2004_2006.csv'),('phase3a_v11_root','reports/stage1_freeze_decision.csv'),('phase3a_stage2_v11_root','reports/stage2_freeze_decision.csv'),('phase3b_v10_root','reports/canonical_ITF_Banda_coupling.csv'),('phase3b_v11_root','reports/mechanistic_pathway_registry.csv'),('phase3c_v10_root','reports/primary_parallel_mediation.csv'),('phase3c_v11_root','reports/mediation_collinearity_diagnostic_classification.csv')]
 rows=[]; miss=[]
 for k,r in specs:
  p=resolve(c['inputs'][k])/r; rows.append({'input':k,'path':str(p),'exists':p.exists()})
  if not p.exists():miss.append(str(p))
 pd.DataFrame(rows).to_csv(ROOT/'reports/preflight_inputs.csv',index=False)
 if miss:raise FileNotFoundError('Missing frozen inputs:\n'+'\n'.join(miss))
 L.info('PASS %d inputs',len(rows))
if __name__=='__main__':main()

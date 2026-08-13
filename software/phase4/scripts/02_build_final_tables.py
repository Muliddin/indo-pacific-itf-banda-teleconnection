from common import *
def main():
 c=cfg()
 specs=[('phase2d_v11_root','reports/canonical_validation_summary.csv','Table_S1_ITF_section_validation.csv'),('phase2d_v12_root','reports/total_outflow_validation_2004_2006.csv','Table_1_total_outflow_validation.csv'),('phase3a_v11_root','reports/stage1_freeze_decision.csv','Table_2_ENSO_IOD_ITF_lagged.csv'),('phase3a_stage2_v11_root','reports/stage2_freeze_decision.csv','Table_3_seasonal_event_robustness.csv'),('phase3b_v10_root','reports/canonical_ITF_Banda_coupling.csv','Table_4_ITF_Banda_coupling.csv'),('phase3c_v10_root','reports/primary_parallel_mediation.csv','Table_5_parallel_mediation.csv'),('phase3c_v11_root','reports/commonality_shared_variance.csv','Table_S2_commonality.csv'),('phase3c_v11_root','reports/single_vs_parallel_indirect_comparison.csv','Table_S3_single_parallel.csv')]
 for k,f,n in specs:pd.read_csv(resolve(c['inputs'][k])/f).to_csv(ROOT/'tables'/n,index=False)
 print('WROTE',len(specs),'tables')
if __name__=='__main__':main()

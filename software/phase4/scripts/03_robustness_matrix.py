from common import *
def main():
 d=pd.read_csv(ROOT/'reports/evidence_registry.csv')
 m=d.groupby(['phase','domain','evidence_tier'],dropna=False).size().reset_index(name='n_findings')
 m.to_csv(ROOT/'reports/robustness_matrix.csv',index=False)
 for tier,name in [('ROBUST_CORE','Table_6_robust_core_findings.csv'),('CONDITIONAL_SUPPORTING','conditional_findings.csv'),('EXPLORATORY_CONTEXTUAL','exploratory_findings.csv')]:
  dest=ROOT/'tables'/name if tier=='ROBUST_CORE' else ROOT/'supplementary'/name
  d[d.evidence_tier==tier].to_csv(dest,index=False)
 print(m.to_string(index=False))
if __name__=='__main__':main()

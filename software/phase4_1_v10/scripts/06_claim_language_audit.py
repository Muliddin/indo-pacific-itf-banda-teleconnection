from common import *
def main():
 d=pd.read_csv(ROOT/'reports/claim_evidence_matrix.csv')
 terms=['causes','caused','mediates','mediated through','drives','is driven by','leads to']
 rows=[]
 for _,r in d.iterrows():
  if r.evidence_tier!='ROBUST_CORE':
   rows.append({'claim_id':r.claim_id,'evidence_tier':r.evidence_tier,'forbidden_or_risky_terms':' | '.join(terms),'recommended_language':r.recommended_language})
 out=pd.DataFrame(rows);out.to_csv(ROOT/'reports/claim_language_audit.csv',index=False)
 print('Audited non-core claims:',len(out))
if __name__=='__main__':main()

from common import *
def role(t):
 return {'ROBUST_CORE':'PRIMARY_RESULT','CONDITIONAL_SUPPORTING':'SUPPORTING_RESULT','EXPLORATORY_CONTEXTUAL':'DISCUSSION_CONTEXT'}.get(t,'DISCUSSION_CONTEXT')
def main():
 c=cfg();L=log('01_claim');p4=resolve(c['inputs']['phase4_root']);d=pd.read_csv(p4/'reports/evidence_registry.csv')
 d['claim_id']=[f'C{i:03d}' for i in range(1,len(d)+1)]
 d['manuscript_role']=d.evidence_tier.map(role)
 d['causal_language_allowed']=False
 d['recommended_language']=d.evidence_tier.map({'ROBUST_CORE':'robustly associated with','CONDITIONAL_SUPPORTING':'associated with under specified conditions','EXPLORATORY_CONTEXTUAL':'consistent with / contextual evidence'})
 d.to_csv(ROOT/'reports/claim_evidence_matrix.csv',index=False)
 print(d.manuscript_role.value_counts().to_string())
if __name__=='__main__':main()

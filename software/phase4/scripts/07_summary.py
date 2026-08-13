from common import *
def main():
 d=pd.read_csv(ROOT/'reports/evidence_registry.csv')
 rep={'phase':'Phase 4 - Synthesis, Figures, Robustness Summary & Manuscript Architecture','version':'v1.0','period':'1993-2025','evidence_rows':len(d),'robust_core':int((d.evidence_tier=='ROBUST_CORE').sum()),'conditional_supporting':int((d.evidence_tier=='CONDITIONAL_SUPPORTING').sum()),'exploratory_contextual':int((d.evidence_tier=='EXPLORATORY_CONTEXTUAL').sum()),'causal_claim_policy':'Associations/directionality only; formal mediation was not robust.','status':'PASS'}
 (ROOT/'reports/phase4_summary.json').write_text(json.dumps(rep,indent=2),encoding='utf-8');print(json.dumps(rep,indent=2))
if __name__=='__main__':main()

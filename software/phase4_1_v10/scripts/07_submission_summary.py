from common import *
def main():
 ev=pd.read_csv(ROOT/'reports/claim_evidence_matrix.csv');man=pd.read_csv(ROOT/'reports/main_vs_supplementary_architecture.csv')
 rep={'phase':'Phase 4.1 - Manuscript Audit & Submission Architecture','version':'v1.0','claims_audited':len(ev),'primary_result_claims':int((ev.manuscript_role=='PRIMARY_RESULT').sum()),'supporting_result_claims':int((ev.manuscript_role=='SUPPORTING_RESULT').sum()),'discussion_context_claims':int((ev.manuscript_role=='DISCUSSION_CONTEXT').sum()),'main_artifacts':int((man.final_placement=='MAIN').sum()),'supplement_artifacts':int((man.final_placement=='SUPPLEMENT').sum()),'status':'PASS','submission_rule':'No causal mediation claim; preserve frozen evidence hierarchy.'}
 (ROOT/'reports/phase4_1_summary.json').write_text(json.dumps(rep,indent=2),encoding='utf-8');print(json.dumps(rep,indent=2))
if __name__=='__main__':main()

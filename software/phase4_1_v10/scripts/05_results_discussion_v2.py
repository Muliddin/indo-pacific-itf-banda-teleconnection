from common import *
def main():
 c=cfg();p4=resolve(c['inputs']['phase4_root'])
 base=(p4/'manuscript/Results_Discussion_DRAFT.md').read_text(encoding='utf-8')
 audit=pd.read_csv(ROOT/'reports/claim_evidence_matrix.csv')
 nrob=int((audit.evidence_tier=='ROBUST_CORE').sum());ncond=int((audit.evidence_tier=='CONDITIONAL_SUPPORTING').sum());nexp=int((audit.evidence_tier=='EXPLORATORY_CONTEXTUAL').sum())
 pre=f'''# Results and Discussion v2 — audited synthesis\n\n**Evidence policy.** This draft is constrained by the frozen Phase 4 evidence registry: {nrob} robust/core, {ncond} conditional/supporting, and {nexp} exploratory/contextual findings. Robust/core evidence supports primary associative claims; conditional evidence retains explicit model/season/lag qualification; exploratory findings are used only for context. Formal mediation was not robust and is not described causally.\n\n'''
 txt=pre+base
 txt=txt.replace('supports physical connectivity','is consistent with physical connectivity')
 txt=txt.replace('provides a strong atmospheric pathway','is consistent with a strong atmospheric pathway')
 txt=txt.replace('identify both oceanic and atmospheric pathways','identify statistical patterns consistent with both oceanic and atmospheric pathways')
 txt += '''\n\n# Submission-facing synthesis\n\nThe central contribution is not a claim of a single serial causal chain. Instead, the 1993–2025 evidence supports a robust, seasonally structured ENSO/IOD–ITF teleconnection embedded within a coupled ocean–atmosphere response of the Banda Sea. Total ITF outflow and full Ekman pumping covary coherently with upper-ocean heat content, but neither yields a statistically separable indirect effect once the climate modes and parallel pathway are accounted for. This distinction should remain explicit in the Abstract, Results, Discussion, and Conclusions.\n'''
 (ROOT/'manuscript/Results_Discussion_v2_AUDITED.md').write_text(txt,encoding='utf-8')
 print('WROTE audited Results–Discussion v2')
if __name__=='__main__':main()

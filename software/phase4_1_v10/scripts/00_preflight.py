from common import *
def main():
 c=cfg();L=log('00_preflight');p4=resolve(c['inputs']['phase4_root'])
 req=[p4/'reports/evidence_registry.csv',p4/'reports/robustness_matrix.csv',p4/'reports/phase4_summary.json',p4/'manuscript/Results_Discussion_DRAFT.md']
 rows=[];miss=[]
 for p in req:
  ok=p.exists();rows.append({'path':str(p),'exists':ok})
  if not ok:miss.append(str(p))
 pd.DataFrame(rows).to_csv(ROOT/'reports/preflight_inputs.csv',index=False)
 if miss:raise FileNotFoundError('Missing Phase4 inputs:\n'+'\n'.join(miss))
 L.info('PASS')
if __name__=='__main__':main()

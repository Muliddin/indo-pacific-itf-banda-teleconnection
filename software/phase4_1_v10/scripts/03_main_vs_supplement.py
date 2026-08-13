from common import *
def main():
 c=cfg();p4=resolve(c['inputs']['phase4_root'])
 man=pd.read_csv(ROOT/'reports/final_figure_table_manifest.csv')
 rows=[]
 for _,r in man.iterrows():
  place=r.placement
  if place=='MAIN_OR_SUPPLEMENT':
   place='SUPPLEMENT' if 'mediation' in r.artifact.lower() else 'MAIN'
  rows.append({**r.to_dict(),'final_placement':place})
 out=pd.DataFrame(rows)
 out.to_csv(ROOT/'reports/main_vs_supplementary_architecture.csv',index=False)
 print(out[['artifact_type','artifact','final_placement']].to_string(index=False))
if __name__=='__main__':main()

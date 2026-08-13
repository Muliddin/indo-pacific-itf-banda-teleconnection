from common import *
def main():
 c=cfg();p4=resolve(c['inputs']['phase4_root']);rows=[]
 for n in c['main_figures']:rows.append({'artifact_type':'figure','artifact':n,'placement':'MAIN','priority':'CORE','source':str(p4/'figures'/n)})
 for n in c['candidate_main_figures']:rows.append({'artifact_type':'figure','artifact':n,'placement':'MAIN_OR_SUPPLEMENT','priority':'SECONDARY','source':str(p4/'figures'/n)})
 for n in c['main_tables']:rows.append({'artifact_type':'table','artifact':n,'placement':'MAIN','priority':'CORE','source':str(p4/'tables'/n)})
 for n in c['supplementary_tables']:rows.append({'artifact_type':'table','artifact':n,'placement':'SUPPLEMENT','priority':'SUPPORTING','source':str(p4/'tables'/n)})
 out=pd.DataFrame(rows);out['exists']=out.source.map(lambda x:Path(x).exists());out.to_csv(ROOT/'reports/final_figure_table_manifest.csv',index=False)
 print(out.to_string(index=False))
if __name__=='__main__':main()

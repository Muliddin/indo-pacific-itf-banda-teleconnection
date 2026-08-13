from common import *
import matplotlib.pyplot as plt
def main():
 c=cfg();dpi=c['figures']['dpi']
 # Fig 1 transport validation
 d=pd.read_csv(ROOT/'tables/Table_S1_ITF_section_validation.csv')
 fig,ax=plt.subplots(figsize=(7,4.5))
 x=np.arange(len(d)); obs=d['reference_mean_2004_2006_sv']; mod=d['canonical_mean_2004_2006_sv']
 ax.bar(x-0.18,obs,0.36,label='Reference');ax.bar(x+0.18,mod,0.36,label='GLORYS native-grid')
 ax.set_xticks(x);ax.set_xticklabels(d.section_id.str.title());ax.set_ylabel('Transport (Sv)');ax.legend();fig.tight_layout()
 fig.savefig(ROOT/'figures/Figure_1_ITF_section_validation.png',dpi=dpi,bbox_inches='tight');plt.close(fig)
 # Fig 2 climate->ITF frozen effects
 a=pd.read_csv(ROOT/'tables/Table_2_ENSO_IOD_ITF_lagged.csv')
 a=a[a.freeze_status=='FREEZE'].copy()
 fig,ax=plt.subplots(figsize=(9,5))
 vals=a.r_best_positive if 'r_best_positive' in a else a.iloc[:,3]
 labels=[f"{i}\\n{t.replace('transport_','').replace('_sv','')}" for i,t in zip(a['index'],a.target)]
 ax.bar(range(len(a)),vals);ax.axhline(0,lw=.8);ax.set_xticks(range(len(a)));ax.set_xticklabels(labels,rotation=45,ha='right');ax.set_ylabel('Correlation at frozen positive lag');fig.tight_layout()
 fig.savefig(ROOT/'figures/Figure_2_climate_ITF_frozen_effects.png',dpi=dpi,bbox_inches='tight');plt.close(fig)
 # Fig 3 ITF-Banda
 b=pd.read_csv(ROOT/'tables/Table_4_ITF_Banda_coupling.csv')
 fig,ax=plt.subplots(figsize=(10,5))
 col='r_best_positive' if 'r_best_positive' in b else ('r_at_best' if 'r_at_best' in b else b.select_dtypes('number').columns[0])
 labels=[f"{str(x).replace('transport_','')}→{str(y).replace('_banda_anom','')}" for x,y in zip(b.iloc[:,0],b.iloc[:,1])]
 ax.bar(range(len(b)),b[col]);ax.axhline(0,lw=.8);ax.set_xticks(range(len(b)));ax.set_xticklabels(labels,rotation=70,ha='right',fontsize=7);ax.set_ylabel('Lagged coupling r');fig.tight_layout()
 fig.savefig(ROOT/'figures/Figure_3_ITF_Banda_coupling.png',dpi=dpi,bbox_inches='tight');plt.close(fig)
 # Fig 4 mediation
 p=pd.read_csv(ROOT/'tables/Table_5_parallel_mediation.csv')
 fig,ax=plt.subplots(figsize=(8,5));x=np.arange(len(p));w=.25
 ax.bar(x-w,p.indirect_qout,w,label='Qout indirect');ax.bar(x,p.indirect_ekman,w,label='Ekman indirect');ax.bar(x+w,p.direct_effect,w,label='Direct')
 ax.axhline(0,lw=.8);ax.set_xticks(x);ax.set_xticklabels([f"{d}→{o}" for d,o in zip(p.driver,p.outcome)],rotation=45,ha='right');ax.set_ylabel('Standardized effect');ax.legend();fig.tight_layout()
 fig.savefig(ROOT/'figures/Figure_4_mediation_decomposition.png',dpi=dpi,bbox_inches='tight');plt.close(fig)
 print('WROTE 4 publication figures')
if __name__=='__main__':main()

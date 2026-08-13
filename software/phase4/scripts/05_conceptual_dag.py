from common import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
def main():
 fig,ax=plt.subplots(figsize=(10,6));ax.axis('off')
 pos={'ENSO':(.1,.75),'IOD':(.1,.25),'ITF / Qout':(.48,.68),'Wind / Full Ekman':(.48,.28),'Banda OHC':(.85,.5)}
 for n,(x,y) in pos.items():ax.text(x,y,n,ha='center',va='center',bbox=dict(boxstyle='round,pad=.5',fc='white',ec='black'))
 def ar(a,b,style='-',lw=2):
  A=pos[a];B=pos[b];ax.add_patch(FancyArrowPatch(A,B,arrowstyle='-|>',mutation_scale=15,lw=lw,linestyle=style,shrinkA=35,shrinkB=35))
 ar('ENSO','ITF / Qout');ar('IOD','ITF / Qout');ar('ENSO','Wind / Full Ekman');ar('IOD','Wind / Full Ekman')
 ar('ITF / Qout','Banda OHC','--');ar('Wind / Full Ekman','Banda OHC','--')
 ax.text(.5,.05,'Solid: robust climate-system association   Dashed: mechanistic coupling; formal mediation not identified',ha='center',fontsize=9)
 fig.tight_layout();fig.savefig(ROOT/'figures/Figure_5_conceptual_DAG.png',dpi=300,bbox_inches='tight');plt.close(fig)
 print('WROTE conceptual DAG')
if __name__=='__main__':main()

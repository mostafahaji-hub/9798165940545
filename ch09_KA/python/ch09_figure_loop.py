import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'DejaVu Sans','font.weight':'bold','savefig.facecolor':'white'})
BLUE='#0B3D91'; ORANGE='#E8600A'; GREEN='#118C4F'; RED='#C8102E'; GREY='#666666'; PURPLE='#6A1B9A'; GOLD='#D4A017'
fig,ax=plt.subplots(figsize=(9,5.9)); ax.set_xlim(0,18); ax.set_ylim(0.6,12.4); ax.set_aspect('equal'); ax.axis('off')
S=[(3,8.9,'1  LOOK','watch a living thing:\nhow does it solve\nits problem?',BLUE),(9,8.9,'2  FIND THE SIGNAL','visible, simple,\ngeometric',PURPLE),(15,8.9,'3  MAP IT','"my solution space is ...\neach solution is a ..."',GREEN),
   (15,2.9,'4  CODE EARLY','the code\ndoes not lie',ORANGE),(9,2.9,'5  BENCHMARK','standard functions,\n30 runs, fair rivals',RED),(3,2.9,'6  NAME AND SHARE','ridicule -> opposition\n-> acceptance',GOLD)]
for x,y,t,b,c in S:
    ax.add_patch(FancyBboxPatch((x-2.5,y-1.5),5.0,3.0,boxstyle='round,pad=0.1',fc='white',ec=c,lw=3))
    ax.text(x,y+0.85,t,ha='center',va='center',fontsize=13,fontweight='bold',color=c); ax.text(x,y-0.35,b,ha='center',va='center',fontsize=11.5,fontweight='bold',linespacing=1.25)
A=dict(arrowstyle='-|>',lw=3,color=GREY,mutation_scale=22)
for (x1,y1),(x2,y2) in [((5.55,8.9),(6.45,8.9)),((11.55,8.9),(12.45,8.9)),((15,7.3),(15,4.5)),((12.45,2.9),(11.55,2.9)),((6.45,2.9),(5.55,2.9)),((3,4.5),(3,7.3))]:
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=A)
ax.text(9,5.9,'Go round this loop once and\nyou will never look at nature\nthe same way again',ha='center',va='center',fontsize=13,fontweight='bold',color=BLUE,linespacing=1.3)
plt.tight_layout(); plt.savefig('fig/fig9_16_loop.png',dpi=300); plt.close()

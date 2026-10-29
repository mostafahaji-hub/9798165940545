import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, math
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({'font.family':'DejaVu Sans','font.weight':'bold','savefig.facecolor':'white'})
BLUE='#0B3D91'; ORANGE='#E8600A'; GREEN='#118C4F'; RED='#C8102E'; GREY='#666666'; PURPLE='#6A1B9A'; GOLD='#D4A017'
# ---- 9-7 KASA (orthogonal return path below the boxes, nothing clipped)
fig,ax=plt.subplots(figsize=(13.5,4.6)); ax.set_xlim(0,27); ax.set_ylim(-0.4,7); ax.axis('off')
B=[(2.6,'lucky Keshtel L\n(one of the best N1)',GOLD),(8.0,'SWIRL (KA)\ndiagnostic + bisection\naround L',BLUE),(13.5,'SHORT SA from L\n10 evaluations;\naccept worse with\np = exp(-D/T)',PURPLE),(19.0,'best point of SA\n(never worse than L)',GREEN),(24.4,'replaces L\nin the lake',GOLD)]
for xx,t,c in B: ax.add_patch(FancyBboxPatch((xx-2.2,2.6),4.4,2.5,boxstyle='round,pad=0.12',fc='white',ec=c,lw=2.6)); ax.text(xx,3.85,t,ha='center',va='center',fontsize=11.5,fontweight='bold')
for a,b in zip(B,B[1:]): ax.annotate('',xy=(b[0]-2.35,3.85),xytext=(a[0]+2.35,3.85),arrowprops=dict(arrowstyle='-|>',lw=2.6))
ax.plot([24.4,24.4,2.6],[2.45,1.55,1.55],color=GREY,lw=2.2); ax.annotate('',xy=(2.6,2.45),xytext=(2.6,1.55),arrowprops=dict(arrowstyle='-|>',lw=2.2,color=GREY))
ax.text(13.5,1.55,'next lucky Keshtel (or next iteration)',ha='center',va='center',fontsize=10.5,fontweight='bold',color=GREY,bbox=dict(fc='white',ec='none',pad=0.3))
ax.text(13.5,0.25,'phases 2 and 3 (fly away / hustle) are unchanged; SA only polishes the lucky Keshtels',ha='center',fontsize=11,fontweight='bold',color=GREY)
ax.text(13.5,6.35,'KASA: the Keshtel algorithm with simulated annealing as the local search of each lucky Keshtel',ha='center',fontsize=12.5,fontweight='bold')
plt.tight_layout(); plt.savefig('fig/fig9_9_kasa.png',dpi=300); plt.close()
# ---- 9-14 (was 9-15) the creation loop: bigger, more readable fonts
fig,ax=plt.subplots(figsize=(10.5,10.5)); ax.set_xlim(-6.9,6.9); ax.set_ylim(-6.9,6.9); ax.set_aspect('equal'); ax.axis('off')
st=['1  LOOK\nwatch a living thing:\nhow does it solve\nits problem?','2  FIND THE SIGNAL\nvisible, simple,\ngeometric','3  MAP IT\n"my solution space is ...\neach solution is a ..."','4  CODE EARLY\nthe code\ndoes not lie','5  BENCHMARK\nstandard functions,\n30 runs, fair rivals','6  NAME AND SHARE\nridicule -> opposition\n-> acceptance']
cols=[BLUE,PURPLE,GREEN,ORANGE,RED,GOLD]; R=4.6
for k,(t,c) in enumerate(zip(st,cols)):
    a=math.radians(90-60*k); x,y=R*math.cos(a),R*math.sin(a)
    ax.add_patch(FancyBboxPatch((x-2.05,y-1.15),4.1,2.3,boxstyle='round,pad=0.12',fc='white',ec=c,lw=3)); ax.text(x,y,t,ha='center',va='center',fontsize=12.5,fontweight='bold',linespacing=1.25)
    a1,a2=math.radians(90-60*k-18),math.radians(90-60*k-42); r0=2.95
    ax.add_patch(FancyArrowPatch((r0*math.cos(a1),r0*math.sin(a1)),(r0*math.cos(a2),r0*math.sin(a2)),arrowstyle='-|>',mutation_scale=24,lw=3,color=GREY,connectionstyle='arc3,rad=-0.35'))
ax.text(0,0,'Go round this loop once\nand you will never look\nat nature the same way',ha='center',va='center',fontsize=14,fontweight='bold',color=BLUE,linespacing=1.3)
plt.tight_layout(); plt.savefig('fig/fig9_16_loop.png',dpi=300); plt.close()

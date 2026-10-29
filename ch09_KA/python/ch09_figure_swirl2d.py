import os
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, random, math
from matplotlib.patches import Ellipse, Circle, FancyBboxPatch, Polygon, Arc, FancyArrowPatch, Rectangle
from ch09_ka import ka, Bench
plt.rcParams.update({'font.size':13,'axes.linewidth':1.8,'lines.linewidth':2.5,'font.family':'DejaVu Sans','savefig.facecolor':'white','font.weight':'bold','axes.labelweight':'bold'})
BLUE='#0B3D91'; ORANGE='#E8600A'; GREEN='#118C4F'; RED='#C8102E'; GREY='#666666'; PURPLE='#6A1B9A'; GOLD='#D4A017'; LAKE='#D6ECF7'
BOX=lambda c='black':dict(fc='white',ec=c,lw=1.3,boxstyle='round,pad=0.25')
def save(n): plt.tight_layout(); plt.savefig(f'fig/{n}.png',dpi=300); plt.close()
def duck(ax,x,y,s,body,head='#2E5E3E',z=6,flip=False):
    d=-1 if flip else 1
    ax.add_patch(Ellipse((x,y),1.0*s,0.55*s,fc=body,ec='black',lw=1.2,zorder=z))
    ax.add_patch(Circle((x+d*0.42*s,y+0.28*s),0.2*s,fc=head,ec='black',lw=1.2,zorder=z+1))
    ax.add_patch(Ellipse((x+d*0.72*s,y+0.24*s),0.36*s,0.14*s,fc='#E0A030',ec='black',lw=1,zorder=z+1))
    ax.add_patch(Circle((x+d*0.47*s,y+0.33*s),0.035*s,fc='white',ec='none',zorder=z+2))
# ---------- 9-5 swirl in 2-D (mixed probes)
f2=lambda p:(p[0]-1.2)**2+2.5*(p[1]-0.6)**2+1.2*(p[0]-1.2)*(p[1]-0.6)
pop=[[-2.2,2.0],[-1.0,-1.6],[0.3,2.4],[2.6,-2.0],[-0.6,1.1],[-1.7,0.1]]
li=min(range(6),key=lambda i:f2(pop[i])); L=list(pop[li]); fL=f2(L); rng=random.Random(3)
near=lambda pt:min((i for i in range(6) if i!=li),key=lambda i:abs(pop[i][0]-pt[0])+abs(pop[i][1]-pt[1]))
centres=[list(L)]; neigh=[pop[near(L)]]; probes=[]; Smax=3; A=pop[near(L)]; cnt=0
while cnt<16:
    r=[L[0]-A[0],L[1]-A[1]]; O=[L[0]+r[0],L[1]+r[1]]; fO=f2(O); cnt+=1; probes.append((O,'diag',fO<fL))
    if fO<fL: L,fL=O,fO; pop[li]=L; A=pop[near(L)]; centres.append(list(L)); neigh.append(A); continue
    moved=False
    for s in range(1,Smax+1):
        rho=0.5**s; u=[rng.gauss(0,1),rng.gauss(0,1)]; nu=math.hypot(*u); rad=math.hypot(*r); j=rng.randrange(2); cc=list(L); cc[j]+=rng.choice((-1,1))*rho*(abs(r[0])+abs(r[1]))
        for c,tg in [([L[0]+rho*r[0],L[1]+rho*r[1]],'axis'),([L[0]-rho*r[0],L[1]-rho*r[1]],'axis'),([L[0]+rho*rad*u[0]/nu,L[1]+rho*rad*u[1]/nu],'random'),(cc,'coord')]:
            fc=f2(c); cnt+=1; probes.append((c,tg,fc<fL))
            if fc<fL: L,fL=c,fc; pop[li]=L; A=pop[near(L)]; centres.append(list(L)); neigh.append(A); moved=True; break
        if moved: break
    if not moved: break
X,Y=np.meshgrid(np.linspace(-3,3.5,300),np.linspace(-2.6,3,300)); Zg=(X-1.2)**2+2.5*(Y-0.6)**2+1.2*(X-1.2)*(Y-0.6)
fig,ax=plt.subplots(figsize=(9.6,8)); ax.contourf(X,Y,np.log10(Zg+0.05),levels=25,cmap='Blues_r',alpha=0.75); ax.contour(X,Y,np.log10(Zg+0.05),levels=12,colors='white',linewidths=0.6)
for p in [q for k,q in enumerate([[-2.2,2.0],[-1.0,-1.6],[0.3,2.4],[2.6,-2.0],[-0.6,1.1],[-1.7,0.1]]) if k!=li]: ax.scatter(*p,s=110,color='#9AA9BC',edgecolor='black',zorder=4)
mk={'diag':'D','axis':'o','random':'^','coord':'s'}
for k,(p,tg,ok) in enumerate(probes[:14]):
    ax.scatter(*p,s=95,marker=mk[tg],color=GREEN if ok else RED,edgecolor='black',zorder=6)
    ax.text(p[0]+0.12,p[1]+0.12,str(k+1),fontsize=9,fontweight='bold',bbox=dict(fc='white',ec=GREEN if ok else RED,boxstyle='round,pad=0.15'),zorder=7)
for a,b in zip(centres,centres[1:]): ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='-|>',lw=3,color=GOLD),zorder=8)
ax.scatter(*centres[0],s=300,marker='*',color=GOLD,edgecolor='black',zorder=9); ax.text(centres[0][0]-0.2,centres[0][1]+0.3,'L (start)',fontsize=10,fontweight='bold',ha='right',bbox=BOX(GOLD))
ax.scatter(*centres[-1],s=300,marker='*',color=GREEN,edgecolor='black',zorder=9); ax.annotate('L (end)',xy=centres[-1],xytext=(2.3,-0.75),fontsize=10,fontweight='bold',bbox=BOX(GREEN),arrowprops=dict(arrowstyle='-|>',lw=2,color=GREEN),zorder=10)
ax.scatter([1.2],[0.6],s=160,marker='P',color='black',zorder=9); ax.annotate('optimum (1.2, 0.6)',xy=(1.2,0.6),xytext=(-0.6,-0.9),fontsize=9.5,fontweight='bold',bbox=BOX(),arrowprops=dict(arrowstyle='-|>',lw=2),zorder=10)
for tg,lab in [('diag','diagnostic point O'),('axis','axis points  L +/- r/2^s'),('random','random direction on the circle'),('coord','one coordinate moved')]: ax.scatter([],[],marker=mk[tg],color='white',edgecolor='black',s=80,label=lab)
ax.scatter([],[],color=GREEN,s=80,label='better: the centre moves'); ax.scatter([],[],color=RED,s=80,label='worse: keep swirling')
ax.legend(fontsize=9,loc='lower left'); ax.set_xlabel('x1'); ax.set_ylabel('x2'); ax.set_title(f'Swirling of one lucky Keshtel in 2-D ({len(centres)-1} centre moves, {cnt} evaluations)',fontsize=12,fontweight='bold'); save('fig9_5_swirl2d')
print('swirl2d',len(centres)-1,'moves',cnt,'evals',[round(v,3) for v in centres[-1]],round(fL,4),flush=True)

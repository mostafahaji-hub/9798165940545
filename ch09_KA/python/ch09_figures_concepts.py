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
# ---------- 9-1 two searchers
x=np.linspace(0,10,600); f=lambda x:3+0.9*np.sin(1.25*x)+0.55*np.sin(3.3*x)-1.6*np.exp(-((x-8.2)/0.35)**2)
fig,ax=plt.subplots(figsize=(10,4.4)); ax.plot(x,f(x),color='black',lw=2.5)
dx=np.array([1.9,2.05,2.15,2.25,2.35,2.45,2.55,2.1,2.3]); ax.scatter(dx,f(dx),s=90,color=ORANGE,edgecolor='black',zorder=5,label='deep searcher: many careful steps in one valley')
wx=np.array([0.5,3.6,5.0,6.3,7.4,9.3,4.4]); ax.scatter(wx,f(wx),s=90,marker='s',color=BLUE,edgecolor='black',zorder=5,label='wide searcher: everywhere, but never deep')
ax.scatter([8.2],[f(8.2)],s=420,marker='*',color=GOLD,edgecolor='black',zorder=6,label='the key (global optimum)')
ax.text(8.2,f(8.2)-0.55,'the key',ha='center',fontsize=12,fontweight='bold',bbox=BOX(GOLD))
ax.set_xlabel('where you search'); ax.set_ylabel('how bad it is (lower is better)'); ax.set_ylim(0.2,5.6); ax.legend(fontsize=10,loc='upper right'); ax.grid(alpha=0.25)
ax.set_title('Two ways of searching for a lost key: depth and breadth must talk to each other',fontsize=12,fontweight='bold'); save('fig9_1_keyroom')
# ---------- 9-2 the lake and the three groups
fig,ax=plt.subplots(figsize=(12,7.6)); ax.set_xlim(0,20); ax.set_ylim(-0.3,12.8); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Ellipse((10,7),18.5,8.8,fc=LAKE,ec=BLUE,lw=2.5,zorder=1)); ax.text(10,11.65,'THE LAKE = the solution space',ha='center',fontsize=13,fontweight='bold',color=BLUE)
for (cx,cy) in [(5,8.2),(11.2,9.0)]:
    for rr in (1.35,0.9,0.5): ax.add_patch(Circle((cx,cy),rr,fc='none',ec=GOLD,lw=2,ls='--',zorder=2))
    duck(ax,cx,cy,0.9,GOLD); duck(ax,cx+1.25,cy-0.5,0.6,'#F2D27A',flip=True)
    ax.annotate('',xy=(cx+0.2,cy-1.32),xytext=(cx+1.15,cy-0.75),arrowprops=dict(arrowstyle='-|>',lw=2,color=GOLD,connectionstyle='arc3,rad=-0.4'),zorder=3)
ax.text(5,6.35,'lucky Keshtel swirls;\nnearest neighbour circles it',ha='center',fontsize=9.5,fontweight='bold',bbox=BOX(GOLD))
for (x0,y0,x1,y1) in [(3.2,4.8,1.2,1.4),(16.6,9.2,18.8,12.2),(17.6,5.4,19.6,3.0)]:
    duck(ax,x0,y0,0.75,RED); ax.annotate('',xy=(x1,y1),xytext=(x0,y0),arrowprops=dict(arrowstyle='-|>',lw=2.2,color=RED,ls='--'),zorder=4)
ax.text(1.5,0.55,'unlucky: fly away',fontsize=10,fontweight='bold',color=RED,bbox=BOX(RED))
for (x0,y0,x1,y1) in [(13.2,12.6,13.6,7.6),(8.0,12.6,7.6,4.6)]:
    ax.annotate('',xy=(x1,y1+0.3),xytext=(x0,y0),arrowprops=dict(arrowstyle='-|>',lw=2.2,color=GREEN),zorder=4); duck(ax,x1,y1,0.75,'#8BD3A5')
ax.text(10.6,12.35,'new Keshtels land',fontsize=10,fontweight='bold',color=GREEN,bbox=BOX(GREEN))
rest=[(9.0,6.4),(12.8,4.6),(15.2,7.2),(6.6,3.9),(10.5,3.4)]
for (x0,y0),(x1,y1) in zip(rest,[(10.2,5.6),(13.9,5.6),(14.6,6.0),(7.9,4.5),(11.6,4.4)]):
    duck(ax,x0,y0,0.7,'#7FA8E0'); ax.annotate('',xy=(x1,y1),xytext=(x0+0.3,y0),arrowprops=dict(arrowstyle='-|>',lw=2,color=BLUE),zorder=4)
ax.text(12.7,2.25,'the rest: hustle toward empty water',ha='center',fontsize=10,fontweight='bold',color=BLUE,bbox=BOX(BLUE))
y0=-0.15; ax.add_patch(Rectangle((2,y0),3.2,0.75,fc=GOLD,ec='black',lw=1.5)); ax.add_patch(Rectangle((5.2,y0),8.0,0.75,fc='#7FA8E0',ec='black',lw=1.5)); ax.add_patch(Rectangle((13.2,y0),4.8,0.75,fc=RED,ec='black',lw=1.5))
for xx,t in [(3.6,'N1 lucky'),(9.2,'N3 rest'),(15.6,'N2 unlucky')]: ax.text(xx,y0+0.37,t,ha='center',va='center',fontsize=10.5,fontweight='bold',color='white' if 'N2' in t else 'black')
for xx in (5.2,13.2): ax.add_patch(Polygon([(xx-0.3,y0-0.42),(xx+0.3,y0-0.42),(xx,y0-0.02)],closed=True,fc='black'))
ax.text(18.3,y0+0.37,'<- you move\n    the sliders',fontsize=9.5,fontweight='bold',va='center'); save('fig9_2_lake')
# ---------- 9-3 diagnostic question and bisection (1-D example)
g=lambda x:(x-3.3)**2+1; xs=np.linspace(0.6,5.8,400)
fig,axs=plt.subplots(1,2,figsize=(13,5.2))
ax=axs[0]; ax.plot(xs,g(xs),color='black')
for (px,lab,col,mk) in [(1.0,'A neighbour\nf = 6.29',BLUE,'o'),(2.0,'L lucky\nf = 2.69',GOLD,'o'),(3.0,'O = L + (L - A)\nf = 1.09',GREEN,'o')]:
    ax.scatter([px],[g(px)],s=170,color=col,edgecolor='black',marker=mk,zorder=5); ax.text(px,g(px)+0.95,lab,ha='center',fontsize=10,fontweight='bold',bbox=BOX(col))
ax.add_patch(Arc((2.0,0.0),2.0,2.6,theta1=0,theta2=180,color=GOLD,lw=2.5,ls='--'))
ax.annotate('',xy=(3.0,1.6),xytext=(2.05,2.95),arrowprops=dict(arrowstyle='-|>',lw=3,color=GREEN))
ax.set_title('(a) SLOPE: f(O) < f(L)\nthe circle moves to O at once',fontsize=12,fontweight='bold'); ax.set_ylim(-0.2,9.5); ax.set_xlabel('x'); ax.set_ylabel('f(x) = (x - 3.3)^2 + 1'); ax.grid(alpha=0.25)
ax=axs[1]; ax.plot(xs,g(xs),color='black'); L=3.0
for rr,c in [(1.8,GOLD),(0.9,'#C9A227'),(0.45,'#9C7C10')]: ax.add_patch(Arc((L,0.0),2*rr,1.8*rr+0.4,theta1=0,theta2=180,color=c,lw=2.2,ls='--'))
ax.scatter([L],[g(L)],s=190,color=GOLD,edgecolor='black',zorder=6); ax.text(L,g(L)-1.0,'L = 3.0, f = 1.09',ha='center',fontsize=10,fontweight='bold',bbox=BOX(GOLD))
ax.scatter([4.8],[g(4.8)],s=170,color=BLUE,edgecolor='black',zorder=6); ax.text(4.8,g(4.8)+0.9,'A = 4.8',ha='center',fontsize=10,fontweight='bold',bbox=BOX(BLUE))
probes=[(1.2,'1','O'),(2.1,'2','s=1'),(3.9,'3','s=1'),(2.55,'4','s=2'),(3.45,'5','s=2')]
for px,no,tg in probes:
    better=g(px)<g(L); ax.scatter([px],[g(px)],s=150,marker='o' if better else 'X',color=GREEN if better else RED,edgecolor='black',zorder=7)
    ax.text(px+(0.0 if px<3 else 0.0),g(px)+0.65,no,ha='center',fontsize=11,fontweight='bold',bbox=dict(fc='white',ec=GREEN if better else RED,boxstyle='circle,pad=0.25'),zorder=8)
ax.text(1.0,8.6,'1: O = 1.2 (worse) -> a pit\n2,3: radius 1.8/2 (worse)\n4,5: radius 1.8/4 -> 3.45 better',fontsize=9.5,fontweight='bold',va='top',bbox=BOX())
ax.set_title('(b) PIT: f(O) > f(L)\nbisection rounds with radius r/2, r/4, ...',fontsize=12,fontweight='bold'); ax.set_ylim(-0.2,9.5); ax.set_xlabel('x'); ax.grid(alpha=0.25)
save('fig9_3_diagnostic')
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
ax.scatter(*centres[-1],s=300,marker='*',color=GREEN,edgecolor='black',zorder=9); ax.text(centres[-1][0]+0.25,centres[-1][1]-0.35,'L (end)',fontsize=10,fontweight='bold',bbox=BOX(GREEN))
ax.scatter([1.2],[0.6],s=160,marker='P',color='black',zorder=9); ax.text(1.32,0.75,'optimum',fontsize=9.5,fontweight='bold',bbox=BOX())
for tg,lab in [('diag','diagnostic point O'),('axis','axis points  L +/- r/2^s'),('random','random direction on the circle'),('coord','one coordinate moved')]: ax.scatter([],[],marker=mk[tg],color='white',edgecolor='black',s=80,label=lab)
ax.scatter([],[],color=GREEN,s=80,label='better: the centre moves'); ax.scatter([],[],color=RED,s=80,label='worse: keep swirling')
ax.legend(fontsize=9,loc='lower left'); ax.set_xlabel('x1'); ax.set_ylabel('x2'); ax.set_title(f'Swirling of one lucky Keshtel in 2-D ({len(centres)-1} centre moves, {cnt} evaluations)',fontsize=12,fontweight='bold'); save('fig9_5_swirl2d')
print('swirl2d',len(centres)-1,'moves',cnt,'evals',[round(v,3) for v in centres[-1]],round(fL,4),flush=True)
# ---------- 9-6 hustle toward empty water
fig,ax=plt.subplots(figsize=(9,6)); ax.set_xlim(0,7); ax.set_ylim(0,5.2); ax.set_aspect('equal'); ax.grid(alpha=0.2)
Xp,G,H=np.array([1.0,1.0]),np.array([4.0,4.2]),np.array([5.2,1.6]); Mp=(G+H)/2; Yp=Xp+0.5*(Mp-Xp)
ax.plot([G[0],H[0]],[G[1],H[1]],ls='--',color=GREY,lw=2); ax.plot([Xp[0],Mp[0]],[Xp[1],Mp[1]],color='#BBBBBB',lw=6,solid_capstyle='round',zorder=1)
for p,lab,col in [(Xp,'X (moving Keshtel)',BLUE),(G,'G',PURPLE),(H,'H',PURPLE)]: duck(ax,p[0],p[1],0.55,col if col!=BLUE else '#7FA8E0'); ax.text(p[0],p[1]-0.6,lab,ha='center',fontsize=10.5,fontweight='bold',bbox=BOX(col))
ax.scatter(*Mp,s=170,marker='s',color='white',edgecolor='black',zorder=6); ax.text(Mp[0]+0.25,Mp[1]+0.25,'M = (G + H)/2\n= (4.6, 2.9)',fontsize=10.5,fontweight='bold',bbox=BOX())
ax.annotate('',xy=Yp,xytext=Xp+np.array([0.25,0.1]),arrowprops=dict(arrowstyle='-|>',lw=3.5,color=GREEN),zorder=7)
duck(ax,Yp[0],Yp[1],0.55,'#8BD3A5'); ax.text(Yp[0]-0.1,Yp[1]+0.5,'Y = X + lambda (M - X)\nlambda = 0.5  ->  (2.8, 1.95)',fontsize=10.5,fontweight='bold',ha='center',bbox=BOX(GREEN))
ax.text(3.5,0.25,'grey band: every possible landing place for lambda in [0, 1]',fontsize=10,fontweight='bold',ha='center',color=GREY)
ax.set_title('Hustle: a Keshtel moves toward the empty water between two others',fontsize=12,fontweight='bold'); ax.set_xticks(range(8)); save('fig9_6_hustle')
# ---------- 9-9 KASA
fig,ax=plt.subplots(figsize=(13,3.6)); ax.set_xlim(0,26); ax.set_ylim(0,7); ax.axis('off')
B=[(2.2,'lucky Keshtel L\n(one of the best N1)',GOLD),(7.6,'SWIRL (KA)\ndiagnostic + bisection\naround L',BLUE),(13.4,'SHORT SA from L\n10 evaluations,\naccept worse with p = exp(-D/T)',PURPLE),(19.2,'best point of SA\n(never worse than L)',GREEN),(24.0,'replaces L\nin the lake',GOLD)]
for xx,t,c in B: ax.add_patch(FancyBboxPatch((xx-2.2,2.4),4.4,2.4,boxstyle='round,pad=0.15',fc='white',ec=c,lw=2.5)); ax.text(xx,3.6,t,ha='center',va='center',fontsize=10.5,fontweight='bold')
for a,b in zip(B,B[1:]): ax.annotate('',xy=(b[0]-2.3,3.6),xytext=(a[0]+2.3,3.6),arrowprops=dict(arrowstyle='-|>',lw=2.5))
ax.annotate('',xy=(2.2,2.3),xytext=(24.0,2.3),arrowprops=dict(arrowstyle='-|>',lw=2,color=GREY,connectionstyle='arc3,rad=0.12'))
ax.text(13,0.45,'phases 2 and 3 (fly away / hustle) are unchanged; SA only polishes the lucky ones',ha='center',fontsize=10.5,fontweight='bold',color=GREY)
ax.text(13,6.3,'KASA: the Keshtel algorithm with simulated annealing as the local search of each lucky Keshtel',ha='center',fontsize=12,fontweight='bold'); save('fig9_9_kasa')
# ---------- 9-16 the creation loop (six stations)
fig,ax=plt.subplots(figsize=(9.5,9.5)); ax.set_xlim(-6,6); ax.set_ylim(-6,6); ax.set_aspect('equal'); ax.axis('off')
st=['1  LOOK\nwatch living things\nand ask: how does it\nsolve its problem?','2  FIND THE SIGNAL\nvisible, simple,\ngeometric','3  MAP IT\n"my solution space is ...\neach solution is a ..."','4  CODE EARLY\nthe code does not lie','5  BENCHMARK\nstandard functions,\n30 runs, fair rivals','6  NAME AND SHARE\nridicule -> opposition\n-> acceptance']
cols=[BLUE,PURPLE,GREEN,ORANGE,RED,GOLD]
for k,(t,c) in enumerate(zip(st,cols)):
    a=math.radians(90-60*k); x,y=4.2*math.cos(a),4.2*math.sin(a)
    ax.add_patch(FancyBboxPatch((x-1.75,y-0.95),3.5,1.9,boxstyle='round,pad=0.12',fc='white',ec=c,lw=2.6)); ax.text(x,y,t,ha='center',va='center',fontsize=9.5,fontweight='bold')
    a2=math.radians(90-60*(k+1)); x2,y2=4.2*math.cos(a2),4.2*math.sin(a2)
    ax.annotate('',xy=(0.62*x2+0.38*x,0.62*y2+0.38*y),xytext=(0.38*x2+0.62*x,0.38*y2+0.62*y),arrowprops=dict(arrowstyle='-|>',lw=2.6,color=GREY,connectionstyle='arc3,rad=-0.25'))
ax.text(0,0,'Go round this loop once\nand you will never look\nat nature the same way',ha='center',va='center',fontsize=12,fontweight='bold',color=BLUE)
save('fig9_16_loop')
# ---------- 9-8 population snapshots on 2-D Rastrigin
b=Bench('Rastrigin',2,shift=False); sn=[]; ka(b,5,M=12,p1=0.25,p2=0.25,Smax=6,budget=520,lo=b.lo,hi=b.hi,snaps=sn)
X,Y=np.meshgrid(np.linspace(-5.12,5.12,300),np.linspace(-5.12,5.12,300)); Zr=20+X**2-10*np.cos(2*np.pi*X)+Y**2-10*np.cos(2*np.pi*Y)
picks=[0,2,len(sn)-1]; fig,axs=plt.subplots(1,3,figsize=(15,5.2))
for ax,k in zip(axs,picks):
    P,Zs,lu,un,re=sn[k]; ax.contourf(X,Y,Zr,levels=30,cmap='Blues_r',alpha=0.8)
    for idx,c,s,lab in [(re,'#7FA8E0',90,'rest'),(un,RED,90,'unlucky'),(lu,GOLD,230,'lucky')]: ax.scatter([P[i][0] for i in idx],[P[i][1] for i in idx],s=s,color=c,edgecolor='black',zorder=5,label=lab)
    ax.scatter([0],[0],s=200,marker='P',color='black',zorder=6); ax.set_title(f'iteration {k}: best f = {min(Zs):.3f}',fontsize=12,fontweight='bold'); ax.set_aspect('equal'); ax.set_xlabel('x1')
axs[0].set_ylabel('x2'); axs[0].legend(fontsize=9,loc='lower left'); save('fig9_8_snapshots'); print('snaps',len(sn),[round(min(s[1]),4) for s in sn][:12])

# note: Figure 9-7 (KASA) and Figure 9-14 (loop) final versions are produced by ch09_figure_kasa_loop.py and ch09_figure_loop.py

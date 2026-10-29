import os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np, json
plt.rcParams.update({'font.size':12,'axes.linewidth':1.8,'lines.linewidth':2.5,'font.family':'DejaVu Sans','savefig.facecolor':'white','font.weight':'bold','axes.labelweight':'bold'})
BLUE='#0B3D91'; ORANGE='#E8600A'; GREEN='#118C4F'; RED='#C8102E'; GREY='#666666'; PURPLE='#6A1B9A'; GOLD='#D4A017'
AC={'SA':BLUE,'GA':ORANGE,'GASA':PURPLE,'KA':GOLD,'KASA':GREEN}; ALG=['SA','GA','GASA','KA','KASA']
def save(n): plt.tight_layout(); plt.savefig(f'fig/{n}.png',dpi=300); plt.close()
c8=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','ch08_GA','python','final.json'))); kd=json.load(open('final_disc.json')); bf=json.load(open('bench_final.json')); l9=json.load(open('l9.json'))
OPT={'SM':53,'TSP':312,'VRP':425,'FCTP':2200}
def disc(p,B,a): return c8[f'RK_{p}_{B}_{a}']['res'] if a in ('SA','GA','GASA') else kd[f'{p}_{B}_{a}']['res']
def clean(v): return [0.0 if x<1e-8 else x for x in v]
# ---- 9-10 L9 main effects
LEV={'M':[10,20,30],'p1':[0.1,0.2,0.4],'p2':[0.1,0.3,0.5],'S':[2,4,8]}; lab={'M':'population M','p1':'lucky share p1','p2':'unlucky share p2','S':'swirl rounds Smax'}
fig,axs=plt.subplots(1,4,figsize=(15,4.2))
for ax,f in zip(axs,['M','p1','p2','S']):
    for key,col,mk in [('TSP_2000',BLUE,'o'),('FCTP_2000',GREEN,'s')]:
        me=l9[key]['me'][f]; ax.plot([str(v) for v in LEV[f]],me,marker=mk,ms=10,color=col,label=key.replace('_',' , budget '))
        for i,v in enumerate(me): ax.text(i,v+0.07,f'{v:.2f}',ha='center',fontsize=10,fontweight='bold',color=col,bbox=dict(fc='white',ec='none',pad=0.1))
    ax.set_title(lab[f],fontsize=12,fontweight='bold'); ax.set_ylabel('mean RPD (%)'); ax.grid(alpha=0.3); ax.set_ylim(-0.15,2.3)
axs[0].legend(fontsize=9,loc='upper right'); save('fig9_10_l9')
# ---- 9-11 box plots discrete
fig,axs=plt.subplots(2,4,figsize=(16,7.6))
for r,B in enumerate((300,2000)):
    for c,p in enumerate(['SM','TSP','VRP','FCTP']):
        ax=axs[r][c]; data=[[(v-OPT[p])/OPT[p]*100 for v in disc(p,B,a)] for a in ALG]
        bp=ax.boxplot(data,labels=ALG,patch_artist=True,widths=0.55)
        for patch,a in zip(bp['boxes'],ALG): patch.set(facecolor=AC[a],alpha=0.55)
        for i,d in enumerate(data): ax.scatter(np.random.RandomState(i).normal(i+1,0.05,len(d)),d,s=12,color='black',alpha=0.55,zorder=3)
        ax.set_title(f'{p}, budget {B}',fontsize=12,fontweight='bold'); ax.grid(axis='y',alpha=0.3); ax.tick_params(axis='x',labelsize=10)
        if c==0: ax.set_ylabel('RPD (%) over 30 runs')
save('fig9_11_box')
# ---- 9-12 convergence FCTP 2000 and SM 300
fig,axs=plt.subplots(1,2,figsize=(14,4.6))
for ax,(p,B) in zip(axs,[('FCTP',2000),('SM',300)]):
    for a in ALG:
        h=c8[f'RK_{p}_{B}_{a}']['hist'] if a in ('SA','GA','GASA') else kd[f'{p}_{B}_{a}']['hist']
        ax.plot(range(1,len(h)+1),h,color=AC[a],lw=2.8 if a.startswith('KA') else 2,label=a)
    ax.axhline(OPT[p],color=GREY,ls='--',lw=1.8); ax.set_xscale('log'); ax.set_ylim(*( (2100,4000) if p=='FCTP' else (45,110))); ax.set_xlabel('evaluations (log scale)'); ax.set_ylabel('best Z so far (run 1)'); ax.set_title(f'{p}, budget {B}'+(' (infeasible start = 10000, off the chart)' if p=='FCTP' else ''),fontsize=11,fontweight='bold'); ax.grid(alpha=0.3); ax.legend(fontsize=10)
save('fig9_12_convergence')
# ---- 9-13 benchmark bars (log scale)
F=['Sphere','Rosenbrock','Rastrigin','Ackley','Griewank']
fig,axs=plt.subplots(1,2,figsize=(16,5.2))
for ax,D in zip(axs,(2,5)):
    w=0.16
    for k,a in enumerate(ALG):
        vals=[max(np.mean(clean(bf[f'{f}_D{D}'][a])),1e-9) for f in F]; xs=np.arange(5)+(k-2)*w
        ax.bar(xs,vals,width=w,color=AC[a],edgecolor='black',lw=1,label=a)
    ax.set_yscale('log'); ax.set_ylim(5e-10,200); ax.set_xticks(range(5)); ax.set_xticklabels(F,fontsize=11); ax.grid(axis='y',alpha=0.3)
    ax.set_ylabel('mean error over 30 runs (log)'); ax.set_title(f'D = {D}, budget {3000 if D==2 else 10000} evaluations (errors < 1e-8 shown at the floor)',fontsize=11,fontweight='bold')
axs[0].legend(fontsize=10,ncol=5,loc='upper left'); save('fig9_13_bench')
# ---- 9-15 scoreboard
rows=[]; names=[]
for p in ['SM','TSP','VRP','FCTP']:
    for B in (300,2000): rows.append([float(np.mean(disc(p,B,a))) for a in ALG]); names.append(f'{p}, budget {B}')
for D in (2,5):
    for f in F: rows.append([float(np.mean(clean(bf[f'{f}_D{D}'][a]))) for a in ALG]); names.append(f'{f}, D = {D}')
R=np.array(rows); rank=np.zeros_like(R)
for i in range(len(R)):
    for j in range(5): rank[i,j]=1+sum(1 for k in range(5) if R[i,k]<R[i,j]-1e-9*max(1,abs(R[i,j])))
fig,ax=plt.subplots(figsize=(11,10)); cmap=plt.get_cmap('RdYlGn_r'); ax.imshow(rank,cmap=cmap,vmin=1,vmax=5,aspect='auto')
for i in range(len(R)):
    for j in range(5):
        v=R[i,j]; t=(f'{v:.1f}' if v>=100 else f'{v:.2f}') if i<8 else ('0' if v==0 else f'{v:.1e}')
        ax.text(j,i,t+(' *' if rank[i,j]==1 else ''),ha='center',va='center',fontsize=10,fontweight='bold')
ax.set_xticks(range(5)); ax.set_xticklabels(ALG,fontsize=12); ax.set_yticks(range(len(names))); ax.set_yticklabels(names,fontsize=10.5)
ax.set_title('Scoreboard: mean result of 30 runs (green = rank 1, * = best or tied best)',fontsize=12,fontweight='bold'); save('fig9_15_scoreboard')
best=[[ALG[j] for j in range(5) if rank[i,j]==1] for i in range(len(R))]
json.dump({'names':names,'means':rows,'best':best},open('scoreboard.json','w'))
for n,b in zip(names,best): print(n,b)

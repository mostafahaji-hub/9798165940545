"""Chapter 9 - Keshtel Algorithm (textbook redesign) and the KASA hybrid.
Continuous vectors in [lo,hi]^n; discrete problems through the random keys of Chapter 8 (prob.decode), with a 'lake memory'
that never re-evaluates a decoded solution that has already been 'chewed'."""
import numpy as np, random, math, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
for p in [('..','..','common'),('..','..','ch07_SA','python'),('..','..','ch08_GA','python')]: sys.path.append(os.path.join(HERE,*p))
from data_reference import *
from ch07_sa import SM, TSP, VRP, FCTP, split_cost, fctp_table, sa
from ch08_ga import RK_SM, RK_TSP, RK_VRP, RK_FCTP, ga, fitness_min, roulette, crossover, mutate
def manhattan(a,b): return sum(abs(x-y) for x,y in zip(a,b))
def clip(v,lo,hi): return [min(hi,max(lo,x)) for x in v]
class Budget(Exception): pass
class Bench:
    BOX={'Sphere':(-100,100),'Rosenbrock':(-5,10),'Rastrigin':(-5.12,5.12),'Ackley':(-32.768,32.768),'Griewank':(-600,600)}
    def __init__(s,name,D=5,shift=True):
        s.name=name; s.n=D; s.opt=0.0; s.lo,s.hi=s.BOX[name]
        rs=np.random.RandomState(7+D); s.o=rs.uniform(0.2,0.6,D)*(s.hi-s.lo)/2*rs.choice([-1,1],D) if shift else np.zeros(D)
        if name=='Rosenbrock': s.o=s.o*0
    def f(s,x):
        x=np.array(x,float)-s.o; D=len(x)
        if s.name=='Sphere': return float(np.sum(x**2))
        if s.name=='Rosenbrock': return float(np.sum(100*(x[1:]-x[:-1]**2)**2+(1-x[:-1])**2))
        if s.name=='Rastrigin': return float(10*D+np.sum(x**2-10*np.cos(2*np.pi*x)))
        if s.name=='Ackley': return float(-20*np.exp(-0.2*np.sqrt(np.sum(x**2)/D))-np.exp(np.sum(np.cos(2*np.pi*x))/D)+20+np.e)
        return float(1+np.sum(x**2)/4000-np.prod(np.cos(x/np.sqrt(np.arange(1,D+1)))))
    def init(s,rng): return [rng.uniform(s.lo,s.hi) for _ in range(s.n)]
    def nb(s,x,rng):
        y=list(x); i=rng.randrange(s.n); y[i]=min(s.hi,max(s.lo,y[i]+rng.gauss(0,0.1*(s.hi-s.lo)))); return y
def ka(prob,seed,M=20,p1=0.2,p2=0.3,Smax=4,budget=2000,lo=0.0,hi=1.0,sa_budget=0,memory=True,swirl='mixed',capmul=10,log=None,snaps=None):
    rng=random.Random(seed); n=prob.n
    N1=round(p1*M); N2=round(p2*M)
    st={'e':0,'b':math.inf,'x':None}; hist=[]; cache={}; calls=[0]
    disc=memory and hasattr(prob,'decode') and not isinstance(prob,Bench)
    def ev(x):
        calls[0]+=1
        if st['e']>=budget or calls[0]>8*budget: raise Budget
        if disc:
            d=prob.decode(x); key=d if isinstance(d,int) else tuple(d)
            if key in cache: z=cache[key]
            else: z=prob.f(x); cache[key]=z; st['e']+=1; hist.append(min(st['b'],z))
        else: z=prob.f(x); st['e']+=1; hist.append(min(st['b'],z))
        if z<st['b']: st['b']=z; st['x']=list(x)
        return z
    P=[]; Z=[]
    try:
        for _ in range(M): x=[rng.uniform(lo,hi) for _ in range(n)]; P.append(x); Z.append(ev(x))
        while True:
            order=sorted(range(M),key=lambda i:Z[i]); lucky=order[:N1]; unlucky=order[M-N2:] if N2>0 else []; rest=order[N1:M-N2]
            if snaps is not None: snaps.append(([list(x) for x in P],list(Z),list(lucky),list(unlucky),list(rest)))
            for li in lucky:                       # ---- Phase 1: attraction and swirling (intensification)
                L=P[li]; fL=Z[li]
                near=lambda pt: P[min((i for i in range(M) if i!=li),key=lambda i:manhattan(P[i],pt))]
                A=near(L); moves=0; cap=capmul*Smax
                while moves<cap:
                    r=[l-a for l,a in zip(L,A)]
                    if max(abs(v) for v in r)<1e-12: r=[rng.uniform(-0.01,0.01)*(hi-lo) for _ in range(n)]
                    O=clip([l+v for l,v in zip(L,r)],lo,hi); fO=ev(O); moves+=1          # diagnostic question: slope or pit?
                    if log is not None: log.append(('O',list(O),fO))
                    if fO<fL: L,fL=O,fO; P[li]=L; Z[li]=fL; A=near(L); continue         # slope: the circle moves
                    moved=False
                    for s in range(1,Smax+1):                                            # pit: bisection rounds
                        rho=0.5**s; c=[[l+rho*v for l,v in zip(L,r)],[l-rho*v for l,v in zip(L,r)]]
                        if n>1 and swirl in ('mixed','random'):
                            u=[rng.gauss(0,1) for _ in range(n)]; nu=math.sqrt(sum(t*t for t in u)) or 1; rad=math.sqrt(sum(v*v for v in r))
                            c.append([l+rho*rad*t/nu for l,t in zip(L,u)])
                        if n>1 and swirl in ('mixed','coord'):
                            j=rng.randrange(n); cc=list(L); cc[j]+=rng.choice((-1,1))*rho*sum(abs(v) for v in r); c.append(cc)
                        for cand in c:
                            cand=clip(cand,lo,hi); fc=ev(cand); moves+=1
                            if log is not None: log.append((s,list(cand),fc))
                            if fc<fL: L,fL=cand,fc; P[li]=L; Z[li]=fL; A=near(L); moved=True; break
                            if moves>=cap: break
                        if moved or moves>=cap: break
                    if not moved: break                                                  # food consumed
                if sa_budget>0:                                                          # KASA: SA polishes the lucky Keshtel
                    L,fL=short_sa(prob,L,fL,rng,sa_budget,ev,lo,hi); P[li]=L; Z[li]=fL
            for wi in unlucky:                     # ---- Phase 2: the unlucky fly away, new Keshtels land (diversification)
                x=[rng.uniform(lo,hi) for _ in range(n)]; P[wi]=x; Z[wi]=ev(x)
            for ri in rest:                        # ---- Phase 3: the rest hustle toward empty water between two others
                g,h=rng.sample([i for i in range(M) if i!=ri],2); lam=rng.random()
                x=clip([a+lam*((b+c)/2-a) for a,b,c in zip(P[ri],P[g],P[h])],lo,hi); P[ri]=x; Z[ri]=ev(x)
    except Budget: pass
    return st['b'],st['x'],hist
def short_sa(prob,x,fx,rng,budget,ev,lo,hi):
    best=list(x); fb=fx; cur=list(x); fc=fx; T=0.05*max(abs(fx),1.0)
    for _ in range(budget):
        y=list(cur); i=rng.randrange(len(y))
        if rng.random()<0.5: y[i]=rng.uniform(lo,hi)
        elif isinstance(prob,Bench): y[i]=min(hi,max(lo,y[i]+rng.gauss(0,0.05*(hi-lo))))
        else: j=rng.randrange(len(y)); y[i],y[j]=y[j],y[i]
        fy=ev(y); d=fy-fc
        if d<=0 or rng.random()<math.exp(-d/max(T,1e-12)): cur,fc=y,fy
        if fc<fb: best,fb=list(cur),fc
        T*=0.85
    return best,fb
def sa_cont(prob,seed,p0=0.8,alpha=0.95,L=20,budget=3000): return sa(prob,seed,p0=p0,alpha=alpha,L=L,budget=budget)[0]
def ga_cont(prob,seed,pop=20,pc=0.9,pm=0.2,budget=3000,gasa=None):
    rng=random.Random(seed); n=prob.n; lo,hi=prob.lo,prob.hi
    P=[[rng.uniform(lo,hi) for _ in range(n)] for _ in range(pop)]; Z=[prob.f(c) for c in P]; ev=[pop]; best=[min(Z)]
    def mut(c):
        c=list(c); i=rng.randrange(n); c[i]=rng.uniform(lo,hi) if rng.random()<0.5 else min(hi,max(lo,c[i]+rng.gauss(0,0.1*(hi-lo)))); return c
    def f(c):
        z=prob.f(c); ev[0]+=1; best[0]=min(best[0],z); return z
    while ev[0]<budget:
        fit=fitness_min(Z); idx=np.argsort(Z); NP=[P[i] for i in idx[:2]]; NZ=[Z[i] for i in idx[:2]]
        while len(NP)<pop and ev[0]<budget:
            a=roulette(fit,rng); b=roulette(fit,rng)
            c1,c2=crossover(P[a],P[b],rng,'uniform') if rng.random()<pc else (list(P[a]),list(P[b]))
            for c in (c1,c2):
                if len(NP)>=pop or ev[0]>=budget: break
                if rng.random()<pm:
                    if gasa:
                        x=list(c); fx=f(x); bx,fb=x,fx; T=0.05*max(abs(fx),1)
                        for k in range(gasa):
                            if ev[0]>=budget: break
                            y=mut(x); fy=f(y); d=fy-fx
                            if d<=0 or rng.random()<math.exp(-d/max(T,1e-12)): x,fx=y,fy
                            if fx<fb: bx,fb=list(x),fx
                            T*=0.85
                        c=bx
                    else: c=mut(c)
                NP.append(c); NZ.append(f(c))
        P,Z=NP,NZ
    return best[0]

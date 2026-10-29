"""Chapter 8 - generational GA with random keys, roulette selection, uniform/two-point crossover, reset mutation, elitism;
GASA hybrid (short SA as mutation). Run: python ch08_ga.py"""
import os
import numpy as np, random, math, itertools, sys, os, json, time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'common')); from data_reference import *
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ch07_SA', 'python')); from ch07_sa import SM, TSP, VRP, FCTP, split_cost, fctp_table, sa
# ---------- random-key decoders ----------
def rk_to_perm(keys): return list(np.argsort(keys, kind='stable'))   # rank: smallest key first
class RK_SM(SM):
    n=6
    def decode(s,k): return rk_to_perm(k)
    def f(s,k): return super().f(s.decode(k))
class RK_TSP(TSP):
    n=8
    def decode(s,k): return [i+1 for i in rk_to_perm(k)]
    def f(s,k): return super().f(s.decode(k))
class RK_VRP(VRP):
    n=8
    def decode(s,k): return [i+1 for i in rk_to_perm(k)]
    def f(s,k): return split_cost(s.decode(k))
class RK_FCTP(FCTP):
    n=12; BIGM=10000
    def decode(s,k): return sum((1<<b) for b in range(12) if k[b]>=0.5)
    def f(s,k):
        v=s.T[s.decode(k)]; return s.BIGM if v is None else v
# ---------- GA ----------
def fitness_min(Z):  # for minimisation: larger is better; use (worst - Z + 1)
    Z=np.array(Z,float); return Z.max()-Z+1.0
def roulette(fit,rng):
    cum=np.cumsum(fit)/fit.sum(); u=rng.random(); return int(np.searchsorted(cum,u))
def crossover(p1,p2,rng,kind='uniform'):
    n=len(p1)
    if kind=='uniform':
        mask=[rng.random()<0.5 for _ in range(n)]
        c1=[p1[i] if mask[i] else p2[i] for i in range(n)]; c2=[p2[i] if mask[i] else p1[i] for i in range(n)]
    else:  # two-point
        a,b=sorted(rng.sample(range(1,n),2)); c1=p1[:a]+p2[a:b]+p1[b:]; c2=p2[:a]+p1[a:b]+p2[b:]
    return c1,c2
def mutate(p,rng,kind='reset'):
    c=list(p); i=rng.randrange(len(c))
    if kind=='reset': c[i]=rng.random()
    else: j=rng.randrange(len(c)); c[i],c[j]=c[j],c[i]
    return c
def ga(prob,seed,pop=20,pc=0.8,pm=0.1,budget=300,elite=2,xover='uniform',gasa=None,trace=False):
    """gasa: None or number of SA evaluations used as mutation (hybrid)."""
    rng=random.Random(seed); n=prob.n
    P=[[rng.random() for _ in range(n)] for _ in range(pop)]; Z=[prob.f(c) for c in P]; evals=pop
    best=min(Z); bx=P[Z.index(best)]; hist=[best]; gen=0
    while evals<budget:
        gen+=1; fit=fitness_min(Z); idx=np.argsort(Z); newP=[P[i] for i in idx[:elite]]; newZ=[Z[i] for i in idx[:elite]]
        while len(newP)<pop and evals<budget:
            a=roulette(fit,rng); b=roulette(fit,rng)
            if rng.random()<pc: c1,c2=crossover(P[a],P[b],rng,xover)
            else: c1,c2=list(P[a]),list(P[b])
            for c in (c1,c2):
                if len(newP)>=pop or evals>=budget: break
                if rng.random()<pm:
                    if gasa: c,used=sa_mutation(prob,c,rng,gasa); evals+=used
                    else: c=mutate(c,rng)
                z=prob.f(c); evals+=1; newP.append(c); newZ.append(z)
                if z<best: best=z; bx=c
                hist.append(best)
        P,Z=newP,newZ
    return best,bx,hist,gen
def sa_mutation(prob,c,rng,budget):
    """short SA on random keys starting from c; returns improved (or same) chromosome and evaluations used."""
    x=list(c); fx=prob.f(x); best=fx; bx=x; T=0.1*fx if fx>0 else 1.0; used=1
    for k in range(budget):
        y=mutate(x,rng,'swap' if rng.random()<0.5 else 'reset'); fy=prob.f(y); used+=1; d=fy-fx
        if d<=0 or rng.random()<math.exp(-d/max(T,1e-9)): x,fx=y,fy
        if fx<best: best=fx; bx=x
        T*=0.8
    return bx,used
if __name__=='__main__':
    for P in (RK_SM(),RK_TSP(),RK_VRP(),RK_FCTP()):
        name=P.__class__.__name__
        for budget in (300,2000):
            res=[ga(P,s,budget=budget)[0] for s in range(1,31)]
            print(name,budget,"GA best/mean/worst",min(res),round(np.mean(res),2),max(res),"hits",sum(r==P.opt for r in res))

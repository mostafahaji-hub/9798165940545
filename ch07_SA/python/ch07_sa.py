"""Chapter 7 - Simulated Annealing on the four reference problems (single machine, TSP, VRP via giant tour + split, FCTP via open/closed pattern table).
Run: python ch07_sa.py   (30 runs per problem, budget 2000)"""
import os
import numpy as np, random, math, itertools, sys, os, json, time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'common')); from data_reference import *
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ch04_scheduling_sequencing', 'python')); from ch04_exact import et_eval, tour_length
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ch03_transportation_fctp', 'python')); from ch03_transportation import transport
# ---------- problem definitions: (random initial solution, neighbor, objective, optimum) ----------
class SM:  # single machine
    opt=53; n=6
    def init(s,rng): p=list(range(6)); rng.shuffle(p); return p
    def nb(s,x,rng):
        y=list(x)
        if rng.random()<0.5: i,j=rng.sample(range(6),2); y[i],y[j]=y[j],y[i]
        else: i,j=rng.sample(range(6),2); e=y.pop(i); y.insert(j,e)
        return y
    def f(s,x): return et_eval(x)['Z']
class TSP:
    opt=312; n=8
    def init(s,rng): p=list(range(1,9)); rng.shuffle(p); return p
    def nb(s,x,rng):
        y=list(x); i,j=sorted(rng.sample(range(8),2))
        if rng.random()<0.7: y[i:j+1]=reversed(y[i:j+1])      # 2-opt
        else: e=y.pop(i); y.insert(j,e)                       # or-opt (1)
        return y
    def f(s,x): return tour_length(x)
q=VRP_DEMAND; D=TSP_DIST
def split_cost(giant,K=3,Q=45):
    n=len(giant); best=10**9
    for k in range(1,K+1):
        for cuts in itertools.combinations(range(1,n),k-1):
            b=[0]+list(cuts)+[n]; ok=True; tot=0
            for i in range(k):
                r=giant[b[i]:b[i+1]]
                if sum(q[c] for c in r)>Q: ok=False; break
                tot+=D[0,r[0]]+sum(D[r[t],r[t+1]] for t in range(len(r)-1))+D[r[-1],0]
            if ok and tot<best: best=tot
    return best if best<10**9 else 2000+sum(q)   # penalty if infeasible
class VRP(TSP):
    opt=425
    def f(s,x): return split_cost(x)
# FCTP: precompute pattern costs
PAT=None
def fctp_table():
    global PAT
    if PAT is not None: return PAT
    cache=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fctp_patterns.json')
    if os.path.exists(cache): PAT={int(k):v for k,v in json.load(open(cache)).items()}; return PAT
    PAT={}
    for pat in range(4096):
        y=np.array([(pat>>b)&1 for b in range(12)]).reshape(3,4); z,x=transport(COST,SUPPLY,DEMAND,y)
        PAT[pat]=None if z is None else int(z+FIXED[y==1].sum())
    json.dump(PAT,open(cache,'w')); return PAT
class FCTP:
    opt=2200; n=12
    def __init__(s): s.T=fctp_table()
    def init(s,rng):
        while True:
            pat=rng.randrange(4096)
            if s.T[pat] is not None: return pat
    def nb(s,x,rng):
        for _ in range(50):
            b=rng.randrange(12); y=x^(1<<b)
            if s.T[y] is not None: return y
        return x
    def f(s,x): return s.T[x]
# ---------- SA ----------
def initial_temperature(prob,rng,p0=0.8,samples=100):
    x=prob.init(rng); fx=prob.f(x); deltas=[]
    for _ in range(samples):
        y=prob.nb(x,rng); fy=prob.f(y)
        if fy>fx: deltas.append(fy-fx)
        x,fx=y,fy
    dbar=np.mean(deltas) if deltas else 1.0
    return -dbar/math.log(p0)
def sa(prob,seed,p0=0.8,alpha=0.9,L=10,budget=2000,Tf_ratio=0.01,trace=False):
    rng=random.Random(seed); T0=initial_temperature(prob,rng,p0); T=T0; Tf=T0*Tf_ratio
    x=prob.init(rng); fx=prob.f(x); best=fx; bx=list(x) if not isinstance(x,int) else x; evals=0; hist=[best]; acc=0; tried=0
    while evals<budget:
        for _ in range(L):
            y=prob.nb(x,rng); fy=prob.f(y); evals+=1; d=fy-fx; tried+=1
            if d<=0 or rng.random()<math.exp(-d/T): x,fx=y,fy; acc+=1
            if fx<best: best=fx; bx=x
            hist.append(best)
            if evals>=budget: break
        T=max(T*alpha,Tf)
    return best,bx,hist,T0
if __name__=='__main__':
    for P in (SM(),TSP(),VRP(),FCTP()):
        t=time.time(); res=[sa(P,s)[0] for s in range(1,31)]
        print(P.__class__.__name__,"30 runs best/mean/worst",min(res),round(np.mean(res),2),max(res),"hits",sum(r==P.opt for r in res),"time",round(time.time()-t,1))

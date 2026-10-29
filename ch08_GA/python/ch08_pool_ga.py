import os, json, math, random
import numpy as np
from ch08_ga import *
def mut_ops(p,rng):
    c=list(p); n=len(c); k=rng.randrange(4)
    if k==0: i=rng.randrange(n-1); c[i],c[i+1]=c[i+1],c[i]
    elif k==1: i,j=rng.sample(range(n),2); c[i],c[j]=c[j],c[i]
    elif k==2: i,j=sorted(rng.sample(range(n),2)); c[i:j+1]=reversed(c[i:j+1])
    else: i,j=sorted(rng.sample(range(1,n),2)); seg=c[i:j+1]; c=seg+c[:i]+c[j+1:]
    return c
def ga_pool(prob,seed,pop=20,pc=0.8,pm=0.3,budget=2000):
    rng=random.Random(seed); n=prob.n
    P=[[rng.random() for _ in range(n)] for _ in range(pop)]; Z=[prob.f(c) for c in P]; evals=pop; best=min(Z); hist=[best]
    NC=2*round(pc*pop/2); NM=int(pm*pop)
    while evals<budget:
        fit=fitness_min(Z); kids=[]
        for k in range(0,NC,2):
            a=roulette(fit,rng); b=roulette(fit,rng); kind=rng.choice(['uniform','two'])
            c1,c2=crossover(P[a],P[b],rng,kind); kids+=[c1,c2]
        for k in range(NM): kids.append(mut_ops(P[rng.randrange(pop)],rng))
        kz=[]
        for c in kids:
            if evals>=budget: break
            z=prob.f(c); evals+=1; kz.append(z)
            if z<best: best=z
            hist.append(best)
        pool=list(zip(P+kids[:len(kz)],Z+kz)); pool.sort(key=lambda t:t[1]); P=[p for p,_ in pool[:pop]]; Z=[z for _,z in pool[:pop]]
    return best,hist
import numpy as np, json
out={}
for P in (RK_SM(),RK_TSP(),RK_VRP(),RK_FCTP()):
    name=P.__class__.__name__
    for budget in (300,2000):
        res=[ga_pool(P,s,budget=budget)[0] for s in range(1,31)]
        out[f"{name}_{budget}"]=dict(best=int(min(res)),mean=float(np.mean(res)),worst=int(max(res)),std=float(np.std(res,ddof=1)),meanRPD=float(np.mean([(r-P.opt)/P.opt*100 for r in res])),hits=int(sum(r==P.opt for r in res)))
        o=out[f"{name}_{budget}"]; print(name,budget,"POOL best",o['best'],"mean",round(o['mean'],1),"worst",o['worst'],"std",round(o['std'],1),"RPD",round(o['meanRPD'],2),"hits",o['hits'])
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pool.json'),'w'))

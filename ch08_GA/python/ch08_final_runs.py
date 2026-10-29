import os, json, math, random
import numpy as np
from ch08_ga import *
cfg={300:dict(RK_SM=(40,0.95,0.15),RK_TSP=(40,0.95,0.15),RK_VRP=(40,0.95,0.15),RK_FCTP=(20,0.6,0.3)),2000:dict(RK_SM=(20,0.95,0.15),RK_TSP=(20,0.95,0.15),RK_VRP=(20,0.95,0.15),RK_FCTP=(40,0.8,0.3))}
sacfg=dict(RK_SM=(0.8,0.8,5),RK_TSP=(0.8,0.8,5),RK_VRP=(0.8,0.8,5),RK_FCTP=(0.5,0.9,20))
sacfg2000=dict(RK_SM=(0.8,0.9,10),RK_TSP=(0.8,0.9,10),RK_VRP=(0.8,0.9,10),RK_FCTP=(0.5,0.9,20))
base={'RK_SM':SM(),'RK_TSP':TSP(),'RK_VRP':VRP(),'RK_FCTP':FCTP()}
out={}
def stats(res,opt):
    rpd=[(r-opt)/opt*100 for r in res]; return dict(best=int(min(res)),mean=float(np.mean(res)),worst=int(max(res)),std=float(np.std(res,ddof=1)),meanRPD=float(np.mean(rpd)),hits=int(sum(r==opt for r in res)),res=[int(r) for r in res])
for P in (RK_SM(),RK_TSP(),RK_VRP(),RK_FCTP()):
    name=P.__class__.__name__
    for budget in (300,2000):
        pop,pc,pm=cfg[budget][name]
        g=[ga(P,s,pop=pop,pc=pc,pm=pm,budget=budget) for s in range(1,31)]
        out[f"{name}_{budget}_GA"]=stats([x[0] for x in g],P.opt); out[f"{name}_{budget}_GA"]['hist']=[int(v) for v in g[0][2]]; out[f"{name}_{budget}_GA"]['gens']=float(np.mean([x[3] for x in g]))
        h=[ga(P,s,pop=pop,pc=pc,pm=pm,budget=budget,gasa=10) for s in range(1,31)]
        out[f"{name}_{budget}_GASA"]=stats([x[0] for x in h],P.opt); out[f"{name}_{budget}_GASA"]['hist']=[int(v) for v in h[0][2]]
        p0,a,L=(sacfg if budget==300 else sacfg2000)[name]
        sres=[sa(base[name],s,p0=p0,alpha=a,L=L,budget=budget) for s in range(1,31)]
        out[f"{name}_{budget}_SA"]=stats([x[0] for x in sres],P.opt); out[f"{name}_{budget}_SA"]['hist']=[int(v) for v in sres[0][2]]
        for alg in ('SA','GA','GASA'):
            o=out[f"{name}_{budget}_{alg}"]; print(name,budget,alg,"best",o['best'],"mean",round(o['mean'],1),"worst",o['worst'],"std",round(o['std'],1),"RPD",round(o['meanRPD'],2),"hits",o['hits'])
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'final.json'),'w'))

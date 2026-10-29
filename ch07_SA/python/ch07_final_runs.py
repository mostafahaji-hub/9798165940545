import os, json, math, random
from ch07_sa import *
import numpy as np, json
cfg={'SM':(0.8,0.8,5),'TSP':(0.8,0.8,5),'VRP':(0.8,0.8,5),'FCTP':(0.5,0.9,20)}
out={}
for P in (SM(),TSP(),VRP(),FCTP()):
    name=P.__class__.__name__; p0,a,L=cfg[name]
    for budget in (300,2000):
        res=[]; hists=[]; T0s=[]
        for s in range(1,31):
            b,bx,h,T0=sa(P,s,p0=p0,alpha=a,L=L,budget=budget); res.append(b); hists.append(h); T0s.append(T0)
        rpd=[(r-P.opt)/P.opt*100 for r in res]
        out[f"{name}_{budget}"]=dict(best=int(min(res)),mean=float(np.mean(res)),worst=int(max(res)),std=float(np.std(res,ddof=1)),meanRPD=float(np.mean(rpd)),hits=int(sum(r==P.opt for r in res)),T0=float(np.mean(T0s)),res=[int(r) for r in res],hist=[int(v) for v in hists[0]])
        o=out[f"{name}_{budget}"]; print(name,budget,"best",o['best'],"mean",round(o['mean'],2),"worst",o['worst'],"std",round(o['std'],2),"meanRPD",round(o['meanRPD'],2),"hits",o['hits'],"T0",round(o['T0'],1))
# untuned comparison (worst FF config) for TSP at 300
P=TSP(); res=[sa(P,s,p0=0.95,alpha=0.98,L=20,budget=300)[0] for s in range(1,31)]; print("TSP untuned (0.95,0.98,20) mean",np.mean(res),"hits",sum(r==312 for r in res))
out['TSP_untuned']=[int(r) for r in res]
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'final.json'),'w'))

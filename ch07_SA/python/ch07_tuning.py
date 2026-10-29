import os, json, math, random
from ch07_sa import *
import numpy as np, itertools, json
LEV={'p0':[0.5,0.8,0.95],'alpha':[0.80,0.90,0.98],'L':[5,10,20]}
def run_cfg(P,p0,alpha,L,budget=300,runs=10,seed0=100):
    res=[sa(P,seed0+s,p0=p0,alpha=alpha,L=L,budget=budget)[0] for s in range(runs)]
    return np.mean([(r-P.opt)/P.opt*100 for r in res])
def full_factorial(P):
    rows=[]
    for p0 in LEV['p0']:
        for a in LEV['alpha']:
            for L in LEV['L']:
                rows.append((p0,a,L,round(run_cfg(P,p0,a,L),2)))
    return rows
L9=[(1,1,1),(1,2,2),(1,3,3),(2,1,2),(2,2,3),(2,3,1),(3,1,3),(3,2,1),(3,3,2)]
def taguchi(P):
    rows=[]
    for (i,j,k) in L9:
        p0,a,L=LEV['p0'][i-1],LEV['alpha'][j-1],LEV['L'][k-1]; res=[sa(P,100+s_,p0=p0,alpha=a,L=L,budget=300)[0] for s_ in range(10)]; rp=[(x-P.opt)/P.opt*100 for x in res]; r=float(np.mean(rp)); sn=-10*math.log10(max(np.mean([v*v for v in rp]),1e-9))  # standard smaller-the-better SN
        rows.append((i,j,k,p0,a,L,round(r,2),round(sn,2)))
    return rows
if __name__=='__main__':
    out={}
    for P in (TSP(),FCTP()):
        name=P.__class__.__name__; ff=full_factorial(P); tg=taguchi(P)
        out[name]={'ff':ff,'tg':tg}
        print(name,"FULL FACTORIAL (mean RPD of 10 runs, budget 300)"); [print('  ',r) for r in ff]
        best=min(ff,key=lambda r:r[3]); print("  best",best)
        # main effects
        for f_,idx in (('p0',0),('alpha',1),('L',2)):
            print("  main effect",f_,{lv:round(np.mean([r[3] for r in ff if r[idx]==lv]),2) for lv in LEV[f_]})
        print(name,"TAGUCHI L9"); [print('  ',r) for r in tg]
        for f_,idx in (('p0',0),('alpha',1),('L',2)):
            print("  Taguchi main effect (mean RPD)",f_,{lv:round(np.mean([r[6] for r in tg if r[idx]==lv]),2) for lv in (1,2,3)})
    json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tuning.json'),'w'))

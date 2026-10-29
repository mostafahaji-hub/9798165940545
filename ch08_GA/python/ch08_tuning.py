import os, json, math, random
import numpy as np
from ch08_ga import *
LEV={'pop':[10,20,40],'pc':[0.6,0.8,0.95],'pm':[0.05,0.15,0.3]}
L9=[(1,1,1),(1,2,2),(1,3,3),(2,1,2),(2,2,3),(2,3,1),(3,1,3),(3,2,1),(3,3,2)]
def run_cfg(P,pop,pc,pm,budget,runs=10,seed0=100,**kw):
    res=[ga(P,seed0+s,pop=pop,pc=pc,pm=pm,budget=budget,**kw)[0] for s in range(runs)]
    return float(np.mean([(r-P.opt)/P.opt*100 for r in res]))
out={}
for P in (RK_TSP(),RK_FCTP()):
    name=P.__class__.__name__
    for budget in (300,2000):
        rows=[]
        for (i,j,k) in L9:
            pop,pc,pm=LEV['pop'][i-1],LEV['pc'][j-1],LEV['pm'][k-1]; r=run_cfg(P,pop,pc,pm,budget); rows.append((i,j,k,pop,pc,pm,round(r,2),round(-10*math.log10(max(r,1e-3)**2),2)))
        out[f"{name}_{budget}"]=rows
        print(name,budget); [print('  ',r) for r in rows]
        for f_,idx in (('pop',0),('pc',1),('pm',2)):
            print("  main effect",f_,{lv:round(np.mean([r[6] for r in rows if r[idx]==lv]),2) for lv in (1,2,3)})
        # full factorial too (for the record)
        ff=[]
        for pop in LEV['pop']:
            for pc in LEV['pc']:
                for pm in LEV['pm']: ff.append((pop,pc,pm,round(run_cfg(P,pop,pc,pm,budget),2)))
        out[f"{name}_{budget}_ff"]=ff; print("  FF best",min(ff,key=lambda r:r[3]),"worst",max(ff,key=lambda r:r[3]))
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tuning.json'),'w'))

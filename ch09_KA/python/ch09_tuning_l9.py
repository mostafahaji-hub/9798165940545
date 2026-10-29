"""Chapter 9 experiment script (see Ch09 verification report). Results are written next to this file."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from ch09_ka import *
L9=[(1,1,1,1),(1,2,2,2),(1,3,3,3),(2,1,2,3),(2,2,3,1),(2,3,1,2),(3,1,3,2),(3,2,1,3),(3,3,2,1)]
LEV={'M':[10,20,30],'p1':[0.1,0.2,0.4],'p2':[0.1,0.3,0.5],'S':[2,4,8]}
import os
out=json.load(open('l9.json')) if os.path.exists('l9.json') else {}
for nm,P in [('TSP',RK_TSP()),('FCTP',RK_FCTP())]:
    for B in (300,2000):
        if f'{nm}_{B}' in out: continue
        rows=[]
        for (a,b,c,d) in L9:
            M,p1,p2,S=LEV['M'][a-1],LEV['p1'][b-1],LEV['p2'][c-1],LEV['S'][d-1]
            res=[ka(P,100+s,M=M,p1=p1,p2=p2,Smax=S,budget=B)[0] for s in range(10)]
            rpd=float(np.mean([(v-P.opt)/P.opt*100 for v in res])); rows.append([a,b,c,d,M,p1,p2,S,round(rpd,2),int(sum(v==P.opt for v in res))])
        me={f:[round(float(np.mean([r[8] for r in rows if r[k]==lv])),2) for lv in (1,2,3)] for k,f in enumerate(['M','p1','p2','S'])}
        best=[LEV[f][int(np.argmin(me[f]))] for f in ['M','p1','p2','S']]
        out[f'{nm}_{B}']={'rows':rows,'me':me,'best':best}; json.dump(out,open('l9.json','w')); print(nm,B,'ME',me,'best',best,'rowbest',min(rows,key=lambda r:r[8])[4:],flush=True)
json.dump(out,open('l9.json','w'))

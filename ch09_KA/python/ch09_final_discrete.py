"""Chapter 9 experiment script (see Ch09 verification report). Results are written next to this file."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from ch09_ka import *
CFG={300:(10,0.2,0.3,4),2000:(10,0.4,0.5,8)}; CFGF={300:(10,0.2,0.3,4),2000:(10,0.1,0.1,2)}
out=json.load(open('final_disc.json')) if os.path.exists('final_disc.json') else {}
def stats(res,opt):
    rpd=[(r-opt)/opt*100 for r in res]; return dict(best=int(min(res)),mean=float(np.mean(res)),worst=int(max(res)),std=float(np.std(res,ddof=1)),meanRPD=float(np.mean(rpd)),hits=int(sum(r==opt for r in res)),res=[int(r) for r in res])
for nm,P in [('SM',RK_SM()),('TSP',RK_TSP()),('VRP',RK_VRP()),('FCTP',RK_FCTP())]:
    for B in (300,2000):
        M,p1,p2,S=(CFGF if nm=='FCTP' else CFG)[B]
        for alg,sab in (('KA',0),('KASA',10)):
            key=f'{nm}_{B}_{alg}'
            if key in out: continue
            runs=[ka(P,s,M=M,p1=p1,p2=p2,Smax=S,budget=B,sa_budget=sab) for s in range(1,31)]
            o=stats([r[0] for r in runs],P.opt); o['hist']=[int(v) for v in runs[0][2]]; o['cfg']=[M,p1,p2,S]; out[key]=o
            json.dump(out,open('final_disc.json','w')); print(key,round(o['mean'],1),o['worst'],round(o['meanRPD'],2),o['hits'],flush=True)

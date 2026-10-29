"""Chapter 9 experiment script (see Ch09 verification report). Results are written next to this file."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from ch09_ka import *
out=json.load(open('bench_final.json')) if os.path.exists('bench_final.json') else {}
for D,B in [(2,3000),(5,10000)]:
    for nm in ['Sphere','Rosenbrock','Rastrigin','Ackley','Griewank']:
        key=f'{nm}_D{D}'
        if key in out: continue
        b=Bench(nm,D); row={}
        row['SA']=[sa_cont(b,s,budget=B) for s in range(1,31)]
        row['GA']=[ga_cont(b,s,budget=B) for s in range(1,31)]
        row['GASA']=[ga_cont(b,s,budget=B,gasa=10) for s in range(1,31)]
        row['KA']=[ka(b,s,M=10,p1=0.2,p2=0.3,Smax=8,budget=B,lo=b.lo,hi=b.hi)[0] for s in range(1,31)]
        row['KASA']=[ka(b,s,M=10,p1=0.2,p2=0.3,Smax=8,budget=B,lo=b.lo,hi=b.hi,sa_budget=10)[0] for s in range(1,31)]
        out[key]={k:[float(v) for v in vals] for k,vals in row.items()}; json.dump(out,open('bench_final.json','w'))
        print(key,{k:f"{np.mean(v):.3g}" for k,v in row.items()},flush=True)

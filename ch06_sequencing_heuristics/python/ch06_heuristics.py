"""Chapter 6 - sequencing heuristics: dispatching rules (SPT/EDD/WSPT/slack/d-beta/Moore-Hodgson/ATC), TSP constructive
(nearest neighbour, nearest/cheapest insertion, savings) and improvement (2-opt, Or-opt), VRP (Clarke-Wright with capacity,
sweep, giant-tour split, relocate/swap improvement). Reproduces all Chapter 6 numbers. Run: python ch06_heuristics.py"""
import numpy as np, itertools, math, sys
import os; sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common')); from data_reference import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ch04_scheduling_sequencing', 'python')); from ch04_exact import et_eval, tour_length, best_route, vrp_exact, tsp_brute
J=JOBS6; N=J['names']; n=6
Z=lambda s: et_eval(s)['Z']
name=lambda s:'-'.join(N[i] for i in s)
rules={}
rules['SPT']=sorted(range(n),key=lambda j:J['p'][j]); rules['LPT']=sorted(range(n),key=lambda j:-J['p'][j])
rules['EDD']=sorted(range(n),key=lambda j:J['d'][j]); rules['LDD']=sorted(range(n),key=lambda j:-J['d'][j])
rules['WSPT (p/beta)']=sorted(range(n),key=lambda j:J['p'][j]/J['beta'][j]); rules['d/beta']=sorted(range(n),key=lambda j:J['d'][j]/J['beta'][j])
rules['slack d-p']=sorted(range(n),key=lambda j:J['d'][j]-J['p'][j])
# Moore-Hodgson: minimize number of tardy jobs
def moore():
    order=sorted(range(n),key=lambda j:J['d'][j]); sched=[]; t=0
    for j in order:
        sched.append(j); t+=J['p'][j]
        if t>J['d'][j]:
            k=max(sched,key=lambda q:J['p'][q]); sched.remove(k); t-=J['p'][k]
    late=[j for j in range(n) if j not in sched]
    return sched+late, len(late)
mh,nl=moore(); rules['Moore-Hodgson']=mh
# ATC rule (K=2): dynamic
def atc(K=2.0):
    left=set(range(n)); t=0; seq=[]
    pbar=np.mean(J['p'])
    while left:
        def idx(j): return (J['beta'][j]/J['p'][j])*math.exp(-max(0,J['d'][j]-J['p'][j]-t)/(K*pbar))
        j=max(left,key=idx); seq.append(j); t+=J['p'][j]; left.remove(j)
    return seq
rules['ATC (K=2)']=atc()
for k,s in rules.items(): print(f"{k:16s} {name(s)}  Z={Z(s)}  RPD={(Z(s)-53)/53*100:.1f}%  ntardy={sum(1 for j in s if False)}")
print("Moore tardy count",nl, "tardy jobs opt?")
# count tardy for each
def ntardy(s):
    t=0;c=0
    for j in s: t+=J['p'][j]; c+= t>J['d'][j]
    return c
for k,s in rules.items(): print(k,'tardy',ntardy(s))
allp=list(itertools.permutations(range(n))); print("min tardy", min(ntardy(s) for s in allp))
# API local search from EDD and d/beta with swap (ch2 results): from EDD 83->71->60->53
# ------- TSP heuristics ---------
D=TSP_DIST; nn_=9
def tl(t): return tour_length(t)
def nearest_neighbour(start=0):
    left=set(range(1,nn_)); cur=0; tour=[]
    while left: j=min(left,key=lambda k:(D[cur,k],k)); tour.append(j); left.remove(j); cur=j
    return tour
def nearest_insertion():
    # start with nearest to depot
    tour=[min(range(1,nn_),key=lambda k:D[0,k])]; left=set(range(1,nn_))-set(tour); log=[]
    while left:
        # customer closest to any node of the tour (incl depot)
        k=min(left,key=lambda c:(min(D[c,v] for v in [0]+tour),c))
        # best insertion position in cycle 0-tour-0
        best=None
        cyc=[0]+tour+[0]
        for pos in range(1,len(cyc)):
            a,b=cyc[pos-1],cyc[pos]; delta=D[a,k]+D[k,b]-D[a,b]
            if best is None or delta<best[0]: best=(delta,pos)
        tour.insert(best[1]-1,k); left.remove(k); log.append((k,best[0],list(tour),tl(tour)))
    return tour,log
def cheapest_insertion():
    tour=[min(range(1,nn_),key=lambda k:D[0,k])]; left=set(range(1,nn_))-set(tour); log=[]
    while left:
        best=None; cyc=[0]+tour+[0]
        for k in left:
            for pos in range(1,len(cyc)):
                a,b=cyc[pos-1],cyc[pos]; delta=D[a,k]+D[k,b]-D[a,b]
                if best is None or (delta,k)<(best[0],best[1]): best=(delta,k,pos)
        tour.insert(best[2]-1,best[1]); left.remove(best[1]); log.append((best[1],best[0],list(tour),tl(tour)))
    return tour,log
def two_opt(tour):
    tour=list(tour); improved=True; log=[tl(tour)]
    while improved:
        improved=False; best=(0,None)
        cyc=[0]+tour+[0]
        for i in range(0,len(cyc)-2):
            for j in range(i+2,len(cyc)-1):
                a,b,c_,d=cyc[i],cyc[i+1],cyc[j],cyc[j+1]
                delta=D[a,c_]+D[b,d]-D[a,b]-D[c_,d]
                if delta<best[0]: best=(delta,(i,j))
        if best[1]:
            i,j=best[1]; cyc[i+1:j+1]=reversed(cyc[i+1:j+1]); tour=cyc[1:-1]; improved=True; log.append((best[0],list(tour),tl(tour)))
    return tour,log
def or_opt(tour):
    tour=list(tour); log=[tl(tour)]; improved=True
    while improved:
        improved=False; best=(0,None)
        for L in (1,2,3):
            for i in range(len(tour)-L+1):
                seg=tour[i:i+L]; rest=tour[:i]+tour[i+L:]
                for pos in range(len(rest)+1):
                    for s2 in (seg,seg[::-1]):
                        new=rest[:pos]+s2+rest[pos:]; delta=tl(new)-tl(tour)
                        if delta<best[0]: best=(delta,new)
        if best[1]: tour=best[1]; improved=True; log.append((best[0],list(tour),tl(tour)))
    return tour,log
nn=nearest_neighbour(); print("NN",nn,tl(nn))
ni,lg=nearest_insertion(); print("NI",ni,tl(ni)); [print('  ',l) for l in lg]
ci,lg=cheapest_insertion(); print("CI",ci,tl(ci)); [print('  ',l) for l in lg]
# savings for TSP (single vehicle, no capacity)
def savings_tsp():
    S=[(D[0,i]+D[0,j]-D[i,j],i,j) for i in range(1,nn_) for j in range(i+1,nn_)]; S.sort(key=lambda t:(-t[0],t[1],t[2]))
    routes={i:[i] for i in range(1,nn_)}; log=[]
    for s,i,j in S:
        ri=[r for r in routes.values() if i in r][0]; rj=[r for r in routes.values() if j in r][0]
        if ri is rj: log.append((s,i,j,'skip same route')); continue
        # endpoints?
        if ri[-1]==i and rj[0]==j: new=ri+rj
        elif rj[-1]==j and ri[0]==i: new=rj+ri
        elif ri[0]==i and rj[0]==j: new=ri[::-1]+rj
        elif ri[-1]==i and rj[-1]==j: new=ri+rj[::-1]
        else: log.append((s,i,j,'skip interior')); continue
        for k in list(routes):
            if routes[k] is ri or routes[k] is rj: del routes[k]
        routes[new[0]]=new; log.append((s,i,j,'link',list(new)))
        if len(routes)==1 and len(new)==nn_-1: break
    return list(routes.values())[0],log
sv,lg=savings_tsp(); print("Savings TSP",sv,tl(sv)); [print('  ',l) for l in lg]
for lab,t in [('NN',nn),('NI',ni),('CI',ci),('SAV',sv)]:
    t2,lg=two_opt(t); print(lab,"2opt",t2,tl(t2),[x if isinstance(x,int) else (x[0],x[2]) for x in lg])
    t3,lg3=or_opt(t2); print("   +oropt",t3,tl(t3))

# ================= VRP =================
import random, math
q=VRP_DEMAND; Q=45; K=3; pts=TSP_POINTS
def rl(r): return tour_length(r)
def total(routes): return sum(rl(r) for r in routes)
# 2-opt local optimum counterexample
random.seed(3); cnt={}
for t in range(300):
    t0=random.sample(range(1,9),8); t2,_=two_opt(t0); cnt[tl(t2)]=cnt.get(tl(t2),0)+1
print("2-opt local optima from random starts:",sorted(cnt.items()))
# find example of 2-opt local optimum >312
random.seed(3)
for t in range(300):
    t0=random.sample(range(1,9),8); t2,_=two_opt(t0)
    if tl(t2)>312: print("example: start",t0,tl(t0),"-> 2opt",t2,tl(t2)); break
# ---- Clarke-Wright with capacity ----
def cw(Q=45):
    S=[(D[0,i]+D[0,j]-D[i,j],i,j) for i in range(1,9) for j in range(i+1,9)]; S.sort(key=lambda t:(-t[0],t[1],t[2]))
    routes={i:[i] for i in range(1,9)}; load={i:q[i] for i in range(1,9)}; log=[]
    for s,i,j in S:
        ki=[k for k,r in routes.items() if i in r][0]; kj=[k for k,r in routes.items() if j in r][0]
        if ki==kj: log.append((int(s),i,j,'skip: same route')); continue
        ri,rj=routes[ki],routes[kj]
        if load[ki]+load[kj]>Q: log.append((int(s),i,j,f'skip: load {load[ki]}+{load[kj]}>{Q}')); continue
        if ri[-1]==i and rj[0]==j: new=ri+rj
        elif rj[-1]==j and ri[0]==i: new=rj+ri
        elif ri[0]==i and rj[0]==j: new=ri[::-1]+rj
        elif ri[-1]==i and rj[-1]==j: new=ri+rj[::-1]
        else: log.append((int(s),i,j,'skip: interior')); continue
        del routes[ki]; del routes[kj]; routes[new[0]]=new; load[new[0]]=sum(q[c] for c in new); log.append((int(s),i,j,'link',list(new),load[new[0]]))
    return list(routes.values()),log
R,lg=cw(); print("CW",R,[rl(r) for r in R],total(R),[sum(q[c] for c in r) for r in R]); [print('  ',l) for l in lg]
# ---- Sweep ----
def sweep(Q=45,start_angle=0,clockwise=False):
    ang={i:(math.degrees(math.atan2(pts[i][1]-50,pts[i][0]-50))-start_angle)%360 for i in range(1,9)}
    order=sorted(range(1,9),key=lambda i:(-ang[i] if clockwise else ang[i]))
    routes=[]; cur=[]; load=0
    for i in order:
        if load+q[i]>Q: routes.append(cur); cur=[]; load=0
        cur.append(i); load+=q[i]
    routes.append(cur)
    opt=[list(best_route(tuple(r))[1]) for r in routes]
    return order,ang,routes,opt
order,ang,rs,opt=sweep(); print("sweep ccw from east: order",order,{i:round(ang[i]) for i in order},"clusters",rs,"raw",[rl(r) for r in rs],total(rs),"after TSP",opt,[rl(r) for r in opt],total(opt),[sum(q[c] for c in r) for r in rs])
best=None
for sa in range(0,360,5):
    for cwise in (False,True):
        o,a,rs2,opt2=sweep(45,sa,cwise); tcost=total(opt2)
        if len(rs2)<=3 and (best is None or tcost<best[0]): best=(tcost,sa,cwise,opt2)
print("best sweep",best)
# ---- cluster-first with seeds (farthest from depot, min angle) ----
# ---- route-first cluster-second: split optimal giant tour 312 ----
giant=[1,5,3,6,7,8,4,2]
def split(giant,Q=45,K=3):
    n=len(giant); best=(10**9,None)
    for cuts in itertools.combinations(range(1,n),K-1):
        b=[0]+list(cuts)+[n]; routes=[giant[b[i]:b[i+1]] for i in range(K)]
        if any(sum(q[c] for c in r)>Q for r in routes): continue
        tcost=total(routes)
        if tcost<best[0]: best=(tcost,routes)
    # also allow 2 routes
    for cut in range(1,n):
        routes=[giant[:cut],giant[cut:]]
        if any(sum(q[c] for c in r)>Q for r in routes): continue
        if total(routes)<best[0]: best=(total(routes),routes)
    return best
print("split of optimal giant tour",split(giant)); print("split of NN giant", split([2,8,7,6,3,5,1,4]))
# ---- improvement: relocate & swap between routes, plus intra 2-opt ----
def improve(routes,Q=45):
    routes=[list(r) for r in routes]; log=[total(routes)]
    while True:
        best=(total(routes),None)
        for a in range(len(routes)):
            for b in range(len(routes)):
                if a==b: continue
                for i,c in enumerate(routes[a]):
                    if sum(q[x] for x in routes[b])+q[c]>Q: continue
                    for pos in range(len(routes[b])+1):
                        R2=[list(r) for r in routes]; R2[a].pop(i); R2[b].insert(pos,c); R2=[r for r in R2 if r]
                        if total(R2)<best[0]: best=(total(R2),R2)
        for a in range(len(routes)):
            for b in range(a+1,len(routes)):
                for i,c in enumerate(routes[a]):
                    for j,d in enumerate(routes[b]):
                        la=sum(q[x] for x in routes[a])-q[c]+q[d]; lb=sum(q[x] for x in routes[b])-q[d]+q[c]
                        if la>Q or lb>Q: continue
                        R2=[list(r) for r in routes]; R2[a][i]=d; R2[b][j]=c
                        if total(R2)<best[0]: best=(total(R2),R2)
        if best[1] is None: break
        routes=best[1]; routes=[list(best_route(tuple(r))[1]) for r in routes]; log.append(total(routes))
    return routes,log
R2,lg=improve(R); print("CW + improve",R2,total(R2),lg)
R3,lg=improve(opt); print("sweep + improve",R3,total(R3),lg)

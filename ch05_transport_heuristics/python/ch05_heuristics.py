"""Chapter 5 - transportation heuristics: North-west corner, Least cost (dummy first/last), VAM (verbose), stepping-stone/MODI,
Balinski effective-cost construction and lane-closing/opening local search for the FCTP. Run: python ch05_heuristics.py"""
import numpy as np, itertools, sys
import os; sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common')); from data_reference import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ch03_transportation_fctp', 'python')); from ch03_transportation import transport
C=np.c_[COST,np.zeros(3,int)]; S=list(SUPPLY); D=list(DEMAND)+[60]   # balanced with dummy
def nwc(C,S,D):
    S=list(S); D=list(D); x=np.zeros(C.shape,int); i=j=0; steps=[]
    while i<len(S) and j<len(D):
        q=min(S[i],D[j]); x[i,j]=q; S[i]-=q; D[j]-=q; steps.append((i+1,j+1,q,list(S),list(D)))
        if S[i]==0 and i<len(S)-1: i+=1
        elif D[j]==0: j+=1
        else: i+=1
    return x,steps
def least_cost(C,S,D):
    S=list(S); D=list(D); x=np.zeros(C.shape,int); steps=[]; done_r=set(); done_c=set()
    while len(done_r)<len(S) and len(done_c)<len(D):
        cells=[(C[i,j],i,j) for i in range(len(S)) for j in range(len(D)) if i not in done_r and j not in done_c]
        if not cells: break
        _,i,j=min(cells); q=min(S[i],D[j]); x[i,j]=q; S[i]-=q; D[j]-=q; steps.append((i+1,j+1,C[i,j],q,list(S),list(D)))
        if S[i]==0: done_r.add(i)
        if D[j]==0: done_c.add(j)
    return x,steps
def vam(C,S,D):
    S=list(S); D=list(D); x=np.zeros(C.shape,int); rows=set(range(len(S))); cols=set(range(len(D))); steps=[]
    while rows and cols:
        pen=[]
        for i in rows:
            cs=sorted(C[i,j] for j in cols); pen.append((cs[1]-cs[0] if len(cs)>1 else cs[0],'r',i))
        for j in cols:
            cs=sorted(C[i,j] for i in rows); pen.append((cs[1]-cs[0] if len(cs)>1 else cs[0],'c',j))
        p=max(pen,key=lambda t:(t[0],t[1]=='r',-t[2]))   # tie: prefer row, then smaller index
        if p[1]=='r': i=p[2]; j=min(cols,key=lambda j:(C[i,j],j))
        else: j=p[2]; i=min(rows,key=lambda i:(C[i,j],i))
        q=min(S[i],D[j]); x[i,j]=q; S[i]-=q; D[j]-=q
        rp={i:(sorted(C[i,j] for j in cols)) for i in rows}; cp={j:(sorted(C[i,j] for i in rows)) for j in cols}
        steps.append((dict((k,(v[1]-v[0]) if len(v)>1 else v[0]) for k,v in rp.items()),dict((k,(v[1]-v[0]) if len(v)>1 else v[0]) for k,v in cp.items()),p,i+1,j+1,q))
        if S[i]==0: rows.discard(i)
        if D[j]==0: cols.discard(j)
    return x,steps
cost=lambda x:int((C*x).sum())
def least_cost_dummy_last(C,S,D,dummy_col=4):
    S=list(S); D=list(D); x=np.zeros(C.shape,int); steps=[]; done_r=set(); done_c={dummy_col}
    while True:
        cells=[(C[i,j],i,j) for i in range(len(S)) for j in range(len(D)) if i not in done_r and j not in done_c]
        if not cells: break
        _,i,j=min(cells); q=min(S[i],D[j]); x[i,j]=q; S[i]-=q; D[j]-=q; steps.append((i+1,j+1,int(C[i,j]),int(q),list(map(int,S)),list(map(int,D))))
        if S[i]==0: done_r.add(i)
        if D[j]==0: done_c.add(j)
    for i in range(len(S)):
        if S[i]>0: x[i,dummy_col]=S[i]; steps.append((i+1,dummy_col+1,0,int(S[i]),None,None)); S[i]=0
    return x,steps
def vam_verbose(C,S,D):
    S=list(S); D=list(D); x=np.zeros(C.shape,int); rows=set(range(len(S))); cols=set(range(len(D))); steps=[]
    while rows and cols:
        rp={i:(lambda v:(v[1]-v[0]) if len(v)>1 else v[0])(sorted(C[i,j] for j in cols)) for i in rows}
        cp={j:(lambda v:(v[1]-v[0]) if len(v)>1 else v[0])(sorted(C[i,j] for i in rows)) for j in cols}
        pen=[(v,'r',k) for k,v in rp.items()]+[(v,'c',k) for k,v in cp.items()]
        p=max(pen,key=lambda t:(t[0],t[1]=='r',-t[2]))
        if p[1]=='r': i=p[2]; j=min(cols,key=lambda j:(C[i,j],j))
        else: j=p[2]; i=min(rows,key=lambda i:(C[i,j],i))
        q=min(S[i],D[j]); x[i,j]=q; S[i]-=q; D[j]-=q
        steps.append(({k+1:int(v) for k,v in rp.items()},{k+1:int(v) for k,v in cp.items()},('row' if p[1]=='r' else 'col',p[2]+1,int(p[0])),i+1,j+1,int(q)))
        if S[i]==0: rows.discard(i)
        if D[j]==0: cols.discard(j)
    return x,steps
def modi(C,x,maxit=10):
    m,n=C.shape; x=x.copy(); log=[]
    basis=[(i,j) for i in range(m) for j in range(n) if x[i,j]>0]
    # ensure m+n-1 basic cells (add zero cells if degenerate)
    while len(basis)<m+n-1:
        for i in range(m):
            for j in range(n):
                if (i,j) not in basis:
                    test=basis+[(i,j)]
                    if not has_cycle(test,m,n): basis=test; break
            else: continue
            break
    for it in range(maxit):
        u=[None]*m; v=[None]*n; u[0]=0
        changed=True
        while changed:
            changed=False
            for (i,j) in basis:
                if u[i] is not None and v[j] is None: v[j]=C[i,j]-u[i]; changed=True
                elif v[j] is not None and u[i] is None: u[i]=C[i,j]-v[j]; changed=True
        red={(i,j):int(C[i,j]-u[i]-v[j]) for i in range(m) for j in range(n) if (i,j) not in basis}
        ent=min(red,key=lambda k:(red[k],k))
        log.append(dict(it=it+1,u=[int(a) for a in u],v=[int(b) for b in v],red=red,cost=cost(x)))
        if red[ent]>=0: log[-1]['status']='optimal'; break
        cyc=find_cycle(basis+[ent],ent,m,n)
        theta=min(x[c] for c in cyc[1::2]); leave=min(cyc[1::2],key=lambda c:(x[c],c))
        for k,c in enumerate(cyc): x[c]+= theta if k%2==0 else -theta
        basis=[b for b in basis if b!=leave]+[ent]
        log[-1].update(entering=ent,cycle=cyc,theta=int(theta),leaving=leave,newcost=cost(x))
    return x,log
def has_cycle(cells,m,n):
    return find_cycle(cells,cells[-1],m,n) is not None
def find_cycle(cells,start,m,n):
    cells=set(cells)
    def dfs(path,horiz):
        cur=path[-1]
        cand=[c for c in cells if c!=cur and ((c[0]==cur[0]) if horiz else (c[1]==cur[1]))]
        for c in cand:
            if c==start and len(path)>=4 and (not horiz): return path
            if c==start and len(path)>=4 and horiz: return path
            if c in path: continue
            r=dfs(path+[c],not horiz)
            if r: return r
        return None
    for h in (True,False):
        r=dfs([start],h)
        if r and len(r)%2==0: return r
    return None

# ---------- FCTP: Balinski construction + pattern local search ----------
Cf, F, Sf, Df = COST, FIXED, SUPPLY, DEMAND
true_cost = lambda x: int((Cf*x).sum() + F[x > 0].sum())
def pattern_cost(y):
    z, x = transport(Cf, Sf, Df, y); return (None, None) if z is None else (true_cost(x), x)
def balinski():
    M = np.minimum.outer(Sf, Df); z, x = transport(Cf + F/M, Sf, Df); return (x > 0).astype(int), x, true_cost(x)
def pattern_local_search(y, moves=('close', 'open')):
    z, x = pattern_cost(y); path = [z]
    while True:
        best = (z, None)
        for i in range(y.shape[0]):
            for j in range(y.shape[1]):
                if ('close' in moves and y[i, j] == 1) or ('open' in moves and y[i, j] == 0):
                    y2 = y.copy(); y2[i, j] = 1 - y2[i, j]; z2, x2 = pattern_cost(y2)
                    if z2 is not None and z2 < best[0]: best = (z2, (y2, x2))
        if best[1] is None: return y, x, z, path
        z = best[0]; y, x = best[1]; path.append(z)

if __name__ == '__main__':
    for name, f in [('NWC', nwc), ('LC dummy-first', least_cost), ('LC dummy-last', least_cost_dummy_last), ('VAM', vam_verbose)]:
        x, st = f(C, S, D); print(f'{name:15s} cost {cost(x)}')
    xl, _ = least_cost_dummy_last(C, S, D); xo, log = modi(C, xl); print('MODI from LC:', [l['cost'] for l in log], '->', cost(xo))
    yB, xB, zB = balinski(); print('Balinski plan', zB); y, x, z, p = pattern_local_search(yB); print('  + lane local search', p)
    for name, yy in [('LP plan', np.array([[1,1,0,0],[1,0,1,0],[0,0,1,1]])), ('least-unit-cost plan', np.array([[1,1,1,0],[0,1,0,0],[0,1,0,1]]))]:
        y, x, z, p = pattern_local_search(yy); print(name, p)

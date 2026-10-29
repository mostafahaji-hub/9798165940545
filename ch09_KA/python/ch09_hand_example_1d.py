import os
import numpy as np, math
f=lambda x:(x-3.3)**2+1
pop=[1.0,2.0,4.8,5.5]; li=1; L=2.0; fL=f(L); Smax=3; rows=[]
def near(L): return min([p for k,p in enumerate(pop) if k!=li],key=lambda p:abs(p-L))
A=near(L); step=0
while step<30:
    r=L-A; O=L+r; fO=f(O); step+=1; rows.append(('diag',round(A,4),round(r,4),'O',round(O,4),round(fO,4),'slope' if fO<fL else 'pit'))
    if fO<fL: L,fL=O,fO; pop[li]=L; A=near(L); continue
    moved=False
    for s in range(1,Smax+1):
        for c in (L+0.5**s*r, L-0.5**s*r):
            fc=f(c); step+=1; rows.append((f's={s}',round(A,4),round(r,4),'P',round(c,4),round(fc,4),'better' if fc<fL else 'worse'))
            if fc<fL: L,fL=c,fc; pop[li]=L; A=near(L); moved=True; break
        if moved: break
    if not moved: break
for r in rows: print(r)
print('final',L,fL,'evals',step)
# ---- full iteration on 4 cake orders (A,B,D,F), M=5, N1=1, N2=1, N3=3, Smax=2, axis-only swirl
jobs={'A':(3,9,2,5),'B':(1,14,2,3),'D':(7,17,3,4),'F':(6,20,3,3)}; names='ABDF'
def Z(seq):
    t=0;z=0
    for j in seq: p,d,a,b=jobs[j]; t+=p; z+=a*max(0,d-t)+b*max(0,t-d)
    return z
dec=lambda k:''.join(names[i] for i in np.argsort(k,kind='stable'))
K=[[0.62,0.15,0.80,0.40],[0.30,0.55,0.85,0.20],[0.45,0.70,0.25,0.95],[0.85,0.35,0.60,0.05],[0.20,0.90,0.65,0.50]]
print('pop',[(k,dec(k),Z(dec(k))) for k in K])
zs=[Z(dec(k)) for k in K]; li=int(np.argmin(zs)); L=K[li]; print('lucky',li+1,L,dec(L),zs[li])
d=[(i+1,round(sum(abs(a-b) for a,b in zip(K[i],L)),2)) for i in range(5) if i!=li]; print('dist',d)
ai=min([i for i in range(5) if i!=li],key=lambda i:sum(abs(a-b) for a,b in zip(K[i],L))); A=K[ai]; r=[round(a-b,2) for a,b in zip(L,A)]; print('nearest',ai+1,'r',r)
cl=lambda v:[round(min(1,max(0,x)),3) for x in v]
O=cl([l+x for l,x in zip(L,r)]); print('O',O,dec(O),Z(dec(O)))
for s in (1,2):
    for sg in (1,-1):
        c=cl([l+sg*0.5**s*x for l,x in zip(L,r)]); print('s',s,sg,c,dec(c),Z(dec(c)))

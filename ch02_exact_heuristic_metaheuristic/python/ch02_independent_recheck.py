# Independent second implementation (numpy-based) to re-verify Chapter 2 numbers
import numpy as np, itertools
p=np.array([3,1,8,7,2,6]); d=np.array([9,14,19,17,21,20]); a=np.array([2,2,1,3,1,3]); b=np.array([5,3,2,4,3,3]); N='ABCDEF'
def Z(seqstr):
    idx=[N.index(c) for c in seqstr.replace('-','')]
    C=np.cumsum(p[idx]); E=np.maximum(0,d[idx]-C); T=np.maximum(0,C-d[idx]); return int((a[idx]*E+b[idx]*T).sum())
checks={'A-C-B-D-E-F':53,'A-B-D-C-F-E':83,'B-E-A-F-D-C':98,'C-D-F-A-E-B':149,'A-D-B-F-E-C':66,'B-E-A-D-F-C':81,'A-E-B-D-F-C':75,'A-E-D-B-F-C':64,'E-A-D-B-F-C':63,'A-B-D-C-E-F':71,'A-D-B-C-E-F':60,'E-A-D-B-C-F':69,'C-A-D-B-E-F':61,'A-C-D-B-E-F':60,'A-D-E-B-F-C':63,'A-C-B-D-F-E':65}
bad=[(k,v,Z(k)) for k,v in checks.items() if Z(k)!=v]; print('sequence mismatches:',bad)
# local optima under swap, independently
perms=list(itertools.permutations(range(6))); val={s:Z(''.join(N[i] for i in s)) for s in perms}
def sw(s):
    for i,j in itertools.combinations(range(6),2):
        t=list(s); t[i],t[j]=t[j],t[i]; yield tuple(t)
lo=[(''.join(N[i] for i in s),v) for s,v in val.items() if all(val[t]>=v for t in sw(s))]; print('local optima:',lo)
# FCTP heuristic totals, independent allocation (loop with explicit remaining)
S=[180,120,140]; D=[60,140,100,80]; c=np.array([[3,3,2,8],[6,7,4,4],[6,5,3,2]]); f=np.array([[250,350,100,200],[300,250,150,100],[400,350,400,400]])
def alloc(order):
    rs=S[:]; rd=D[:]; x=np.zeros((3,4),int)
    for i,j in order:
        q=min(rs[i],rd[j])
        if q>0: x[i,j]=q; rs[i]-=q; rd[j]-=q
    return x, int((c*x).sum()+f[x>0].sum())
cells=[(i,j) for i in range(3) for j in range(4)]
print('least unit', alloc(sorted(cells,key=lambda ij:(c[ij],ij)))[1])
print('least fixed', alloc(sorted(cells,key=lambda ij:(f[ij],ij)))[1])
print('c+f/min', alloc(sorted(cells,key=lambda ij:(c[ij]+f[ij]/min(S[ij[0]],D[ij[1]]),ij)))[1])
print('c+f/s_i', alloc(sorted(cells,key=lambda ij:(c[ij]+f[ij]/S[ij[0]],ij)))[1])
# optimal plan cost
x=np.zeros((3,4),int); x[0,0]=60;x[0,2]=100;x[1,3]=80;x[2,1]=140; print('opt plan',int((c*x).sum()+f[x>0].sum()), 'LP plan with fixed', end=' ')
x=np.array([[40,140,0,0],[20,0,40,0],[0,0,60,80]]); print(int((c*x).sum()+f[x>0].sum()), 'var only', int((c*x).sum()))

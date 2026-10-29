import os
import numpy as np
jobs={'A':(3,9,2,5),'B':(1,14,2,3),'D':(7,17,3,4),'F':(6,20,3,3)}; names='ABDF'
def Z(seq):
    t=0;z=0
    for j in seq: p,d,a,b=jobs[j]; t+=p; z+=a*max(0,d-t)+b*max(0,t-d)
    return z
dec=lambda k:''.join(names[i] for i in np.argsort(k,kind='stable'))
cl=lambda v:[round(min(1,max(0,x)),3) for x in v]
K={1:[0.35,0.14,0.20,0.59],2:[0.42,0.26,0.73,0.04],3:[0.39,0.07,0.17,0.05],4:[0.53,0.63,0.37,0.72],5:[0.83,0.51,0.33,0.78]}
for i,k in K.items(): print(i,k,dec(k),Z(dec(k)))
L=K[4]; print('dist',{i:round(sum(abs(a-b) for a,b in zip(K[i],L)),2) for i in K if i!=4})
K[4]=[0.38,0.69,0.39,0.69]
print('after swirl lucky',K[4],dec(K[4]),Z(dec(K[4])),'new nn dist',{i:round(sum(abs(a-b) for a,b in zip(K[i],K[4])),2) for i in K if i!=4})
A=K[min([i for i in K if i!=4],key=lambda i:sum(abs(a-b) for a,b in zip(K[i],K[4])))]; r=[round(a-b,3) for a,b in zip(K[4],A)]; print('new r',r)
O=cl([l+x for l,x in zip(K[4],r)]); print('O2',O,dec(O),Z(dec(O)))
for s in (1,2):
    for sg in (1,-1):
        c=cl([l+sg*0.5**s*x for l,x in zip(K[4],r)]); print('s',s,sg,c,dec(c),Z(dec(c)))
K[3]=[0.12,0.88,0.47,0.30]; print('new3',dec(K[3]),Z(dec(K[3])))
for i,(g,h),lam in [(2,(4,1),0.5),(1,(2,5),0.4),(5,(4,2),0.7)]:
    mid=[(a+b)/2 for a,b in zip(K[g],K[h])]; K[i]=[round(x+lam*(m-x),3) for x,m in zip(K[i],mid)]; print('hustle',i,'mid',[round(m,3) for m in mid],'new',K[i],dec(K[i]),Z(dec(K[i])))

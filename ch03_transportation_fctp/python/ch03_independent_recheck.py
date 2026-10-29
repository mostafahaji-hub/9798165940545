"""Independent second check of Chapter 3 numbers: hand-style arithmetic + brute-force over integer grids (no LP solver)."""
import itertools, numpy as np
# Ex 3-1: scan t
Z = {t: 4*t+7*(50-t)+3*(40-t)+5*(30+t) for t in range(0, 41)}; t = min(Z, key=Z.get); print('Ex3-1 best t', t, 'Z', Z[t])
# Ex 3-2: brute force over integer x (two free variables after balance): x_A1=a, x_A2=b, x_A3=100-a-b, x_B1=50-a, x_B2=70-b, x_B3=60-(100-a-b)
c = np.array([[7, 9, 12], [5, 10, 6]]); best = (10**9, None)
for a in range(0, 51):
    for b in range(0, 71):
        x = np.array([[a, b, 100-a-b], [50-a, 70-b, a+b-40]])
        if (x >= 0).all(): z = (c*x).sum(); best = min(best, (z, x.tolist()))
print('Ex3-2 brute force', best)
# Ex 3-3 and 3-6 plan costs by hand
C = np.array([[3, 3, 2, 8], [6, 7, 4, 4], [6, 5, 3, 2]]); F = np.array([[250, 350, 100, 200], [300, 250, 150, 100], [400, 350, 400, 400]])
for name, P in [('LP plan', [[40, 140, 0, 0], [20, 0, 40, 0], [0, 0, 60, 80]]), ('FCTP opt', [[60, 0, 100, 0], [0, 0, 0, 80], [0, 140, 0, 0]]), ('Ex3-10', [[0, 140, 0, 0], [60, 0, 40, 0], [0, 0, 60, 80]])]:
    P = np.array(P); print(name, 'var', (C*P).sum(), 'fixed', F[P > 0].sum(), 'total', (C*P).sum()+F[P > 0].sum(), 'rows', P.sum(1).tolist(), 'cols', P.sum(0).tolist())
# Ex 3-4 plan cost by hand
print('Ex3-4 total', 130*2+130*3 + 40*6+90*4+30*5+100*3)
# Exercise 3-2 scan
Z = {t: 6*t+4*(60-t)+5*(30-t)+8*(10+t) for t in range(0, 31)}; t = min(Z, key=Z.get); print('Exr3-2 t', t, Z[t])
# Exercise 3-12 step trucks
print('Exr3-12 trucks', [int(np.ceil(v/80)) for v in (60, 100, 80, 140)], 'fixed', 250*1+100*2+100*1+350*2, 'total', 1400+250+200+100+700)
print('2^40/1e6 days', 2**40/1e6/86400, '2^200/1e6 years', 2**200/1e6/3.156e7)

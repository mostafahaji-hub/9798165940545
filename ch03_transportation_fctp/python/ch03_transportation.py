"""Chapter 3 - exact solution of the two-level, three-level and fixed-charge transportation problems.
Reproduces every number in Chapter 3 (examples and exercises). Run: python ch03_transportation.py"""
import itertools, sys, os
import numpy as np
from scipy.optimize import linprog
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common'))
from data_reference import SUPPLY, DEMAND, COST, FIXED

def transport(c, s, d, open_mask=None, equality_supply=False):
    """Two-level transportation LP. open_mask (0/1 matrix) closes lanes (x=0). Returns (Z, x) or (None, None)."""
    c = np.array(c, float); s = np.array(s, float); d = np.array(d, float); m, n = c.shape
    A_sup = [np.r_[np.zeros(i*n), np.ones(n), np.zeros((m-i-1)*n)] for i in range(m)]
    A_dem = [np.array([1.0 if k % n == j else 0 for k in range(m*n)]) for j in range(n)]
    bounds = [(0, None) if (open_mask is None or open_mask[i, j]) else (0, 0) for i in range(m) for j in range(n)]
    if equality_supply: r = linprog(c.flatten(), A_eq=np.vstack([A_sup, A_dem]), b_eq=np.r_[s, d], bounds=bounds, method='highs')
    else: r = linprog(c.flatten(), A_ub=A_sup, b_ub=s, A_eq=A_dem, b_eq=d, bounds=bounds, method='highs')
    return (r.fun, np.round(r.x.reshape(m, n)).astype(int)) if r.status == 0 else (None, None)

def three_level(a, b, s, q, d):
    """Plants (s) -> DCs (capacity q) -> retailers (d). a: m x K unit costs, b: K x n. Returns Z, x (m x K), y (K x n)."""
    a = np.array(a, float); b = np.array(b, float); m, K = a.shape; n = b.shape[1]; nx = m*K
    cost = np.r_[a.flatten(), b.flatten()]; A_ub = []; b_ub = []; A_eq = []; b_eq = []
    for i in range(m): row = np.zeros(nx+K*n); row[i*K:(i+1)*K] = 1; A_ub.append(row); b_ub.append(s[i])
    for k in range(K): row = np.zeros(nx+K*n); row[k:nx:K] = 1; A_ub.append(row); b_ub.append(q[k])
    for k in range(K):
        row = np.zeros(nx+K*n); row[k:nx:K] = 1; row[nx+k*n:nx+(k+1)*n] = -1; A_eq.append(row); b_eq.append(0)   # flow conservation
    for j in range(n): row = np.zeros(nx+K*n); row[nx+j::n] = 1; A_eq.append(row); b_eq.append(d[j])
    r = linprog(cost, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
    if r.status != 0: return None, None, None
    x = np.round(r.x[:nx]).astype(int).reshape(m, K); y = np.round(r.x[nx:]).astype(int).reshape(K, n); return r.fun, x, y

def fctp_enumerate(c, f, s, d):
    """Exact FCTP by enumerating all 2^(mn) open/closed patterns (small instances only)."""
    c = np.array(c); f = np.array(f); m, n = c.shape; best = (np.inf, None, None); feasible = 0
    for pat in itertools.product([0, 1], repeat=m*n):
        y = np.array(pat).reshape(m, n); z, x = transport(c, s, d, y)
        if z is None: continue
        feasible += 1; z += f[y == 1].sum()
        if z < best[0] - 1e-9: best = (z, x, y)
    return best, feasible

fctp_cost = lambda x, c=COST, f=FIXED: int((np.array(c)*x).sum() + np.array(f)[np.array(x) > 0].sum())

if __name__ == '__main__':
    print('Ex 3-1:', transport([[4, 7], [3, 5]], [50, 70], [40, 80]))
    print('Ex 3-2:', transport([[7, 9, 12], [5, 10, 6]], [100, 80], [50, 70, 60]))
    print('Ex 3-3:', transport(COST, SUPPLY, DEMAND))
    A3 = [[2, 5, 4], [4, 3, 6]]; B3 = [[6, 4, 8], [5, 7, 3], [6, 6, 6]]
    print('Ex 3-4 (3 DCs, cap 200):', three_level(A3, B3, [150, 130], [200, 200, 200], [70, 90, 100]))
    (z, x, y), feas = fctp_enumerate(COST, FIXED, SUPPLY, DEMAND); print('Ex 3-6: FCTP optimum', z, 'feasible patterns', feas); print(x)
    print('Exercise 3-2:', transport([[6, 4], [5, 8]], [60, 40], [30, 70]))
    print('Exercise 3-4:', transport([[4, 8, 6], [7, 3, 9], [15, 25, 20]], [90, 60, 20], [50, 40, 80], equality_supply=True))
    print('Exercise 3-5:', three_level([[3, 5]], [[4, 6], [2, 3]], [100], [60, 70], [40, 50]))
    print('Exercise 3-6 (cap 120):', three_level(A3, B3, [150, 130], [120, 120, 120], [70, 90, 100]))
    import itertools as it
    for op in it.product([0, 1], repeat=3):
        r = three_level(A3, B3, [150, 130], [200*o for o in op], [70, 90, 100]); print('Exercise 3-13 open', op, 'total', None if (r is None or r[0] is None) else r[0] + 400*sum(op))
    (z, x, y), _ = fctp_enumerate([[3, 6], [5, 4]], [[100, 80], [70, 220]], [100, 100], [80, 80]); print('Exercise 3-7:', z, x.tolist())
    P = np.array([[0, 140, 0, 0], [60, 0, 40, 0], [0, 0, 60, 80]]); print('Exercise 3-10 plan cost:', fctp_cost(P))

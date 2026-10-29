"""Chapter 1 - complete enumeration tools (verification of all Chapter 1 examples & exercises).
Run:  python ch01_enumeration.py
"""
import itertools, math, sys, os
import numpy as np
from scipy.optimize import linprog
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common'))
from data_reference import JOBS6, JOBS4_CH1, FCTP2x2_CH1, SUPPLY, DEMAND, COST, FIXED

# ---------- single machine earliness/tardiness ----------
def et_cost(seq, jobs):
    """seq: list of job indices. Returns (Z, rows) where rows = (name, C, E, T, penalty)."""
    t, z, rows = 0, 0, []
    for j in seq:
        t += jobs['p'][j]
        e, l = max(0, jobs['d'][j] - t), max(0, t - jobs['d'][j])
        pen = jobs['alpha'][j] * e + jobs['beta'][j] * l
        z += pen; rows.append((jobs['names'][j], t, e, l, pen))
    return z, rows

def enumerate_sequences(jobs):
    n = len(jobs['p'])
    return sorted(((et_cost(s, jobs)[0], ''.join(jobs['names'][i] for i in s)) for s in itertools.permutations(range(n))))

def rule(jobs, key):
    n = len(jobs['p'])
    return sorted(range(n), key={'SPT': lambda j: jobs['p'][j], 'LPT': lambda j: -jobs['p'][j],
                                 'EDD': lambda j: jobs['d'][j], 'LDD': lambda j: -jobs['d'][j]}[key])

# ---------- transportation / fixed-charge enumeration ----------
def transport_lp(c, s, d, open_mask=None):
    m, n = c.shape
    A = [np.r_[np.zeros(i * n), np.ones(n), np.zeros((m - i - 1) * n)] for i in range(m)]
    Aeq = [np.array([1.0 if k % n == j else 0 for k in range(m * n)]) for j in range(n)]
    bounds = [(0, None) if (open_mask is None or open_mask[i, j]) else (0, 0) for i in range(m) for j in range(n)]
    r = linprog(c.flatten(), A_ub=A, b_ub=s, A_eq=Aeq, b_eq=d, bounds=bounds, method='highs')
    return (r.fun, r.x.reshape(m, n)) if r.status == 0 else (None, None)

def fctp_enumerate(c, f, s, d):
    c, f = np.array(c), np.array(f); m, n = c.shape; best = (math.inf, None, None)
    for pat in itertools.product([0, 1], repeat=m * n):
        y = np.array(pat).reshape(m, n)
        z, x = transport_lp(c, s, d, y)
        if z is not None:
            z += (f * y).sum()
            if z < best[0] - 1e-9: best = (z, np.round(x), y)
    return best

if __name__ == '__main__':
    print('Example 1.2 (4 orders):', enumerate_sequences(JOBS4_CH1)[:3])
    for k in ('SPT', 'EDD'):
        s = rule(JOBS4_CH1, k); print(k, ''.join(JOBS4_CH1['names'][i] for i in s), et_cost(s, JOBS4_CH1)[0])
    print('Example 1.3 (2x2 FCTP):', fctp_enumerate(**FCTP2x2_CH1))
    res = enumerate_sequences(JOBS6); print('Example 1.5 (6 orders) optimum:', res[0], ' median:', res[360][0])
    for k in ('SPT', 'EDD', 'LPT'):
        s = rule(JOBS6, k); print(k, ''.join(JOBS6['names'][i] for i in s), et_cost(s, JOBS6)[0])
    print('Reference FCTP optimum (Chapter 3):', fctp_enumerate(COST, FIXED, SUPPLY, DEMAND)[0])

# ---------- ratio heuristics (Section 1-8 and Exercise 1-12) ----------
def ratio_rule(jobs, key):
    n = len(jobs['p']); s = sorted(range(n), key=key)
    return ''.join(jobs['names'][i] for i in s), et_cost(s, jobs)[0]

if __name__ == '__main__':
    J = JOBS6
    print('d/beta :', ratio_rule(J, lambda j: J['d'][j] / J['beta'][j]))   # A-D-B-F-E-C, 66
    print('p/beta :', ratio_rule(J, lambda j: J['p'][j] / J['beta'][j]))   # B-A-E-D-F-C, 82
    print('d-p    :', ratio_rule(J, lambda j: J['d'][j] - J['p'][j]))      # A-D-C-B-F-E, 82

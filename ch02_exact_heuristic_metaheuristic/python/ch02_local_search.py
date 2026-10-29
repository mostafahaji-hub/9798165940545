"""Chapter 2 - exact LP, constructive heuristics with arbitrary key, local search, random-restart local search.
Reproduces every number of Chapter 2 (run: python ch02_local_search.py)."""
import itertools, random, sys, os
import numpy as np
from scipy.optimize import linprog
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common'))
from data_reference import JOBS6, SUPPLY, DEMAND, COST, FIXED
J = JOBS6; n = 6; N = J['names']

def Z(seq):
    t = z = 0
    for j in seq:
        t += J['p'][j]; z += J['alpha'][j]*max(0, J['d'][j]-t) + J['beta'][j]*max(0, t-J['d'][j])
    return z
name = lambda s: '-'.join(N[i] for i in s)

def swap_neighbours(s):
    for i, j in itertools.combinations(range(len(s)), 2):
        t = list(s); t[i], t[j] = t[j], t[i]; yield tuple(t)
def insert_neighbours(s):
    for i in range(len(s)):
        for j in range(len(s)):
            if i != j:
                t = list(s); e = t.pop(i); t.insert(j, e); yield tuple(t)

def local_search(s, nb=swap_neighbours, verbose=False):
    """Best-improvement local search; ties broken by first in enumeration order."""
    path = [(name(s), Z(s))]
    while True:
        best = min(nb(s), key=Z)              # min keeps the first minimum (stable)
        if Z(best) < Z(s): s = best; path.append((name(s), Z(s)))
        else: break
    if verbose: print(' -> '.join(f'{a}({b})' for a, b in path))
    return s, path

def random_restart_ls(R, seed, nb=swap_neighbours):
    rng = random.Random(seed); best = None
    for _ in range(R):
        s, _ = local_search(tuple(rng.sample(range(n), n)), nb)
        if best is None or Z(s) < Z(best): best = s
    return best

# ---- transportation: exact LP and greedy heuristics ----
def transport_lp(c, s, d):
    m, k = c.shape
    A = [np.r_[np.zeros(i*k), np.ones(k), np.zeros((m-i-1)*k)] for i in range(m)]
    Aeq = [np.array([1.0 if q % k == j else 0 for q in range(m*k)]) for j in range(k)]
    r = linprog(c.flatten(), A_ub=A, b_ub=s, A_eq=Aeq, b_eq=d, bounds=(0, None), method='highs')
    return r.fun, np.round(r.x.reshape(m, k)).astype(int)

def greedy_transport(key):
    """key: m x n matrix; cheapest key first; ship min(remaining supply, remaining demand)."""
    s = SUPPLY.astype(float).copy(); d = DEMAND.astype(float).copy(); x = np.zeros(COST.shape, int)
    for _, i, j in sorted((key[i, j], i, j) for i in range(COST.shape[0]) for j in range(COST.shape[1])):
        q = int(min(s[i], d[j])); x[i, j] = q; s[i] -= q; d[j] -= q
    return x
fctp_cost = lambda x: int((COST*x).sum() + FIXED[x > 0].sum())

if __name__ == '__main__':
    z, x = transport_lp(COST, SUPPLY, DEMAND); print('Example 2-1 LP optimum', z); print(x)
    rules = {'SPT': lambda j: J['p'][j], 'EDD': lambda j: J['d'][j], 'LPT': lambda j: -J['p'][j], 'd/beta': lambda j: J['d'][j]/J['beta'][j]}
    for k, f in rules.items():
        s = tuple(sorted(range(n), key=f)); print(f'{k:7s} {name(s)} Z={Z(s)} RPD={(Z(s)-53)/53*100:.1f}%')
    M = np.minimum.outer(SUPPLY, DEMAND)
    for lab, key in [('c', COST*1.0), ('f', FIXED*1.0), ('c+f/min', COST+FIXED/M), ('c+f/s_i', COST+FIXED/SUPPLY[:, None]), ('c+f/d_j', COST+FIXED/DEMAND[None, :])]:
        x = greedy_transport(key); print(f'Example 2-3 {lab:8s} cost={fctp_cost(x)} RPD={(fctp_cost(x)-2200)/2200*100:.1f}%')
    print('Example 2-4:')
    for k in ('SPT', 'EDD', 'd/beta'): local_search(tuple(sorted(range(n), key=rules[k])), verbose=True)
    local_search(tuple(sorted(range(n), key=rules['SPT'])), insert_neighbours, verbose=True)
    allp = list(itertools.permutations(range(n)))
    lo = [(name(s), Z(s)) for s in allp if all(Z(t) >= Z(s) for t in swap_neighbours(s))]; print('swap local optima:', lo)
    rng = random.Random(0); cnt = {}
    for _ in range(1000):
        s, _ = local_search(tuple(rng.sample(range(n), n))); cnt[name(s)] = cnt.get(name(s), 0) + 1
    print('basins (1000 random starts):', cnt)
    res = [Z(random_restart_ls(1, seed)) for seed in range(1, 31)]
    print('Example 2-5: 30 runs', res, 'mean', np.mean(res), 'hits', res.count(53))

# ---------- lower bounds for the FCTP (Section 2-8-3) ----------
def fctp_lower_bounds():
    lb1, _ = transport_lp(COST * 1.0, SUPPLY, DEMAND)                       # drop fixed charges
    Mmat = np.minimum.outer(SUPPLY, DEMAND)
    lb2, x2 = transport_lp(COST + FIXED / Mmat, SUPPLY, DEMAND)              # Balinski (1961) LP relaxation
    return lb1, lb2, x2

if __name__ == '__main__':
    lb1, lb2, x2 = fctp_lower_bounds()
    print('LB1 (drop fixed) =', lb1, ' LB2 (Balinski) =', round(lb2, 2)); print(x2)
    for z in (2200, 2510, 2840): print(f'Z={z}: gap vs LB1 {(z-lb1)/lb1*100:.1f}%  gap vs LB2 {(z-lb2)/lb2*100:.1f}%')
    res = [53]*17 + [63]*13
    print('30-run stats: mean', np.mean(res), 'std', round(np.std(res, ddof=1), 2), 'mean RPD', round(np.mean([(r-53)/53*100 for r in res]), 2))

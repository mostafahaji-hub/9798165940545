"""Chapter 4 - exact tools: single-machine E/T evaluation + enumeration, TSP brute force + Held-Karp DP, small VRP by partition enumeration.
Run: python ch04_exact.py"""
import itertools, sys, os
from functools import lru_cache
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common'))
from data_reference import JOBS6, TSP_DIST as D, VRP_DEMAND as Q_DEM, VRP_K, VRP_Q
N = JOBS6['names']

def et_eval(seq, J=JOBS6):
    """Returns Z (weighted E/T), plus sumC, Lmax, sumT for the sequence of job indices."""
    t = 0; Z = 0; C = []; L = []; T = []
    for j in seq:
        t += J['p'][j]; C.append(t); L.append(t - J['d'][j]); T.append(max(0, t - J['d'][j]))
        Z += J['alpha'][j]*max(0, J['d'][j]-t) + J['beta'][j]*max(0, t-J['d'][j])
    return dict(Z=Z, sumC=sum(C), Lmax=max(L), sumT=sum(T), Cmax=t)

def tour_length(tour, D=D):
    s = [0] + list(tour) + [0]; return int(sum(D[a, b] for a, b in zip(s, s[1:])))

def tsp_brute(D=D):
    n = len(D); best = (10**9, None)
    for perm in itertools.permutations(range(1, n)):
        if perm[0] > perm[-1]: continue            # skip reversed duplicates (symmetric)
        L = tour_length(perm, D)
        if L < best[0]: best = (L, perm)
    return best

def tsp_held_karp(D=D):
    """Dynamic programming (Held & Karp 1962), independent of brute force."""
    n = len(D); INF = 10**9
    dp = {(1 << 0, 0): (0, None)}
    for mask in range(1, 1 << n):
        if not mask & 1: continue
        for j in range(1, n):
            if not mask & (1 << j): continue
            prev = mask ^ (1 << j); best = (INF, None)
            for k in range(n):
                if k != j and prev & (1 << k) and (prev, k) in dp:
                    v = dp[(prev, k)][0] + D[k, j]
                    if v < best[0]: best = (v, k)
            if best[1] is not None: dp[(mask, j)] = best
    full = (1 << n) - 1; L, j = min((dp[(full, j)][0] + D[j, 0], j) for j in range(1, n))
    tour = []; mask = full
    while j != 0: tour.append(j); mask, j = mask ^ (1 << j), dp[(mask, j)][1]
    return int(L), tuple(reversed(tour))

def nearest_neighbour(D=D):
    n = len(D); tour = [0]; left = set(range(1, n))
    while left: j = min(left, key=lambda k: (D[tour[-1], k], k)); tour.append(j); left.remove(j)
    return tuple(tour[1:]), tour_length(tour[1:], D)

@lru_cache(None)
def best_route(custs):
    best = (10**9, None)
    for perm in itertools.permutations(custs):
        L = tour_length(perm)
        if L < best[0]: best = (L, perm)
    return best

def vrp_exact(K=VRP_K, Q=VRP_Q, custs=range(1, 9), dem=Q_DEM):
    custs = list(custs); best = (10**9, None); seen = set()
    for assign in itertools.product(range(K), repeat=len(custs)):
        groups = tuple(sorted(tuple(c for c, a in zip(custs, assign) if a == k) for k in range(K)))
        if groups in seen: continue
        seen.add(groups)
        if any(sum(dem[c] for c in g) > Q for g in groups): continue
        tot = 0; routes = []
        for g in groups:
            if g: L, p = best_route(g); tot += L; routes.append((p, L, sum(dem[c] for c in g)))
        if tot < best[0]: best = (tot, routes)
    return best

if __name__ == '__main__':
    allp = list(itertools.permutations(range(6)))
    opt = min(allp, key=lambda s: et_eval(s)['Z']); print('Ex 4-3 optimum', ''.join(N[i] for i in opt), et_eval(opt))
    for key in ('sumC', 'Lmax', 'sumT'): b = min(allp, key=lambda s: et_eval(s)[key]); print('  min', key, ''.join(N[i] for i in b), et_eval(b)[key])
    print('Ex 4-7 TSP brute force', tsp_brute(), ' Held-Karp', tsp_held_karp(), ' NN', nearest_neighbour())
    print('Ex 4-8 small VRP', vrp_exact(2, 35, [2, 4, 7, 8]))
    print('Ex 4-9 reference VRP', vrp_exact()); print('  2 vans Q=60', vrp_exact(2, 60)); print('  Q=50', vrp_exact(3, 50)[0], ' Q=40', vrp_exact(3, 40)[0])

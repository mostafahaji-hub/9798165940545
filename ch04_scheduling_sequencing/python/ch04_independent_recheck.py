"""Independent second check: VRP optimum via giant-tour + split enumeration (different logic from partition enumeration);
TSP via Held-Karp DP (ch04_exact.tsp_held_karp); E/T via numpy cumulative sums."""
import itertools, numpy as np, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'common'))
from data_reference import TSP_DIST as D, VRP_DEMAND as q, JOBS6
def vrp_split(K, Q, custs=range(1, 9)):
    custs = list(custs); n = len(custs); best = (10**9, None)
    for perm in itertools.permutations(custs):
        for r in range(1, K+1):
            for cuts in itertools.combinations(range(1, n), r-1):
                b = [0] + list(cuts) + [n]; routes = [perm[b[i]:b[i+1]] for i in range(r)]
                if any(sum(q[c] for c in rt) > Q for rt in routes): continue
                tot = sum(D[0, rt[0]] + sum(D[rt[i], rt[i+1]] for i in range(len(rt)-1)) + D[rt[-1], 0] for rt in routes)
                if tot < best[0]: best = (tot, routes)
    return best
if __name__ == '__main__':
    print('VRP ref (3,45) by split:', vrp_split(3, 45)); print('VRP (2,60):', vrp_split(2, 60)[0]); print('small VRP (2,35):', vrp_split(2, 35, [2, 4, 7, 8]))
    p = np.array(JOBS6['p']); d = np.array(JOBS6['d']); a = np.array(JOBS6['alpha']); b = np.array(JOBS6['beta'])
    for s, name in [([0,2,1,3,4,5], 'ACBDEF'), ([3,0,1,2,4,5], 'DABCEF'), ([1,4,0,5,3,2], 'SPT')]:
        C = np.cumsum(p[s]); print(name, 'Z', int((a[s]*np.maximum(0, d[s]-C) + b[s]*np.maximum(0, C-d[s])).sum()), 'sumC', int(C.sum()), 'Lmax', int((C-d[s]).max()), 'sumT', int(np.maximum(0, C-d[s]).sum()))

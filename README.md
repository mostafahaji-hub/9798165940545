# Code Bank — Heuristic and Metaheuristic Optimization for Logistics and Production Systems

Companion code for the textbook *Heuristic and Metaheuristic Optimization for Logistics and Production Systems: An Introductory Textbook with Applications to Network Design, Vehicle Routing, and Production Scheduling* (Fatemeh Gholian-Jouybari, Saber Molla-Alizadeh-Zavardehi, Mostafa Hajiaghaei-Keshteli; first edition, 2026; ISBN 9798165940545).

Code bank version 2.5. The folder names below are exactly those of Table B.1 (Appendix B) of the book. Each chapter folder has a `python` and a `matlab` subfolder. The Python codes, with fixed random seeds (main runs: seeds 1 to 30; tuning experiments: seeds 100 to 109), reproduce every number and figure in the book; the MATLAB codes are simpler teaching versions.

| Chapter | Folder | Main files | What it does |
|:--:|:--|:--|:--|
| Common | `common` | `data_reference.py` | Data of the four reference problems: fixed-charge transportation, six cake orders, TSP, and VRP |
| 1 | `ch01_optimization_basics` | `ch01_enumeration.py`, `ch01_enumeration.m`, `ch01_fctp_enum.m` | Complete enumeration of the examples of Chapter 1 |
| 2 | `ch02_exact_heuristic_metaheuristic` | `ch02_local_search.py`, `ch02_benchmarks.py`, `ch02_fctp_heuristics.m` | Fixed-charge heuristics, local search, benchmark functions |
| 3 | `ch03_transportation_fctp` | `ch03_transportation.py`, `ch03_three_level.m` | Exact solution of the two-level, three-level, and fixed-charge transportation problems |
| 4 | `ch04_scheduling_sequencing` | `ch04_exact.py`, `ch04_exact.m` | Exact solution of the single-machine, TSP, and VRP problems by enumeration |
| 5 | `ch05_transport_heuristics` | `ch05_heuristics.py`, `ch05_constructive.m` | North-west corner, least cost, Vogel, MODI, Balinski, search over patterns |
| 6 | `ch06_sequencing_heuristics` | `ch06_heuristics.py`, `ch06_tsp_heuristics.m` | Dispatching rules, ATC, constructive and improvement heuristics for the TSP and VRP |
| 7 | `ch07_SA` | `ch07_sa.py`, `ch07_tuning.py`, `ch07_final_runs.py`, `SA.m`, `ch07_sa_tsp.m` | Simulated annealing on the four problems, tuning, and 30 runs |
| 8 | `ch08_GA` | `ch08_ga.py`, `ch08_pool_ga.py`, `ch08_tuning.py`, `ch08_ga_pool_tsp.m` | Genetic algorithm with random keys, GASA, the pool-based version, tuning, and 30 runs |
| 9 | `ch09_KA` | `ch09_ka.py`, `ch09_tuning_l9.py`, `ch09_benchmarks.py`, `ch09_keshtel.m` | The textbook Keshtel algorithm, KASA, Taguchi L9, shifted benchmark functions |

## Requirements
Python 3 with NumPy, SciPy, and Matplotlib (for example `pip install numpy scipy matplotlib`). The MATLAB files run in any recent MATLAB version (the transportation models use `linprog` / `intlinprog` from the Optimization Toolbox).

## How to run
Run the scripts from inside the `python` subfolder of a chapter, for example `cd ch07_SA/python` and then `python ch07_sa.py`. The data of the reference problems are read from `common/data_reference.py`.

## Changes in version 2.5
- Folder structure aligned exactly with Table B.1 of the book (earlier draft folders removed from the public code bank).
- `ch07_SA/python/ch07_tuning.py`: the Taguchi signal-to-noise ratio uses the standard smaller-the-better formula, SN = −10 log10(mean of RPD²), as printed in Section 7.6.2 and Pseudo-Code 7.2.

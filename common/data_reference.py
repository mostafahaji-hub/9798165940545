"""Reference instances of the fictional company "Sahar" used throughout the book.
Designed (and verified by exact enumeration) so that simple rules and LP relaxations
are NOT optimal: objectives contain conflicting forces (earliness vs tardiness; unit cost vs fixed charge)."""
import numpy as np

# --- Fixed-charge transportation instance (Chapter 3, 5, 7-9): 3 plants x 4 DCs, pallets/week
SUPPLY = np.array([180, 120, 140])          # total 440 (unbalanced: 60 surplus)
DEMAND = np.array([60, 140, 100, 80])       # total 380
COST   = np.array([[3, 3, 2, 8],            # unit cost per pallet
                   [6, 7, 4, 4],
                   [6, 5, 3, 2]])
FIXED  = np.array([[250, 350, 100, 200],    # weekly fixed charge if a lane is used
                   [300, 250, 150, 100],
                   [400, 350, 400, 400]])
# Verified: pure transportation (no fixed) optimum = 1160; FCTP optimum = 2200 with
# x13=60, x13... see enum_fctp: x[0,0]=60, x[0,2]=100, x[1,3]=80, x[2,1]=140 ; LP-optimal plan costs 3010 with fixed charges.

# --- Single-machine earliness/tardiness instance (Chapter 4, 6, 7-9): 6 cake orders, hours
JOBS6 = dict(names=list("ABCDEF"), p=[3, 1, 8, 7, 2, 6], d=[9, 14, 19, 17, 21, 20],
             alpha=[2, 2, 1, 3, 1, 3], beta=[5, 3, 2, 4, 3, 3])
# Verified by enumeration of 720 sequences: optimum A-C-B-D-E-F, Z=53 (unique); SPT=98, EDD=83, LPT=149.

# --- Small teaching instances used in Chapter 1
JOBS4_CH1 = dict(names=list("ABDF"), p=[3, 1, 7, 6], d=[9, 14, 17, 20], alpha=[2, 2, 3, 3], beta=[5, 3, 4, 3])  # opt A-D-B-F = 48
FCTP2x2_CH1 = dict(c=[[3, 6], [5, 4]], f=[[300, 80], [70, 220]], s=[100, 100], d=[80, 80])            # opt 1030 (anti-diagonal)

# --- TSP / VRP reference instance (Chapter 4, 6, 7-9): Sami's route, depot = DC at (50,50), 8 shops, km, Euclidean rounded
TSP_POINTS = [(50, 50), (80, 75), (34, 80), (33, 5), (14, 95), (85, 12), (34, 13), (9, 47), (14, 70)]
TSP_DIST = np.array([[0,39,34,48,58,52,40,41,41],[39,0,46,84,69,63,77,76,66],[34,46,0,75,25,85,67,41,22],[48,84,75,0,92,52,8,48,68],
                     [58,69,25,92,0,109,84,48,25],[52,63,85,52,109,0,51,84,92],[40,77,67,8,84,51,0,42,60],[41,76,41,48,48,84,42,0,24],[41,66,22,68,25,92,60,24,0]])
VRP_DEMAND = [0, 12, 18, 9, 15, 21, 8, 14, 17]     # total 114
VRP_K, VRP_Q = 3, 45
# Verified: TSP optimum 312 (DC-1-5-3-6-7-8-4-2-DC, unique up to reversal); nearest neighbour 372.
# VRP optimum (3 vans, Q=45) = 425: DC-1-4-2 (45), DC-5-3-6 (38), DC-7-8 (31). With 2 vans Q=60: 411.

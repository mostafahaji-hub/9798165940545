%% Chapter 7 - Simulated annealing for the 8-shop reference TSP (optimum 312), 30 runs
clc; clear;
D = [0 39 34 48 58 52 40 41 41; 39 0 46 84 69 63 77 76 66; 34 46 0 75 25 85 67 41 22; 48 84 75 0 92 52 8 48 68; ...
     58 69 25 92 0 109 84 48 25; 52 63 85 52 109 0 51 84 92; 40 77 67 8 84 51 0 42 60; 41 76 41 48 48 84 42 0 24; 41 66 22 68 25 92 60 24 0];
p0 = 0.8; alpha = 0.8; L = 5; budget = 300; res = zeros(30,1);
for run = 1:30
    rng(run); x = randperm(8) + 1; fx = tourlen(x, D);
    % initial temperature from a short random walk
    deltas = []; y = x; fy = fx;
    for k = 1:100, z = neighbour(y); fz = tourlen(z, D); if fz > fy, deltas(end+1) = fz - fy; end; y = z; fy = fz; end
    T0 = -mean([deltas 1]) / log(p0); T = T0; best = fx; evals = 0;
    while evals < budget
        for k = 1:L
            y = neighbour(x); fy = tourlen(y, D); evals = evals + 1; d = fy - fx;
            if d <= 0 || rand < exp(-d/T), x = y; fx = fy; end
            if fx < best, best = fx; end
            if evals >= budget, break; end
        end
        T = max(alpha*T, 0.01*T0);
    end
    res(run) = best;
end
fprintf('SA on TSP: best %d  mean %.1f  worst %d  hits %d/30\n', min(res), mean(res), max(res), sum(res == 312));
function L = tourlen(t, D), c = [1 t 1]; L = sum(D(sub2ind(size(D), c(1:end-1), c(2:end)))); end
function y = neighbour(x)
    y = x; ij = sort(randperm(8, 2)); i = ij(1); j = ij(2);
    if rand < 0.7, y(i:j) = y(j:-1:i); else, e = y(i); y(i) = []; y = [y(1:j-1) e y(j:end)]; end
end

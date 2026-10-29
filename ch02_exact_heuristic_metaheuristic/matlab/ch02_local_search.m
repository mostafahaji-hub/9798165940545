%% Chapter 2 - local search (best improvement, swap neighbourhood) and random-restart local search
% Reference 6-order instance; optimum A-C-B-D-E-F, Z = 53. Local optima under swap: 53, 63 (A-D-E-B-F-C), 63 (E-A-D-B-F-C)
clc; clear; rng(1);
names = 'ABCDEF'; p = [3 1 8 7 2 6]; d = [9 14 19 17 21 20]; alpha = [2 2 1 3 1 3]; beta = [5 3 2 4 3 3];
[~, spt] = sort(p); [~, edd] = sort(d); [~, db] = sort(d ./ beta);
starts = {spt, 'SPT'; edd, 'EDD'; db, 'd/beta'};
for k = 1:3
    [s, path] = localSearch(starts{k,1}, p, d, alpha, beta);
    fprintf('%s: %s\n', starts{k,2}, strjoin(arrayfun(@(v) num2str(v), path, 'UniformOutput', false), ' -> '));
end
% 30 independent runs of random-start local search
res = zeros(30,1);
for r = 1:30
    rng(r); s0 = randperm(6); [~, path] = localSearch(s0, p, d, alpha, beta); res(r) = path(end);
end
fprintf('30 runs: best %d, mean %.2f, worst %d, hits %d\n', min(res), mean(res), max(res), sum(res==53));

function z = ETcost(seq, p, d, alpha, beta)
    t = 0; z = 0;
    for j = seq, t = t + p(j); z = z + alpha(j)*max(0, d(j)-t) + beta(j)*max(0, t-d(j)); end
end
function [s, path] = localSearch(s, p, d, alpha, beta)
    path = ETcost(s, p, d, alpha, beta);
    while true
        bestZ = inf; best = s;
        for i = 1:numel(s)-1
            for j = i+1:numel(s)
                t = s; t([i j]) = t([j i]); z = ETcost(t, p, d, alpha, beta);
                if z < bestZ, bestZ = z; best = t; end   % strict < keeps the first minimum (tie rule)
            end
        end
        if bestZ < path(end), s = best; path(end+1) = bestZ; else, break; end
    end
end

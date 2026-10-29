%% Chapter 8 - pool-based GA with random keys (classroom logic: crossover offspring + mutants + parents -> keep best npop)
% Reference 8-shop TSP (optimum 312). Operators follow the course files: RouletteWheel, One/Two-point/Uniform crossover,
% Swap/BigSwap/Inversion/Displacement mutation, all applied to the random-key vector.
clc; clear; rng(1);
D = [0 39 34 48 58 52 40 41 41; 39 0 46 84 69 63 77 76 66; 34 46 0 75 25 85 67 41 22; 48 84 75 0 92 52 8 48 68; ...
     58 69 25 92 0 109 84 48 25; 52 63 85 52 109 0 51 84 92; 40 77 67 8 84 51 0 42 60; 41 76 41 48 48 84 42 0 24; 41 66 22 68 25 92 60 24 0];
n = 8; npop = 20; Maxit = 100; PCrossover = 0.8; PMutation = 0.3;
NCrossover = 2*round(PCrossover*npop/2); NMutation = floor(PMutation*npop);
Cost = @(k) tourlen(decode(k), D);
pop = rand(npop, n); cost = arrayfun(@(r) Cost(pop(r,:)), 1:npop)'; BestCost = zeros(Maxit,1);
for it = 1:Maxit
    P = (1./cost) / sum(1./cost);                        % roulette probabilities (minimisation: 1/cost)
    popC = zeros(NCrossover, n);
    for k = 1:2:NCrossover
        p1 = pop(roulette(P),:); p2 = pop(roulette(P),:);
        [popC(k,:), popC(k+1,:)] = crossover(randi(3), p1, p2);
    end
    popM = zeros(NMutation, n);
    for k = 1:NMutation, popM(k,:) = mutation(randi(4), pop(randi(npop),:)); end
    pool = [pop; popC; popM]; pc = arrayfun(@(r) Cost(pool(r,:)), 1:size(pool,1))';
    [pc, idx] = sort(pc); pop = pool(idx(1:npop),:); cost = pc(1:npop); BestCost(it) = cost(1);
end
fprintf('Best tour: %s  length %d\n', mat2str(decode(pop(1,:))), cost(1)); plot(BestCost); xlabel('iteration'); ylabel('best cost');
function t = decode(k), [~, t] = sort(k); end
function L = tourlen(t, D), c = [1 t+1 1]; L = sum(D(sub2ind(size(D), c(1:end-1), c(2:end)))); end
function k = roulette(P), r = rand; c = cumsum(P); k = find(r <= c, 1); end
function [a, b] = crossover(idx, p1, p2)
    n = numel(p1);
    switch idx
        case 1, pt = randi(n-1); a = [p1(1:pt) p2(pt+1:n)]; b = [p2(1:pt) p1(pt+1:n)];
        case 2, pt = sort(randperm(n-1, 2)); a = [p2(1:pt(1)) p1(pt(1)+1:pt(2)) p2(pt(2)+1:n)]; b = [p1(1:pt(1)) p2(pt(1)+1:pt(2)) p1(pt(2)+1:n)];
        case 3, m = rand(1,n) < 0.5; a = p1; b = p2; a(~m) = p2(~m); b(~m) = p1(~m);
    end
end
function y = mutation(idx, x)
    n = numel(x); y = x;
    switch idx
        case 1, i = randi(n-1); y([i i+1]) = y([i+1 i]);                       % adjacent swap
        case 2, ij = randperm(n, 2); y(ij) = y(fliplr(ij));                    % big swap
        case 3, ij = sort(randperm(n, 2)); y(ij(1):ij(2)) = y(ij(2):-1:ij(1)); % inversion
        case 4, ij = sort(randperm(n-1, 2)) + 1; seg = y(ij(1):ij(2)); y = [seg y(1:ij(1)-1) y(ij(2)+1:end)]; % displacement
    end
end

%% Chapter 4 - exact enumeration for the single-machine E/T instance and the 8-shop TSP (reference instances)
clc; clear;
names = 'ABCDEF'; p = [3 1 8 7 2 6]; d = [9 14 19 17 21 20]; alpha = [2 2 1 3 1 3]; beta = [5 3 2 4 3 3];
P = perms(1:6); Z = arrayfun(@(k) ETcost(P(k,:), p, d, alpha, beta), 1:size(P,1));
[zb, k] = min(Z); fprintf('Single machine optimum: %s  Z = %d\n', names(P(k,:)), zb);
D = [0 39 34 48 58 52 40 41 41; 39 0 46 84 69 63 77 76 66; 34 46 0 75 25 85 67 41 22; 48 84 75 0 92 52 8 48 68; ...
     58 69 25 92 0 109 84 48 25; 52 63 85 52 109 0 51 84 92; 40 77 67 8 84 51 0 42 60; 41 76 41 48 48 84 42 0 24; 41 66 22 68 25 92 60 24 0];
T = perms(2:9); best = inf;
for k = 1:size(T,1)
    tour = [1 T(k,:) 1]; L = sum(D(sub2ind(size(D), tour(1:end-1), tour(2:end))));
    if L < best, best = L; bt = tour; end
end
fprintf('TSP optimum: %d km, tour: %s\n', best, mat2str(bt-1));   % nodes printed with DC = 0
function z = ETcost(seq, p, d, alpha, beta)
    t = 0; z = 0;
    for j = seq, t = t + p(j); z = z + alpha(j)*max(0, d(j)-t) + beta(j)*max(0, t-d(j)); end
end

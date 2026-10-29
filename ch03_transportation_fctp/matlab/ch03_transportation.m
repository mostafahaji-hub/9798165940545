%% Chapter 3 - exact solution of the two-level and fixed-charge transportation problems (reference instance)
% Requires Optimization Toolbox (linprog). Reference: optimum 1160 (simple), 2200 (fixed charge, 4 lanes).
clc; clear;
c = [3 3 2 8; 6 7 4 4; 6 5 3 2]; f = [250 350 100 200; 300 250 150 100; 400 350 400 400];
s = [180 120 140]; d = [60 140 100 80];
[x, z] = transportLP(c, s, d, ones(3,4)); fprintf('Simple TP optimum = %g\n', z); disp(x);
best = inf; [m,n] = size(c);
for pat = 0:2^(m*n)-1
    y = reshape(bitget(pat, 1:m*n), n, m)';
    [x, z] = transportLP(c, s, d, y);
    if ~isempty(x), z = z + sum(f(y==1)); if z < best, best = z; xbest = x; ybest = y; end, end
end
fprintf('FCTP optimum = %g\n', best); disp(xbest); disp(ybest);

function [x, z] = transportLP(c, s, d, y)
    [m,n] = size(c); yt = y'; ub = inf(m*n,1); ub(yt(:)==0) = 0;
    Aub = kron(eye(m), ones(1,n)); Aeq = kron(ones(1,m), eye(n));
    [xv, z, flag] = linprog(reshape(c',[],1), Aub, s', Aeq, d', zeros(m*n,1), ub, optimoptions('linprog','Display','none'));
    if flag == 1, x = round(reshape(xv, n, m)'); else, x = []; z = inf; end
end

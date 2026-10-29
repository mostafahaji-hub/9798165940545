%% Chapter 1 - enumeration of open/closed lane patterns for the fixed-charge transportation problem
% Example 1.3 (2x2): optimum 1030 using lanes 1->2 and 2->1. Requires Optimization Toolbox (linprog).
clc; clear;
c = [3 6; 5 4]; f = [300 80; 70 220]; s = [100 100]; d = [80 80];
[m,n] = size(c); best = inf;
for pat = 0:2^(m*n)-1
    y = reshape(bitget(pat, 1:m*n), n, m)';        % open/closed pattern
    yt = y'; ub = inf(m*n,1); ub(yt(:)==0) = 0;     % closed lanes forced to zero
    Aub = kron(eye(m), ones(1,n)); Aeq = kron(ones(1,m), eye(n));
    [x, z, flag] = linprog(reshape(c',[],1), Aub, s', Aeq, d', zeros(m*n,1), ub, optimoptions('linprog','Display','none'));
    if flag == 1
        z = z + sum(sum(f.*y));
        if z < best, best = z; xbest = reshape(x,n,m)'; ybest = y; end
    end
end
fprintf('Optimum = %g\n', best); disp(xbest); disp(ybest);

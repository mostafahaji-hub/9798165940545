%% Chapter 3 - three-level (transshipment) transportation, Example 3-4. Optimum 1700.
clc; clear;
a = [2 5; 4 3]; b = [6 4 8; 5 7 3]; s = [150 130]; q = [160 150]; d = [70 90 100];
[m,K] = size(a); n = size(b,2); nx = m*K; nv = nx + K*n;
cost = [reshape(a',[],1); reshape(b',[],1)];      % x11 x12 x21 x22 y11 y12 y13 y21 y22 y23
Aub = zeros(m+K, nv); bub = [s q]';
for i = 1:m, Aub(i, (i-1)*K+1:i*K) = 1; end            % plant supply
for k = 1:K, Aub(m+k, k:K:nx) = 1; end                  % DC capacity (inflow)
Aeq = zeros(K+n, nv); beq = [zeros(K,1); d'];
for k = 1:K, Aeq(k, k:K:nx) = 1; Aeq(k, nx+(k-1)*n+1:nx+k*n) = -1; end   % flow conservation
for j = 1:n, Aeq(K+j, nx+j:n:nv) = 1; end               % retailer demand
[v, z] = linprog(cost, Aub, bub, Aeq, beq, zeros(nv,1), [], optimoptions('linprog','Display','none'));
fprintf('Optimum = %g\n', z); disp(reshape(v(1:nx), K, m)'); disp(reshape(v(nx+1:end), n, K)');

%% Chapter 6 - nearest neighbour, savings and 2-opt on the 8-shop reference TSP (optimum 312)
clc; clear;
D = [0 39 34 48 58 52 40 41 41; 39 0 46 84 69 63 77 76 66; 34 46 0 75 25 85 67 41 22; 48 84 75 0 92 52 8 48 68; ...
     58 69 25 92 0 109 84 48 25; 52 63 85 52 109 0 51 84 92; 40 77 67 8 84 51 0 42 60; 41 76 41 48 48 84 42 0 24; 41 66 22 68 25 92 60 24 0];
n = size(D,1); tourlen = @(t) sum(D(sub2ind([n n], [1 t 1](1:end-1), [1 t 1](2:end))));
% nearest neighbour (node 1 = depot)
left = 2:n; cur = 1; t = [];
while ~isempty(left), [~, k] = min(D(cur, left)); cur = left(k); t(end+1) = cur; left(k) = []; end
fprintf('NN: %s  length %d\n', mat2str(t-1), tourlen(t));
% 2-opt (best improvement)
improved = true; cyc = [1 t 1];
while improved
    improved = false; best = 0;
    for i = 1:numel(cyc)-3
        for j = i+2:numel(cyc)-1
            d = D(cyc(i),cyc(j)) + D(cyc(i+1),cyc(j+1)) - D(cyc(i),cyc(i+1)) - D(cyc(j),cyc(j+1));
            if d < best, best = d; bi = i; bj = j; end
        end
    end
    if best < 0, cyc(bi+1:bj) = cyc(bj:-1:bi+1); improved = true; end
end
fprintf('NN + 2-opt: %s  length %d\n', mat2str(cyc(2:end-1)-1), tourlen(cyc(2:end-1)));

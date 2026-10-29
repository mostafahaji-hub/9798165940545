%% Chapter 2 - greedy constructive heuristics for the fixed-charge transportation problem (reference instance)
clc; clear;
c = [3 3 2 8; 6 7 4 4; 6 5 3 2]; f = [250 350 100 200; 300 250 150 100; 400 350 400 400];
s = [180 120 140]; d = [60 140 100 80];
keys = {c, 'unit cost c'; f, 'fixed cost f'; c + f./min(s', d), 'c + f/min(s,d)'; c + f./s', 'c + f/s_i'; c + f./d, 'c + f/d_j'};
for k = 1:size(keys,1)
    x = greedy(keys{k,1}, s, d); z = sum(sum(c.*x)) + sum(f(x>0));
    fprintf('%-16s cost = %d  RPD = %.1f%%\n', keys{k,2}, z, (z-2200)/2200*100);
end
function x = greedy(K, s, d)
    [~, idx] = sort(K(:)); x = zeros(size(K)); rs = s; rd = d;
    for q = idx'
        [i, j] = ind2sub(size(K), q); a = min(rs(i), rd(j)); x(i,j) = a; rs(i) = rs(i) - a; rd(j) = rd(j) - a;
    end
end

%% Chapter 5 - North-west corner, least cost (dummy last) and VAM on the reference tableau (balanced with dummy column)
clc; clear;
C = [3 3 2 8 0; 6 7 4 4 0; 6 5 3 2 0]; S = [180 120 140]; D = [60 140 100 80 60];
fprintf('NWC  cost = %d\n', sum(sum(C .* nwc(S, D))));
fprintf('LC   cost = %d\n', sum(sum(C .* leastcost(C, S, D, 5))));
fprintf('VAM  cost = %d\n', sum(sum(C .* vam(C, S, D))));
function x = nwc(S, D)
    x = zeros(numel(S), numel(D)); i = 1; j = 1;
    while i <= numel(S) && j <= numel(D)
        q = min(S(i), D(j)); x(i,j) = q; S(i) = S(i)-q; D(j) = D(j)-q;
        if S(i) == 0 && i < numel(S), i = i+1; elseif D(j) == 0, j = j+1; else, i = i+1; end
    end
end
function x = leastcost(C, S, D, dummy)
    x = zeros(size(C)); act = true(size(C)); act(:, dummy) = false;
    while any(act(:))
        c = C; c(~act) = inf; [~, k] = min(c(:)); [i, j] = ind2sub(size(C), k);
        q = min(S(i), D(j)); x(i,j) = q; S(i) = S(i)-q; D(j) = D(j)-q;
        if S(i) == 0, act(i,:) = false; end
        if D(j) == 0, act(:,j) = false; end
    end
    for i = 1:numel(S), x(i, dummy) = S(i); end
end
function x = vam(C, S, D)
    [m, n] = size(C); x = zeros(m, n); rows = true(1,m); cols = true(1,n);
    while any(rows) && any(cols)
        pr = -inf(1,m); pc = -inf(1,n);
        for i = find(rows), v = sort(C(i, cols)); pr(i) = v(min(2,end)) - v(1)*(numel(v)>1); end
        for j = find(cols), v = sort(C(rows, j)); pc(j) = v(min(2,end)) - v(1)*(numel(v)>1); end
        [prm, i] = max(pr); [pcm, j] = max(pc);
        if prm >= pcm, c = C(i,:); c(~cols) = inf; [~, j] = min(c); else, c = C(:,j); c(~rows) = inf; [~, i] = min(c); end
        q = min(S(i), D(j)); x(i,j) = q; S(i) = S(i)-q; D(j) = D(j)-q;
        if S(i) == 0, rows(i) = false; end
        if D(j) == 0, cols(j) = false; end
    end
end

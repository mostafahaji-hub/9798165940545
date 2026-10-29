%% Chapter 9 - Keshtel Algorithm (textbook version) on a continuous test function
% Phase 1: lucky Keshtels attract the nearest neighbour and swirl (diagnostic point, then bisection rounds)
% Phase 2: unlucky Keshtels fly away, new ones land; Phase 3: the rest move toward the midpoint of two others.
clc; clear; rng(1);
f = @(x) sum(x.^2 - 10*cos(2*pi*x)) + 10*numel(x);      % Rastrigin (change to any function)
n = 2; lo = -5.12; hi = 5.12; budget = 3000;
M = 10; p1 = 0.2; p2 = 0.3; Smax = 8;
N1 = round(p1*M); N2 = round(p2*M);
P = lo + (hi-lo)*rand(M, n); Z = zeros(M,1); for i = 1:M, Z(i) = f(P(i,:)); end
evals = M; best = min(Z); hist = best;
clip = @(x) min(hi, max(lo, x));
while evals < budget
    [~, ord] = sort(Z); lucky = ord(1:N1); unlucky = ord(M-N2+1:M); rest = ord(N1+1:M-N2);
    for li = lucky'                                      % ---- Phase 1: attraction and swirling
        L = P(li,:); fL = Z(li); A = nearest(P, li, L); moves = 0;
        while moves < 10*Smax && evals < budget
            r = L - A; if all(abs(r) < 1e-12), r = 0.01*(hi-lo)*(2*rand(1,n)-1); end
            O = clip(L + r); fO = f(O); evals = evals + 1; moves = moves + 1;
            if fO < fL, L = O; fL = fO; P(li,:) = L; Z(li) = fL; A = nearest(P, li, L); continue; end   % slope
            moved = false;
            for s = 1:Smax                                % pit: bisection rounds
                rho = 0.5^s; u = randn(1,n); u = u/norm(u); j = randi(n); e = zeros(1,n); e(j) = sign(rand-0.5)*rho*sum(abs(r));
                C = [L + rho*r; L - rho*r; L + rho*norm(r)*u; L + e];
                for k = 1:4
                    c = clip(C(k,:)); fc = f(c); evals = evals + 1; moves = moves + 1;
                    if fc < fL, L = c; fL = fc; P(li,:) = L; Z(li) = fL; A = nearest(P, li, L); moved = true; break; end
                end
                if moved || evals >= budget, break; end
            end
            if ~moved, break; end                        % food consumed
        end
        best = min(best, fL);
    end
    for wi = unlucky'                                    % ---- Phase 2: fly away, new Keshtels land
        P(wi,:) = lo + (hi-lo)*rand(1,n); Z(wi) = f(P(wi,:)); evals = evals + 1;
    end
    for ri = rest'                                       % ---- Phase 3: hustle toward empty water
        gh = randperm(M); gh(gh == ri) = []; G = P(gh(1),:); H = P(gh(2),:);
        P(ri,:) = clip(P(ri,:) + rand*((G+H)/2 - P(ri,:))); Z(ri) = f(P(ri,:)); evals = evals + 1;
    end
    best = min([best; Z]); hist(end+1) = best; %#ok<SAGROW>
end
fprintf('Keshtel algorithm: best f = %.3e after %d evaluations\n', best, evals);
plot(hist, 'LineWidth', 2); xlabel('iteration'); ylabel('best f'); grid on;
function A = nearest(P, li, L)
    d = sum(abs(P - L), 2); d(li) = inf; [~, k] = min(d); A = P(k,:);
end

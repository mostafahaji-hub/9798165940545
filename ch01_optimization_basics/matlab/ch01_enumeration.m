%% Chapter 1 - complete enumeration for the single-machine earliness/tardiness problem
% Reference 6-order instance of company "Sahar" (verified optimum: A-C-B-D-E-F, Z = 53)
clc; clear;
names = 'ABCDEF';
p = [3 1 8 7 2 6]; d = [9 14 19 17 21 20]; alpha = [2 2 1 3 1 3]; beta = [5 3 2 4 3 3];
P = perms(1:6);                         % 720 permutations
Z = zeros(size(P,1),1);
for k = 1:size(P,1)
    Z(k) = ETcost(P(k,:), p, d, alpha, beta);
end
[Zbest, idx] = min(Z);
fprintf('Optimum: %s   Z = %d\n', names(P(idx,:)), Zbest);
[~, spt] = sort(p);  fprintf('SPT: %s  Z = %d\n', names(spt), ETcost(spt,p,d,alpha,beta));
[~, edd] = sort(d);  fprintf('EDD: %s  Z = %d\n', names(edd), ETcost(edd,p,d,alpha,beta));
histogram(Z,30); xlabel('Z'); ylabel('number of sequences'); title('All 720 sequences');

function z = ETcost(seq, p, d, alpha, beta)
    t = 0; z = 0;
    for j = seq
        t = t + p(j);
        z = z + alpha(j)*max(0, d(j)-t) + beta(j)*max(0, t-d(j));
    end
end

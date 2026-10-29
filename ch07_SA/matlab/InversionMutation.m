function Ans=InversionMutation(X)
K=numel(X);
i=sort(randsample(K,2));
X(i(1):i(2))= X(i(2):-1:i(1));
Ans=X;
end
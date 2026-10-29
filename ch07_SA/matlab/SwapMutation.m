function Ans=SwapMutation(X)
    K=numel(X);
    Point=randsample(1:K-1,1);
    temp=X(Point);
    X(Point)=X(Point+1);
    X(Point+1)=temp;
    Ans=X;
end
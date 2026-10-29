function Ans=DisplacementMutation(X)
K=numel(X);
Point=sort(randsample(2:K,2));
temp=X(Point(1):Point(2));
X1=X(1:Point(1)-1);
X2=[];
if(Point(2)~=K)
    X2=X(Point(2)+1:end);
end
Ans=[temp X1 X2];
end
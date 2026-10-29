function [Ans1,Ans2]=UniformCrossover(p1,p2)
n=numel(p1);
Mask=randsample(0:1,n,1);
Ans1=p1;
Ans2=p2;
for i=1:n
    if(Mask(i)==0)
        temp=Ans1(i);
        Ans1(i)=Ans2(i);
        Ans2(i)=temp;
    end
end 
end
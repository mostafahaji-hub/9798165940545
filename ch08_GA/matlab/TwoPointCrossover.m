function [Ans1,Ans2]=TwoPointCrossover(p1,p2)
n=numel(p1);
Point=sort(randsample(1:n-1,2));
Ans1=[p2(1:Point(1)) p1(Point(1)+1:Point(2)) p2(Point(2)+1:n)];
Ans2=[p1(1:Point(1)) p2(Point(1)+1:Point(2)) p1(Point(2)+1:n)]; 
end
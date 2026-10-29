clc;
clear all;
close all;

%% initialization

model=Model();

%Parameters
Maxit=50;
T0=50;
alpha=0.97;
w=1;

%Parameters
Sol.X=CreateRandomSolution(model);
Sol.Cost=Cost(Sol.X,model);
it=0;
BestSol=Sol;
BestCost=zeros(Maxit,1);
T=T0;
%% SA loop
   
while it<Maxit
    
        NewSol.X=Mutation(4,Sol.X);
        NewSol.Cost=Cost(NewSol.X,model);
       if (NewSol.Cost<=Sol.Cost)
           Sol=NewSol;
       else           
           delta=NewSol.Cost-Sol.Cost;           
           p=exp(-delta/T);
           h=rand;                     
           if(p<=h)
                  Sol=NewSol;                   
           end
       end
       
       if(Sol.Cost <=BestSol.Cost)
           BestSol=Sol;
       end
      it=it+1;
      
    % SA accepts both best and worst solutions (chaotic)
    %BestCost(it)=Sol.Cost;
    % SA accepts just bad solutions (convergent)
    BestCost(it)=BestSol.Cost;
    
    T=alpha*T;
    %w=w+1
    disp(['Iteration' num2str(it) ' : Best Cost =' num2str(BestCost(it))]);
end

%% Result
disp('=====================================')
plot(BestCost(:,1));
[GlobalBestCost,GlobalBestPosition]=min(BestCost);
BestSol
GlobalBestCost
GlobalBestPosition

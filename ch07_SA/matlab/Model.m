function model=Model()

%% indices for number of suppliers (i) and customers (j)
i=3;
j=4;

%% fix cost
f=[1000
   2000
   3000];     

%% supply capacity
a   =[1500 
      1500
      1500];  
  
%% demand
b   =[500 
      500
      500 
      500];      

%% transportation cost
cij =[5,6,7,3
      2,5,4,4
      9,8,1,6];  


%% creating the model in a structure
    
model.f=f;
model.a=a;
model.b=b;
model.cij=cij;
model.i=i;
model.j=j;

end
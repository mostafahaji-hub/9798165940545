function Ans=Mutation(Index,Sol)
switch(Index)
    case 1
    Ans=SwapMutation(Sol);
    case 2
    Ans=BigSwapMutation(Sol);
    case 3
    Ans=InversionMutation(Sol);
    case 4
    Ans=DisplacementMutation(Sol);
end
end

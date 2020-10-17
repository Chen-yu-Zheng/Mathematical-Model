function [pop] = Init(NP,Minimum,Maximum)
    pop = rand( NP,1) * (Maximum - Minimum) + Minimum;
end
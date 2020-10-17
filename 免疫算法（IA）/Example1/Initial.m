function [population] = Initial(NP,D,Maximum,Minimum)
    population = rand(NP,D) * (Maximum - Minimum) + Minimum;
end
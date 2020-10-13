function [population] = InitPopulation(InitNum, Minimum, Maximum)
    population = zeros(InitNum,1);
    for i = 1 : InitNum
        population(i,1) = Minimum + (Maximum -  Minimum)*rand;
    end
end
        
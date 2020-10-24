function [fit] = get_fitness(X)
    fit = sum(X.* X , 2);
end
function [fitness] = get_fitness(X)
    fitness = 3 * cos(X(:,1) .* X(:,2)) + X(:,1) + X(:,2) .* X(:,2);
end
    
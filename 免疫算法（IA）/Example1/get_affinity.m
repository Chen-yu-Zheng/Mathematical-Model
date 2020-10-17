function [affinity] = get_affinity(population)
    x = population(:,1);
    y = population(:,2);
    affinity = f(x,y);
end
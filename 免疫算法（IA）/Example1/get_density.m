function [density] = get_density(population,deta)
    r = size(population,1);
    distance = zeros(r,1);
    density = zeros(r,1);
    for i = 1 : r
        for j = 1 : r
            distance(j) = sum((population(i) - population(j)).^2).^0.5;
            if distance(j) < deta
                distance(j) = 1;
            else
                distance(j) = 0;
            end
        end
        density(i) = sum(distance) / r;
    end
    
                
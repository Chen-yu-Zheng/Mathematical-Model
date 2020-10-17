function density = get_density(pop, threshold)
    r = size(pop,1);
    density = zeros(r,1);
    distance = zeros(r,1);
    for np = 1 : r
        for i = 1 : r
            if abs(pop(np) - pop(i)) < threshold
                distance(i) = 1;
            else
                distance(i) = 0;
            end
            density(np) = sum(distance) / r;
        end
    end
end
function [newpop] = Variate(pop , P_variation)
    [m, n] = size(pop);
    newpop = pop;
    for i = 1:m
        for j = 1 : n
            if rand < P_variation
                if pop(i,j) == '1'
                    newpop(i,j) = '0';
                else
                    newpop(i,j) = '1';
                end
            end
        end
    end
end
                    
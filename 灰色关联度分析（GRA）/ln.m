function [lnp] = ln(p)
    [r,c] = size(p);
    lnp = zeros(r,c);
    for i = 1 : r
        for j = 1 : c
            if p(i,j) > 0
                lnp(i,j) = log(p(i,j));
            else
                lnp(i,j) = 0;
            end
        end
    end
end
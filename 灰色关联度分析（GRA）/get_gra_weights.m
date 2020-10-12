function [weights] = get_gra_weights(Z,rho)
    Y = max(Z);
    abs_Z_Y = abs( Z - repmat(Y, size(Z,1) , 1) );
    minimum = min(abs_Z_Y(:));
    maximum = max(abs_Z_Y(:));
    relations = (minimum + rho * maximum) ./ (abs_Z_Y + rho * maximum);
    weights = mean(relations);
    weights = weights / sum(weights);
end
    
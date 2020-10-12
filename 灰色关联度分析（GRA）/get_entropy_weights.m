function [weights] = get_entropy_weights(Z)
    r = size(Z,1);
    Z = Z ./ repmat( sum(Z) , r , 1 );
    weights =  - sum(Z .* ln(Z)) / log(r);
    weights = 1 - weights;
    weights = weights ./ sum(weights);
end
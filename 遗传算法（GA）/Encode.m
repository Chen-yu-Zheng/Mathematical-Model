function [binpool] = Encode(pool,Length,Minimum,Maximum)
    pool = (pool - Minimum)*(2^Length - 1) / (Maximum - Minimum);
    binpool = dec2bin(pool);
    binpool = num2str(binpool,'%023d');
end
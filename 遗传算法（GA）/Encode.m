function [binpool] = Encode(pool,Length,Minimum,Maximum)
    pool = (pool - Minimum)*(2^Length - 1) / (Maximum - Minimum);
    binpool = dec2bin(pool， Length);
end

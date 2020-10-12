function [x_positive] = min2max(x)
    x_positive = (max(x) - x) / (max(x) - min(x)) ;
end
    
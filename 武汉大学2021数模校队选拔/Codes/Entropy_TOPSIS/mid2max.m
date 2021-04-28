function [x_positive] = mid2max(x,best)
    M = max(abs(x - best));
    x_positive = 1 - abs(x - best) / M;
end
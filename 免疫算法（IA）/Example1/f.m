function [answer] = f(x,y)
    answer = 5 * sin(x .* y) + x.^2 + y.^2;
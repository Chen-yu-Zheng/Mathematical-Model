function [answer] = f(x)
    answer = exp(-(x - 0.1).^2) .* ((sin(5 .* pi .* (x .^ 0.75))).^6);
end
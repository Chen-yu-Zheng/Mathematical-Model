function [x_positive] = inter2max(x, infimum , supremum , minimum , maximum)
    x_positive = zeros(size(x,1) , 1);
    for i = 1 : size(x,1)
        if x(i) < infimum
            x_positive(i) = 1 - (infimum - x(i)) / (infimum - minimum);
        elseif x(i) >= infimum && x(i) <= supremum
            x_positive(i) = 1;
        else
            x_positive(i) = 1 - (x(i) - supremum) / (maximum - supremum);
        end
    end
end
            
function [x_positive] = inter2max(x, infimum , supremum , minimum , maximum)
    x_positive = zeros(size(x,1) , 1);
    for i = 1 : size(x,1)
        if x(i) <= minimum
            x_positive(i) = 0;
        elseif x(i) < infimum
            x_positive(i) = 1 - (infimum - x(i)) / (infimum - minimum);
        elseif x(i) <= supremum
            x_positive(i) = 1;
        elseif x(i) < maximum
            x_positive(i) = 1 - (x(i) - supremum) / (maximum - supremum);
        else
            x_positive(i) = 0;
        end
    end
end
            
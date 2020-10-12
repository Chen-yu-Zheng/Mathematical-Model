function [x_positive] = Positivation(x,type)
    if type == 1
        disp('min2max begin!');
        x_positive = min2max(x);
        disp('min2max end!');
        disp('--------------------------------------');
    elseif type == 2
        disp('mid2max begin!');
        best = input('Please input the best value:');
        x_positive = mid2max(x,best);
        disp('mid2max end!');
        disp('--------------------------------------');
    elseif type == 3
        disp('inter2max begin!');
        infimum = input('Please input the infimum of the best interver: ');
        supremum = input('Please input the supremum of the best interver: ');
        minimum = input('Please input the minimum value you can accept: ');
        maximum = input('Please input the maximum value you can accept: ');
        x_positive = inter2max(x,infimum,supremum,minimum,maximum);
        disp('inter2max end!');
        disp('--------------------------------------');
    else
        disp('Please examine your input.');
    end
end
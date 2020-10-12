%% Loda data
clear;clc;
load water_quality.mat
[r,c] = size(X);

%% Positivation & normalization

ifpositive = input('Do you need Positivzation? (0/1):');

if ifpositive ~= 1 && ifpositive ~=0
    disp('Error,Please examine your input.');
end

if ifpositive == 1
    
    columns = input('Please enter the columns you want to be positive, like [1,2,3]:');
    types = input('Please enter the type of transformation for the columns you have selected:(1:min2max,2:mid2max,inter2max):');
    for i = 1:size(columns,2)
        X(:,columns(i)) = Positivation(X(:,columns(i)) , types(i));
    end
end

%It depends on reality.
columns = input('Please enter the columns without positivation:');

for i = 1 : size(columns,2)
    X(:,columns(i)) = ( X(:,columns(i)) - min(X(:,columns(i))) ) / ( max(X(:,columns(i))) - min(X(:,columns(i))) );
end

disp('X_positivation: ');
disp(X);


%% Standardization

Z = X ./ repmat(sum(X .* X) .^ 0.5 , r ,1);
disp('Z = X_standard: ');
disp(Z);

%% Set weights vector

ifweight = input('Do you want to posit weights for each features?(0/1):');
if ifweight == 0
    weights = ones(1,c);
elseif ifweight == 1
    OK = 0;
    while OK == 0
        inputs = input('Please enter a weight vector for each feature:');
        if abs(sum(inputs)- 1) < 0.001 && size(inputs,2) == size(X,2) && size(inputs,1) == 1 && sum(inputs <= 0) == 0
            weights = inputs;
            OK = 1;
        else
            disp('Weights vector is wrong!');
        end
    end
else
    disp('Please examine the label you have input.');
end

%% Compute each vector's distance to best/worst vector

D_P = sum(((Z - repmat(max(Z) , r , 1)) .^ 2) .* repmat(weights , r , 1) , 2) .^ 0.5;
D_N = sum(((Z - repmat(min(Z) , r , 1)) .^ 2) .* repmat(weights , r , 1) , 2) .^ 0.5;
disp('Distance to the best vector:');
disp(D_P);
disp('Distance to the worst vector:');
disp(D_N);

%% Compute scores

scores = D_N ./ (D_P + D_N);
scores_stand = scores ./ sum(scores);
disp('scores_standard:');
disp(scores_stand);

%% sort scores

[scores_sorted , index] = sort(scores_stand , 'descend');
disp('scores_sorted:');
disp(scores_sorted);
disp('rank:')
disp(index);

%% Get result

disp(['The reiver ' num2str(index(1)) ' has the best water quality.']);
disp(['The reiver ' num2str(index(end)) ' has the worst water quality.']);

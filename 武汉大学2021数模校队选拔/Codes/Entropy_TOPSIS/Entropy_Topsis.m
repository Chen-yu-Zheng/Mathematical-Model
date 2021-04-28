%% Loda data
clear;clc;
load X.mat;
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

weights = get_entropy_weights(Z);
disp('Weights by entropy method:');
disp(weights);

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


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


%% Normalization

Z = X ./ repmat(mean(X) , r ,1);
disp('Z = X_standard: ');
disp(Z);

%% Set weights vector

weights = get_entropy_weights(Z);
disp('Weights by entropy method:');
disp(weights);

%% Compute scores by GRA Method

rho = input('Please enter rho for Dray Relation Analysis:');
Y = max(Z);
abs_Z_Y = abs(Z - repmat(Y , r , 1));
minimum = min(abs_Z_Y(:));
maximum = max(abs_Z_Y(:));
relations = (minimum + rho * maximum) ./ (abs_Z_Y + rho * maximum);
scores = sum(relations .* repmat(weights , r , 1),2);



%% sort scores

scores_stand = scores ./ sum(scores);
disp('scores_stand:');
disp(scores_stand);
[scores_sorted , index] = sort(scores_stand , 'descend');
disp('scores_sorted:');
disp(scores_sorted);
disp('rank:')
disp(index);

%% Get result

disp(['The reiver ' num2str(index(1)) ' has the best water quality.']);
disp(['The reiver ' num2str(index(end)) ' has the worst water quality.']);

%% Enter Discriminant Matrix
clear;clc;
A = input('Please enter a discriminant matrix:');
[row_num , column_num] = size(A);

%% Examine if it is discriminant matrix

ERROR = 0;

% columns munber = rows number = n
if row_num ~= column_num || row_num <= 1
    ERROR = 1;
end

% for all i,j --> a_ij > 0
if ERROR == 0
    n = row_num;
    if sum(sum(A <= 0)) > 0
        ERROR = 2;
    end
end

% The RI Table's max index is 15
if ERROR == 0
    if n > 15
        ERROR = 3;
    end
end

% for all i,j --> a_ij * a_ji = 1
if ERROR == 0
    if sum(sum(A' .* A ~= 1)) > 0
        ERROR = 4;
    end
end

% Uniform Examination
if ERROR == 0
    [V, D] = eig(A);
    max_eig = max(D(:));
    CI = ( max_eig - n) / (n - 1);
    RI=[0 0.00001 0.52 0.89 1.12 1.26 1.36 1.41 1.46 1.49 1.52 1.54 1.56 1.58 1.59];
    CR = CI / RI(n);
    if CR > 0.1
        ERROR = 5;
    end
end

%% Compute weights vector in 3 methods.

if ERROR == 0
    disp(['max-eig = ',num2str(max_eig)]);
    disp(['CR = ', num2str(CR) , '< 0.1']);
    
    %Method1 : Arithmetic mean
    disp('Method1: Arithmetic mean:')
    sum_A = sum(A);
    SUM_A = repmat(sum_A , n , 1);
    Stand_A = A ./ SUM_A;
    A1 = sum(Stand_A , 2) / n;
    disp('Result:');
    disp(A1);
    
    %Method2 : Geometric mean
    disp('Method2: Geometric mean:')
    prod_A = prod(A,2);
    prod_A_nroot = prod_A .^ (1/n);
    A2 = prod_A_nroot ./ sum(prod_A_nroot) ;
    disp('Result:');
    disp(A2);
    
    %Method3 : Max-eig
    disp('Method3: Max_eig:');
    [r,c] = find(D,1);
    A3 = V(:,c) ./ sum(V(:,c));
    disp('Result:');
    disp(A3);
    
    %Get average number
    disp('Take all aspects into consideration:');
    disp('Result:');
    disp( (A1 + A2 + A3) / 3);

% Throw  errors
elseif ERROR == 1
    disp("The discriminant matrix's rows number is not the same as columns number");

elseif ERROR == 2
    disp('Exists i,j; a_ij <= 0')

elseif ERROR == 3
    disp('n is too large to compute')

elseif ERROR == 4
    disp('Exists i,j; a_ij * a_ji != 1')
    
else
    disp('CR > 0.1, Failure to pass conformance test');
end

    
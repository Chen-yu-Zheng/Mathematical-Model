clc; clear;
x0 = [4.3,9.3,10.8,16.7,22.5,26.3,29,28.1,25.4,21.4,12.4,6.9];
x00 = [4.3,9.3,10.8,16.7,22.5,26.3,29,28.1,25.4,21.4,12.4,6.9];
n = size(x0, 2);
sigma = x0(2:end) ./ x00(1:end-1);
range = minmax(sigma);
% disp(range);
% disp(exp(2/(n+1)));
x1 = cumsum(x0);
z = zeros(1,12);
for i = 2 : n
    z(i) = 0.5 * ( x1(i) + x1(i-1));
end
B = [-z(2:end)' ones(n-1,1)];
Y = x0(2:end)';
u = B \ Y;
x0_1 = zeros(1,n);
x0_1(1) = x0(1);
for k = 1 : n - 1
    x0_1(k + 1) = (1 - exp(u(1)))*(x0(1)-u(2)/u(1))*exp(-u(1)*k);
end
disp(x0);
disp(x0_1);
pred = zeros(1,4);
for k = n : n+3
    pred(k - n + 1) = (1 - exp(u(1)))*(x0(1)-u(2)/u(1))*exp(-u(1)*k);
end
disp(pred);
all = [x0_1 pred];

figure(1);
plot(1:12,x0,'o',1:16,all,'r*');
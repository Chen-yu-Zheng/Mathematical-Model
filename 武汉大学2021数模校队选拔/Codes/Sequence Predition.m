%%
clc;clear;
load China.mat;
%%

indicators = {'Tertiary education enrollment rate(%)';'GPI(%)'; 'Education/GDP(%)';
    'Education system(rank)';'Science education(rank)'; 
    'Management schools(rank)'; 'Research and training services(rank)';
    'Internet access(rank)';'Teacher-student ratio(%)'; 'Papers(thousand)'; 
    'Patents(million)'; 'R&D Funding/GDP(%)';
    'Staff training(rank)'};

years = (2016:2025)';
years_new = (2026:2035)';
years_all = (2016:2035)';
%%
yt  = X(1:10,2);
n = size(yt,1);
alpha = 0.24;
st1(1,1) = (yt(1) + yt(2)) / 2;
st2(1,1) = (yt(1) + yt(2)) / 2;
for i = 2 : n
    st1(i,1) = alpha* yt(i) + (1 - alpha) * st1(i-1,1);
    st2(i,1) = alpha* st1(i,1) + (1 - alpha) * st2(i - 1,1);
end
at = 2 * st1 - st2;
bt = alpha / (1-alpha) * (st1 - st2);
yhat = at + bt;

loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2025);

figure(1);
X(11:20,2) = yhat_new;
plot(years, yt,'ro',years_new, yhat_new, '+');

%%
yt  = X(1:10,10);
n = size(yt,1);
alpha = 0.3;
st1(1,1) = (yt(1) + yt(2)) / 2;
st2(1,1) = (yt(1) + yt(2)) / 2;
for i = 2 : n
    st1(i,1) = alpha* yt(i) + (1 - alpha) * st1(i-1,1);
    st2(i,1) = alpha* st1(i,1) + (1 - alpha) * st2(i - 1,1);
end
at = 2 * st1 - st2;
bt = alpha / (1-alpha) * (st1 - st2);
yhat = at + bt;

loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020);

figure(1);
X(11:15,10) = yhat_new;
plot(years, yt,'ro',years_new, yhat_new, '+');

%%
yt  = X(1:10,11);
n = size(yt,1);
alpha = 0.2;
st1(1,1) = (yt(1) + yt(2)) / 2;
st2(1,1) = (yt(1) + yt(2)) / 2;
for i = 2 : n
    st1(i,1) = alpha* yt(i) + (1 - alpha) * st1(i-1,1);
    st2(i,1) = alpha* st1(i,1) + (1 - alpha) * st2(i - 1,1);
end
at = 2 * st1 - st2;
bt = alpha / (1-alpha) * (st1 - st2);
yhat = at + bt;

loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020);

figure(1);
X(11:15,11) = yhat_new;
plot(years, yt,'o',years_new, yhat_new, 'r*');

%%
yt  = X(1:10,12);
n = size(yt,1);
alpha = 0.28;
st1(1,1) = (yt(1) + yt(2)) / 2;
st2(1,1) = (yt(1) + yt(2)) / 2;
for i = 2 : n
    st1(i,1) = alpha* yt(i) + (1 - alpha) * st1(i-1,1);
    st2(i,1) = alpha* st1(i,1) + (1 - alpha) * st2(i - 1,1);
end
at = 2 * st1 - st2;
bt = alpha / (1-alpha) * (st1 - st2);
yhat = at + bt;

loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020);

figure(1);
X(11:15,12) = yhat_new;
plot(years, yt,'o',years_new, yhat_new, 'r*');



%%
yt  = X(1:10,2);
n = size(yt,1);
alpha = 0.35;
st0 = mean(yt(1:3));
st1(1,1) = alpha * yt(1) + (1 - alpha) * st0;
st2(1,1) = alpha * st1(1) + (1 - alpha) * st0;
st3(1,1) = alpha * st2(1) + (1 - alpha) * st0;

for i = 2 : n
    st1(i,1) = alpha * yt(i) + (1 - alpha) * st1(i-1);
    st2(i,1) = alpha * st1(i) + (1 - alpha) * st2(i-1);
    st3(i,1) = alpha * st2(i) + (1 - alpha) * st3(i-1);
end

at = 3*st1 - 3*st2 + st3;
bt = 0.5 * alpha /(1-alpha)^2 * ((6 - 5*alpha)*st1 - 2*(5 - 4*alpha)*st2 + (4 - 3*alpha)*st3);
ct = 0.5 *  alpha^2 / (1-alpha)^2 * (st1 - 2*st2 + st3);
yhat = at + bt + ct;
loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020) + ct(end) * ((years_new - 2020) .^2);
X(11:15,2) = yhat_new;
figure(5)
plot(years, yt,'o',years_new, yhat_new, 'r*');

%%
yt  = X(1:10,3);
n = size(yt,1);
alpha = 0.5;
st0 = mean(yt(1:3));
st1(1,1) = alpha * yt(1) + (1 - alpha) * st0;
st2(1,1) = alpha * st1(1) + (1 - alpha) * st0;
st3(1,1) = alpha * st2(1) + (1 - alpha) * st0;

for i = 2 : n
    st1(i,1) = alpha * yt(i) + (1 - alpha) * st1(i-1);
    st2(i,1) = alpha * st1(i) + (1 - alpha) * st2(i-1);
    st3(i,1) = alpha * st2(i) + (1 - alpha) * st3(i-1);
end

at = 3*st1 - 3*st2 + st3;
bt = 0.5 * alpha /(1-alpha)^2 * ((6 - 5*alpha)*st1 - 2*(5 - 4*alpha)*st2 + (4 - 3*alpha)*st3);
ct = 0.5 *  alpha^2 / (1-alpha)^2 * (st1 - 2*st2 + st3);
yhat = at + bt + ct;
loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020) + ct(end) * ((years_new - 2020) .^2);
X(11:15,3) = yhat_new;
figure(5)
plot(years, yt,'o',years_new, yhat_new, 'r*');

%%
yt  = X(1:10,4);
n = size(yt,1);
alpha = 0.58;
st0 = mean(yt(1:3));
st1(1,1) = alpha * yt(1) + (1 - alpha) * st0;
st2(1,1) = alpha * st1(1) + (1 - alpha) * st0;
st3(1,1) = alpha * st2(1) + (1 - alpha) * st0;

for i = 2 : n
    st1(i,1) = alpha * yt(i) + (1 - alpha) * st1(i-1);
    st2(i,1) = alpha * st1(i) + (1 - alpha) * st2(i-1);
    st3(i,1) = alpha * st2(i) + (1 - alpha) * st3(i-1);
end

at = 3*st1 - 3*st2 + st3;
bt = 0.5 * alpha /(1-alpha)^2 * ((6 - 5*alpha)*st1 - 2*(5 - 4*alpha)*st2 + (4 - 3*alpha)*st3);
ct = 0.5 *  alpha^2 / (1-alpha)^2 * (st1 - 2*st2 + st3);
yhat = at + bt + ct;
loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020) + ct(end) * ((years_new - 2020) .^2);
X(11:15,4) = yhat_new;
figure(5)
plot(years, yt,'o',years_new, yhat_new, 'r*');

%%
yt  = X(1:10,5);
n = size(yt,1);
alpha = 0.58;
st0 = mean(yt(1:3));
st1(1,1) = alpha * yt(1) + (1 - alpha) * st0;
st2(1,1) = alpha * st1(1) + (1 - alpha) * st0;
st3(1,1) = alpha * st2(1) + (1 - alpha) * st0;

for i = 2 : n
    st1(i,1) = alpha * yt(i) + (1 - alpha) * st1(i-1);
    st2(i,1) = alpha * st1(i) + (1 - alpha) * st2(i-1);
    st3(i,1) = alpha * st2(i) + (1 - alpha) * st3(i-1);
end

at = 3*st1 - 3*st2 + st3;
bt = 0.5 * alpha /(1-alpha)^2 * ((6 - 5*alpha)*st1 - 2*(5 - 4*alpha)*st2 + (4 - 3*alpha)*st3);
ct = 0.5 *  alpha^2 / (1-alpha)^2 * (st1 - 2*st2 + st3);
yhat = at + bt + ct;
loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020) + ct(end) * ((years_new - 2020) .^2);
X(11:15,5) = yhat_new;
figure(5)
plot(years, yt,'o',years_new, yhat_new, 'r*');

%%
yt  = X(1:10,8);
n = size(yt,1);
alpha = 0.31;
st0 = mean(yt(1:3));
st1(1,1) = alpha * yt(1) + (1 - alpha) * st0;
st2(1,1) = alpha * st1(1) + (1 - alpha) * st0;
st3(1,1) = alpha * st2(1) + (1 - alpha) * st0;

for i = 2 : n
    st1(i,1) = alpha * yt(i) + (1 - alpha) * st1(i-1);
    st2(i,1) = alpha * st1(i) + (1 - alpha) * st2(i-1);
    st3(i,1) = alpha * st2(i) + (1 - alpha) * st3(i-1);
end

at = 3*st1 - 3*st2 + st3;
bt = 0.5 * alpha /(1-alpha)^2 * ((6 - 5*alpha)*st1 - 2*(5 - 4*alpha)*st2 + (4 - 3*alpha)*st3);
ct = 0.5 *  alpha^2 / (1-alpha)^2 * (st1 - 2*st2 + st3);
yhat = at + bt + ct;
loss = sum((yhat - yt) .^2)^0.5;
disp(loss);

yhat_new = at(end) + bt(end)*  (years_new - 2020) + ct(end) * ((years_new - 2020) .^2);
X(11:15,8) = yhat_new;
figure(5)
plot(years, yt,'o',years_new, yhat_new, 'r*');


%%
years = 2011 : 2020;
figure(12);
for i = 1 : 12
    subplot(3,4,i);
    pp = csape(years_all, X(:,i));
    pred = fnval(pp,2011:0.1:2025);
    plot(2011:0.1:2025,pred, years, X(1:10,i), 'ro', years_new, X(11:15,i),'*');
    grid('on');
    xlabel('Year');
    ylabel(indicators{i})
%     xlim([2007 2026]);
end
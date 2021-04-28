%clear;clc;
%load DATA/98.mat

Minimum = min(X(:,1));
Maximum = max(X(:,1));
disp(Minimum);
disp(Maximum);
t = Minimum:Maximum;

pp1 = csape(X(:,1), X(:,2));
y1 = fnval(pp1, t);
figure(1);
plot(X(:,1), X(:,2), 'o');
hold on;
plot(t, y1, 'r-','LineWidth',2);
legend('Row data','Interpolation');
xlabel('t');
ylabel('longitude');
title('longitude-t');

pp2 = csape(X(:,1), X(:,3));
y2 = fnval(pp2, t);
figure(2);
plot(X(:,1), X(:,3), 'o');
hold on;
plot(t, y2, 'r-','LineWidth',2);
legend('Row data','Interpolation');
xlabel('t');
ylabel('latitude');
title('latitude-t');


figure(3);
plot(X(:,2), X(:,3), 'o');
hold on;
plot(y1, y2, 'r-','LineWidth',2);
legend('Row data','Interpolation');
xlabel('longitude');
ylabel('latitude');
title('latitude-longitude');

Y = [t',y1',y2'];
xlswrite('qs1/re1.xlsx', Y);
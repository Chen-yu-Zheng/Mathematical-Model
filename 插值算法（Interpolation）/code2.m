clear;clc;
load data.mat

week = data(1,:);
new_week = 1:0.1:15;

new_data = zeros(size(data,1)-1,size(new_week,2));

figure(1);
for i = 2 : size(data,1)
    pred = spline(week,data(i,:),new_week);
    new_data(i-1,:) = pred;
    subplot(4,3,i-1);
    plot(week,data(i,:),'o',new_week,pred,'r');
end
legend('row data','new data','Location','SouthEast');
new_data = [1:0.1:15 ; new_data];
    
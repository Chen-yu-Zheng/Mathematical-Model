clear;clc;
load population.mat

year = population(:,1);
population = population(:,2);
new_year = 2019:2021;

prediction1 = pchip(year,population,new_year);
prediction2 = spline(year,population,new_year);

figure(1)
plot(year,population,'o',new_year,prediction1,'r*-',new_year,prediction2,'bx-')
%%
clear;clc;

PopNum = 100; %种群个体数
Minimum = 0; %搜索下界
Maximum = 1; %搜索上界
Iternum = 100; %最大迭代次数
Length = 17; %precise:1e-5 %数码长度
P_cross = 0.7; %杂交率
P_variation = 0.005; %变异率


population = InitPopulation(PopNum, Minimum, Maximum);

x = 0:0.01:1;
y = f(x);
figure(1);
fignum = 1;

hold on;

subplot(3,4,fignum);
fignum = fignum + 1;
plot(x,y, population , f(population), 'ro');
xlabel('x');
ylabel('f(x)');
title('Initial');

%%


for epoch = 1:Iternum
    evaluation = Evaluate(population);
    pool = Select(population , PopNum , evaluation);
    binpool = Encode(pool , Length , Minimum , Maximum);
    newpop = Cross(binpool, PopNum , P_cross , Length);
    newpop = Variate(newpop, P_variation);
    newpop = Decode(newpop, Minimum , Maximum , Length);
    population = newpop;
    
    if mod(epoch , 10) == 0
        subplot(3,4,fignum)
        plot(x,y,population, f(population),'ro');
        xlabel('x');
        ylabel('f(x)');
        title(['epoch = ' num2str(epoch)]);
        fignum = fignum + 1;
    end
    
end

subplot(3,4,fignum);
plot(x,y,population, f(population),'ro');
xlabel('x');
ylabel('f(x)');
legend('Function','Population','location','southeast');
title('End');
hold off;



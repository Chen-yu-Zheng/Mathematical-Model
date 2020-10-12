%%
clear;clc;

PopNum = 100; %��Ⱥ������
Minimum = 0; %�����½�
Maximum = 31; %�����Ͻ�
Iternum = 100; %����������
Length = 23; %precise:1e-5 %���볤��
P_select = 0.7; %ѡ����
P_cross = 0.7; %�ӽ���
P_variation = 0.008; %������


population = InitPopulation(PopNum, Minimum, Maximum);

x = 1:0.1:31;
y = f(x);
figure(1);
fignum = 1;

hold on;

subplot(3,4,fignum);
fignum = fignum + 1;
plot(x,y,population, f(population),'ro');
xlabel('x');
ylabel('f(x)');
title('Initial');

%%


for epoch = 1:Iternum
    evaluation = Evaluate(population);
    pool = Select(population , PopNum , evaluation);
    binpool = Encode(pool , Length , Minimum , Maximum);
    newpop = Cross(binpool, PopNum , P_cross , Length);
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



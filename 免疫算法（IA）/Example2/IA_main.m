clear;clc;

NP = 100; %抗体数量
Maximum = 1; %x最大值
Minimum = 0; %x最小值
Maxiter = 100; %最大迭代次数
P_select = 0.5; %免疫选择率
P_variation = 0.1; %变异率
alpha = 1; %激励函数系数1
belta = 1; %激励函数系数2
threshold = 0.1; %相似度阈值
Ncl = 20; %复制大小
deta0 = Maximum; %邻域范围初值

pop = Init(NP,Minimum,Maximum);

x = 0:0.01:1;
y = f(x);

figure(1);
subplot(3,4,1);
plot(x,y,pop, f(pop), 'ro');
xlabel('x');
ylabel('y');

hold on;

pop_affinity = get_affinity(pop);
pop_density = get_density(pop, threshold);
pop_active = get_active(pop_affinity, pop_density, alpha, belta);
[pop_active_sort, index] = sort(pop_active, 'descend');
pop_sort = pop(index);

fignum = 2;
for gen = 1 : Maxiter
    pop_a = zeros(NP * P_select,1);
    pop_b = zeros(NP * (1-P_select) , 1);
    for i = 1 :size(pop_a,1)
        a = pop_sort(i);
        a_clone = repmat(a,Ncl,1);
        
        deta = deta0 / gen;
        for ii = 1 : Ncl
            if rand < P_variation
                a_clone(ii) = a_clone(ii) + (rand - 0.5) * deta;
            end
            
            if (a_clone(ii) < Minimum) || (a_clone(ii) > Maximum)
                a_clone(ii) = rand * (Maximum - Minimum) + Minimum;
            end
        end
        a_clone(1) = pop_sort(i);
        a_clone_affinity = get_affinity(a_clone);
        [a_clone_affinity_sort,index] = sort(a_clone_affinity, 'descend');
        pop_a(i) = a_clone(index(1));
    end
    
    pop_b = rand( size(pop_b,1),1 ) * (Maximum - Minimum) + Minimum;
    
    pop_new = [pop_a; pop_b];
    pop_new_affinity = get_affinity(pop_new);
    pop_new_density = get_density(pop_new, threshold);
    pop_new_active = get_active(pop_new_affinity, pop_new_density, alpha, belta);
    [pop_new_active_sort, index] = sort(pop_new_active, 'descend');
    pop_sort = pop_new(index);
    
    if mod(gen,10) == 0
        subplot(3,4,fignum);
        plot(x,y,pop_sort, f(pop_sort),'ro');
        title(['gen = ' num2str(gen)]);
        xlabel('x');
        ylabel('y');
        fignum = fignum + 1;
    end
    
end

subplot(3,4,12)
plot(x,y,pop_sort, f(pop_sort),'ro');
title('End');
xlabel('x');
ylabel('y');
legend('function','IA');
hold off;


    
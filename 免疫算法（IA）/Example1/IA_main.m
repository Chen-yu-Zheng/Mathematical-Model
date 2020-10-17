clear; clc;

x = (-4 : 0.02 : 4);
y = (-4 : 0.02 : 4);

z = zeros(size(x,2), size(y,2));

for i = 1 : size(z,1)
    for j = 1 : size(z,2)
        z(i,j) = f(x(i), y(j));
    end
end



NP = 50; %免疫个体个数
Maximum = 4; %取值上限
Minimum = -4; %取值下限
Dim = 2; %维度
MaxIter = 500; %最大迭代次数
P_select = 0.5; %免疫选择比例
P_variation = 0.1; %变异概率
alpha = 2; %激励度系数1
belta = 1; %激励度系数2
threshold = 0.2; %相似度阈值
Ncl = 5; %克隆个数
deta0 = 0.5 * Maximum; %邻域范围初值

population = Initial(NP,Dim,Maximum,Minimum);

figure(1);
subplot(2,3,1);
mesh(x,y,z);
plot3(population(:,1),population(:,2),get_affinity(population),'ro');
xlabel('x');
ylabel('y');
zlabel('f(x,y)');
title('Initial');


hold on;

fignum = 2;

affinity = get_affinity(population);
density = get_density(population, threshold);
active = get_active(affinity, density, alpha, belta);
[active_sort, index] = sort(active, 'descend');
pop_sort = population(index , :);

pop_a = zeros(NP*P_select,Dim);
pop_b = zeros(NP*(1-P_select), Dim);

for gen = 1 : MaxIter
    for i = 1 : NP * P_select
        a = pop_sort(i,:);
        a_clone = repmat(a,Ncl,1);
        deta = deta0 / gen;
        
        for ii = 1 : Ncl
            for j = 1 : Dim
                if rand < P_variation
                    a_clone(ii, j) = a_clone(ii,j) + (rand - 0.5) * deta;
                end
                
                if (a_clone(ii,j) < Minimum) || (a_clone(ii,j) > Maximum)
                    a_clone(ii,j) = rand*(Maximum - Minimum) + Minimum;
                end
            end
        end
        
        a_clone(1,:) = pop_sort(i,:);
        a_clone_affinity = get_affinity(a_clone);
        [a_clone_affinity_sort, index] = sort(a_clone_affinity, 'descend');
        pop_a(i) = a_clone(index(1));
    end
    
    pop_b = rand(NP*(1 - P_select),Dim) * (Maximum - Minimum) + Minimum;
    pop_new = [pop_a; pop_b];
    pop_new_affinity = get_affinity(pop_new);
    pop_new_density = get_density(pop_new, threshold);
    pop_new_active = get_active(pop_new_affinity, pop_new_density, alpha, belta);
    [pop_new_active_sort ,index] = sort(pop_new_active, 'descend');
    pop_sort = pop_new(index,:);
    
    if mod(gen,100) == 0
        subplot(2,3,fignum);
        mesh(x,y,z);
        plot3(pop_sort(:,1),pop_sort(:,2),get_affinity(pop_sort),'ro');
        xlabel('x');
        ylabel('y');
        zlabel('f(x,y)');
        title(['gen = ' num2str(gen)]);
        fignum = fignum + 1;
    end
    
end

best = pop_sort(1,:);
disp('best:')
disp(['x = ' ,num2str(best(1)) , ', y = ' , num2str(best(2))])
disp(f(best(1),best(2)));

legend('IA');
hold off;

        

    





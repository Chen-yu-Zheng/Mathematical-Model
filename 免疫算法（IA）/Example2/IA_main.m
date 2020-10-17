clear;clc;

NP = 100; %��������
Maximum = 1; %x���ֵ
Minimum = 0; %x��Сֵ
Maxiter = 100; %����������
P_select = 0.5; %����ѡ����
P_variation = 0.1; %������
alpha = 1; %��������ϵ��1
belta = 1; %��������ϵ��2
threshold = 0.1; %���ƶ���ֵ
Ncl = 20; %���ƴ�С
deta0 = Maximum; %����Χ��ֵ

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


    
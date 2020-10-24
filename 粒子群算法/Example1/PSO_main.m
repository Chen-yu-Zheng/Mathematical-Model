%%Prepare
clear;clc;

%%Set Parameters
N = 100;
Dim = 10;
w = 0.9;
c1 = 2;
c2 = 2;
v_max = 10;
v_min = 10;
Gen_max =  200;
x_max = 20;
x_min = -20;

%%Initial Group's indivisual and v
group = rand(N, Dim)*(x_max - x_min) + x_min;
v = rand(N,Dim)*(v_max - v_min) + v_min;

%%Initial p_best
pos = group; %每个个体的最好位置
P_best =  get_fitness(pos); %每个个体的最好值

%%Initial G_best
[P_best_sort, index] = sort(P_best);
G_best = P_best_sort(1); %全局最好值
G = pos( index(1) , :); %全局最好位置
G_history = zeros(Gen_max , 1);


%%Train
for epoch = 1 : Gen_max
    
    for i = 1 : N
        
        if get_fitness(group(i,:)) < P_best(i)
            P_best(i) = get_fitness(group(i,:));
            pos(i,:) = group(i,:);
        end
        
        if P_best(i) < G_best
            G_best = P_best(i);
            G = pos(i,:);
        end
        
        v(i,:) = w .* v(i,:) + c1 * rand * (pos(i,:) - group(i,:)) + c2 * rand * ( G - group(i,:));
        group(i,:) = group(i,:) + v(i,:);
        
        for j = 1 : Dim
            if (v(i,j) > v_max || v(i,j) < v_min)
                v(i,j) = rand * (v_max - v_min) + v_min;
            end
            if (group(i,j) > x_max || group(i,j) < x_min)
                group(i,j) = rand * (x_max - x_min) + x_min;
            end
        end
    end
    G_history(epoch) = G_best;
end

%%Show result
disp(G);
disp(G_best);
figure(1)
plot( G_history, 'r*-');
title('Fitness History');
xlabel('epoch');
ylabel('fitness');

        

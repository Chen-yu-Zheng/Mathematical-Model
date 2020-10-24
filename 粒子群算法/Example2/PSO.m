clear; clc;

x = -4 : 0.01 : 4;
y = -4 : 0.01 : 4;
z = zeros( size(x,2));
for i = 1 : size(z,1)
    for j = 1 : size(z,2)
        z(i,j) = 3 * cos(x(i) * y(j)) + x(i)+  y(j)^2;
    end
end
figure(1)
mesh(x,y,z);
title('Function');
xlabel('x');
ylabel('y');
zlabel('z');

N = 100;
Dim = 2;
Gen_max = 200;
c1 = 2;
c2 = 2;
w_max = 1.1;
w_min = 0.2;
v_max = 1;
v_min = -1;
x_max = 4;
x_min = -4;

x = rand(N, Dim) * (x_max - x_min) + x_min;
v = rand(N, Dim) * (v_max - v_min) + v_min;

pos_best = x;
pos_best_value = get_fitness(pos_best);

[pos_best_sort , index] = sort(pos_best_value);
group_best_value = pos_best_sort(1);
group_best = pos_best( index(1));

group_best_history =  zeros( Gen_max, 1);

for epoch = 1 : Gen_max
    for i = 1 : N
        if get_fitness(x(i,:)) < pos_best_value(i)
            pos_best_value(i) = get_fitness(x(i,:));
            pos_best(i,:) = x(i,:);
        end
        
        if pos_best_value(i) < group_best_value
            group_best_value = pos_best_value(i);
            group_best = pos_best(i,:);
        end
        
        w = w_max - (w_max - w_min) * epoch / Gen_max;
        
        v(i,:) = w * v(i,:) + c1 * rand * (pos_best(i) - x(i,:)) + c2 * rand * (group_best - x(i,:));
        x(i,:) = x(i,:) + v(i,:);
        
        for j = 1 : Dim
            if (v(i,j) > v_max || v(i,j) < v_min)
                v(i,j) = rand* (v_max - v_min) + v_min;
            end
            if (x(i,j) > x_max || x(i,j) < x_min)
                v(i,j) = rand * (x_max - x_min) + x_min;
            end
        end
    end
    group_best_history(epoch) = group_best_value;
end

figure(2)
plot(group_best_history, 'r*-');
title('Group Best Fitness');
xlabel('epoch');
ylabel('fitness');


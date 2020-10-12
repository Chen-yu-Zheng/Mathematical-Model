function [pool] = Select(population, PopNum ,evaluation)
    sum_evaluation = sum(evaluation);
    table = cumsum(evaluation ./ sum_evaluation);
    pool = zeros( PopNum , 1);
    for i = 1: size(pool,1)
        flag = rand;
        bge = find(table >= flag);
        pool(i,1) = population( bge(1) , 1);
    end
end
        
    
    
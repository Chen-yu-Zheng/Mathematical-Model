function newpop = Cross(pool , PopNum, P_cross , Length)

newpop = pool;
    for i = 1:PopNum
        father = pool( ceil( size(pool , 1) * rand ) , :);
        mother = pool( ceil( size(pool , 1) * rand ) , :);
        if rand <= P_cross
            index = ceil( size(pool,2) * rand);
            for j = index : size(pool,2)
                temp = father(j);
                father(j) = mother(j);
                mother(j) = temp;
            end
        end
        newpop(i,:) = father;
    end
end
        
        
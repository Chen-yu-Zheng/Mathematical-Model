function [decpop] = Decode(binpop , Minimum , Maximum ,Length)
    decpop = zeros( size(binpop , 1) , 1);
    for i = 1 : Length
        decpop = decpop + str2num(binpop(:,i)) *( 2^(Length - i));
    end
    decpop = Minimum + decpop * (Maximum - Minimum) / (2^Length - 1);
end
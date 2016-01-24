function [ seq ] = GenerateStateCandidate(seq)
    n = size(seq,1);
    i = randi(n,1);
    j = randi(n, 1);
        
    if(i > j)
        seq(j:i) = flipud(seq(j:i));
    else
        seq(i:j) = flipud(seq(i:j));
    end

end

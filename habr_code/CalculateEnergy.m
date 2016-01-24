function [ E ] = CalculateEnergy(sequence, cities)

    n = size(sequence);
    E = 0;
    for i = 1:n-1
        E = E + Metric(cities(sequence(i),:), cities(sequence(i+1),:));
    end
    
    E = E + Metric(cities(sequence(end),:), cities(sequence(1),:));

end



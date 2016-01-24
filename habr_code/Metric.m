function [ distance ] = Metric( A, B )
    distance = (A - B).^2;
    distance = sqrt(distance);
    distance = sum(distance);
end


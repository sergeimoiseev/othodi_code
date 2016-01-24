function [ a ] = MakeTransit(probability )
    if(probability > 1 || probability < 0)
        error('Violation of argument constraint');
    end

    value = rand(1);

    if(value <= probability)
        a = 1;
    else
        a = 0; 
    end

end
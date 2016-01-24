function [ P ] = GetTransitionProbability( E, T )
P = exp(-E/T);
end


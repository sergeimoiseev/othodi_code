function [ state ] = SimulatedAnnealing( cities, initialTemperature, endTemperature)

    [n, z] = size(cities); % получаем размер вектора городов

    state = randperm(n)'; % задаём начальное состояние, как случайную перестановку городов
    currentEnergy = CalculateEnergy(state, cities); % вычисляем энергию для первого состояния
    T = initialTemperature;
    
    for k = 1:100000        

        stateCandidate = GenerateStateCandidate(state); % получаем состояние-кандидат
        candidateEnergy = CalculateEnergy(stateCandidate, cities); % вычисляем его энергию
        
        if(candidateEnergy < currentEnergy) % если кандидат обладает меньшей энергией
            currentEnergy = candidateEnergy; % то он переходит в текущее состояние
            state = stateCandidate;
        else
            p = GetTransitionProbability(candidateEnergy-currentEnergy, T); % иначе, считаем вероятность
            if (MakeTransit(p)) % и смотрим, осуществится ли переход
                currentEnergy = candidateEnergy;
                state = stateCandidate;
            end
        end;

        T = DecreaseTemperature(initialTemperature, k) ; % уменьшаем температуру
        
        if(T <= endTemperature) % условие выхода
            break;
        end;
    end

end


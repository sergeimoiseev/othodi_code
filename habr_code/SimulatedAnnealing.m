function [ state ] = SimulatedAnnealing( cities, initialTemperature, endTemperature)

    [n, z] = size(cities); % �������� ������ ������� �������

    state = randperm(n)'; % ����� ��������� ���������, ��� ��������� ������������ �������
    currentEnergy = CalculateEnergy(state, cities); % ��������� ������� ��� ������� ���������
    T = initialTemperature;
    
    for k = 1:100000        

        stateCandidate = GenerateStateCandidate(state); % �������� ���������-��������
        candidateEnergy = CalculateEnergy(stateCandidate, cities); % ��������� ��� �������
        
        if(candidateEnergy < currentEnergy) % ���� �������� �������� ������� ��������
            currentEnergy = candidateEnergy; % �� �� ��������� � ������� ���������
            state = stateCandidate;
        else
            p = GetTransitionProbability(candidateEnergy-currentEnergy, T); % �����, ������� �����������
            if (MakeTransit(p)) % � �������, ������������ �� �������
                currentEnergy = candidateEnergy;
                state = stateCandidate;
            end
        end;

        T = DecreaseTemperature(initialTemperature, k) ; % ��������� �����������
        
        if(T <= endTemperature) % ������� ������
            break;
        end;
    end

end


# -*- coding: utf-8 -*-
import time, math, random, sys, copy
import numpy as np
import habr_module as hm
import habr_plot as hp
from tools import setup_logging
# вектор городов
import logging.config, os, yaml, inspect
logger = logging.getLogger(__name__)


def simulated_annealing(cities, initialTemperature, endTemperature,num_of_loops):
# function [ state ] = SimulatedAnnealing( cities, initialTemperature, endTemperature)

#     n = size(cities,1); % получаем размер вектора городов
    n = len(cities)

#     state = randperm(n); % задаём начальное состояние, как случайный маршрут
#     % Функция randperm(n) - генерирует случайныую последовательность из целых чисел от 1 до n
    state = np.random.permutation(n)

#     currentEnergy = CalculateEnergy(state, cities); % вычисляем энергию для первого состояния
    currentEnergy = hm.calculate_energy(state, cities)
    logger.info("start_energy\n%s" % (currentEnergy,))
#     T = initialTemperature;
    T = initialTemperature
#     for i = 1:100000  %на всякий случай ограничеваем количество итераций
#     % может быть полезно при тестировании сложных функций изменения температуры T 
    i_last = 0     
    for i in range(1,num_of_loops+1):
    # for i in range(1,100000):
#         stateCandidate = GenerateStateCandidate(state); % получаем состояние-кандидат
        stateCandidate = hm.generate_state_candidate(state)
#         candidateEnergy = CalculateEnergy(stateCandidate, cities); % вычисляем его энергию
        candidateEnergy = hm.calculate_energy(stateCandidate,cities)
#         if(candidateEnergy < currentEnergy) % если кандидат обладает меньшей энергией
        if(candidateEnergy < currentEnergy):
#             currentEnergy = candidateEnergy; % то оно становится текущим состоянием
            currentEnergy = candidateEnergy
#             state = stateCandidate;
            state = stateCandidate
        else:
#         else
#             p = GetTransitionProbability(candidateEnergy-currentEnergy, T); % иначе, считаем вероятность
            p = hm.get_transition_probability(candidateEnergy-currentEnergy, T)
#             if (MakeTransit(p)) % и смотрим, осуществится ли переход
            if hm.make_transit(p):
#                 currentEnergy = candidateEnergy;
                currentEnergy = candidateEnergy
#                 state = stateCandidate;
                state = stateCandidate
        # print(currentEnergy)
#             end
#         end;
        T = hm.decrease_temperature(initialTemperature, i)
#         T = DecreaseTemperature(initialTemperature, i) ; % уменьшаем температуру

#         if(T <= endTemperature) % условие выхода
#             break;
        if T <= endTemperature:
            break
#         end;
        i_last = i
#     end

# end
    return state, i_last, T

def main():
    cities = hm.init_cities()

    initialTemperature = 4.
    endTemperature = 0.000001

    # num_of_loops=100000
    num_of_loops_list = [1000]
    # num_of_loops_list = [100,1000,10000,100000]
    for num_of_loops in num_of_loops_list:
        time_start = time.time()
        final_state, num_of_loops_really_made, final_temp = simulated_annealing(cities, initialTemperature, endTemperature, num_of_loops)
        time_finish = time.time()
        time_for_run = time_finish-time_start
        logger.info("time for run\n%s" % (time_for_run,))
        logger.info("num_of_loops_really_made\n%s" % (num_of_loops_really_made,))
        final_energy = hm.calculate_energy(final_state,cities)  
        logger.info("final_energy\n%s" % (final_energy,))
        logger.info("final_temp\n%s" % (final_temp,))
        text4plot = "%d_%.2f" % (num_of_loops_really_made, final_energy)
        hp.plot_route(final_state,cities,text4plot)
    return True

if __name__ == '__main__':
    setup_logging()
    main()
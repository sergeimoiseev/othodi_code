# -*- coding: utf-8 -*-
import time, math, random, sys, copy
# import tools
import numpy as np

def init_cities():
    cities_dtype = np.dtype([('lat', np.float64, 1),  ('lng', np.float64, 1)])
    cities = np.zeros(10,dtype=cities_dtype)
    for city in cities:
        city['lat'] = random.random()*10
        city['lng'] = random.random()*10
    return cities

def metric(A,B):
    sq_distance = (A['lat']-B['lat'])**2 + (A['lng']-B['lng'])**2
    distance = math.sqrt(sq_distance)
    return distance
# function [ distance ] = Metric( A, B )
#     distance = (A - B).^2;
#     distance = sqrt(distance);
#     distance = sum(distance);
# end


import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None) # b itterator is moved one step forward from initial position
    return itertools.izip(a, b)

def calculate_energy(sequence, cities):
    n = len(sequence)
    E = 0.
    for (i,ii) in pairwise(sequence):
        E = E + metric(cities[i],cities[ii])
    E = E + metric(cities[sequence[-1]],cities[sequence[0]])
    return E
# function [ E ] = CalculateEnergy(sequence, cities)
#     n = size(sequence);
#     E = 0;
#     for i = 1:n-1
#         E = E + Metric(cities(sequence(i),:), cities(sequence(i+1),:));
#     end
#     E = E + Metric(cities(sequence(end),:), cities(sequence(1),:));
# end

def generate_state_candidate(seq):
    n = len(seq)
    i = np.random.choice(n, 1)
    j = np.random.choice(n, 1)
    if i>j:
        # print(seq)
        part_to_flip = seq[j:i]
        seq[j:i] = part_to_flip[::-1]
        # print(seq)
    else:
        # print(seq)
        part_to_flip = seq[i:j]
        seq[i:j] = part_to_flip[::-1]
        # print(seq)
    return seq

# function [ seq ] = GenerateStateCandidate(seq)
#     n = size(seq,1);
#     i = randi(n,1);
#     j = randi(n, 1);
#     if(i > j)
#         seq(j:i) = flipud(seq(j:i));
#     else
#         seq(i:j) = flipud(seq(i:j));
#     end
# end


def get_transition_probability(E, T):
    P = math.exp(-E/T)
    return P
# function [ P ] = GetTransitionProbability( E, T )
# P = exp(-E/T);
# end

def make_transit(probability):
    if (probability > 1 or probability < 0):
        return None
    value = random.random()
    if value <= probability:
        a = 1
    else:
        a = 0
    return a

# function [ a ] = MakeTransit(probability )
#     if(probability > 1 || probability < 0)
#         error('Violation of argument constraint');
#     end
#     value = rand(1);
#     if(value <= probability)
#         a = 1;
#     else
#         a = 0; 
#     end
# end

def decrease_temperature(initialTemperature, k):
    T = initialTemperature * 0.1 / k
    return T

# function [ T ] = DecreaseTemperature( initialTemperature, k)
# T = initialTemperature * 0.1 / k; 
# end
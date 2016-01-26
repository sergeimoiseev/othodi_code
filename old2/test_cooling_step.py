import math
t_max = 100
# for T in range(t_max):
#     step = math.exp((alpha*(-T))/t_max)
#     print(T)
#     print(step)

alpha = 0.1
T=t_max
i = 0
while T>alpha:
    step = alpha*math.exp(((T-t_max)/t_max))
    T -= step
    i+=1
    print("\t%d" % i)
    print(T)
    print("step = %f" % step)

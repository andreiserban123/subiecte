import numpy as np


def fitness(x):
    n = len(x)
    counter = 0
    sum = 0
    for i in range(n):
        if x[i] == 1:
            counter += 1
        sum = sum + x[i] * i
    return counter >= 5, sum


def gen(dim):
    pop = []
    n = 9
    for i in range(dim):
        flag = False
        while flag == False:
            x = np.random.randint(0, 2, n)
            flag, f = fitness(x)
        x = list(x)
        x.append(f)
        pop.append(x)
    return pop


pop = gen(30)
pop = np.asarray(pop)

print()

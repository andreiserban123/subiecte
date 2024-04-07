import numpy as np


def fitness(x):
    counter = 0
    n = len(x)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if x[i] == j and x[j] == i:
                counter += 1
    return counter


def gen_pop(dim, n):
    pop = []
    for i in range(dim):
        x = np.random.permutation(n)
        x = list(x)
        f = fitness(x)
        x += [f]
        pop.append(x)
    return pop


def inserare(x):
    n = len(x)
    i = np.random.randint(0, n - 1)
    j = np.random.randint(i + 1, n)
    r = x.copy()
    r[i + 1] = x[j]
    if i + 1 < j:
        r[i + 2:j + 1] = x[i + 1:j]
    return r


def mutatie_populatie(pop, probabilitate_m):
    pop_m = pop.copy()
    dim = len(pop)
    n = len(pop[0])
    for i in range(dim):
        r = np.random.uniform(0, 1)
        if r <= probabilitate_m:
            x = pop[i][0:n].copy()
            x = inserare(x)
            f = fitness(x)
            x = list(x)
            x = x + [f]
            pop_m[i] = x.copy()
    return pop_m


pop = gen_pop(100, 5)
pop_m = mutatie_populatie(pop, 0.2)
print(pop_m)

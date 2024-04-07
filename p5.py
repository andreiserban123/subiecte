import numpy as np


def fitness(x):
    counter = 0
    for i in range(len(x)):
        counter += x[i]
    return counter


def gen_pop(dim):
    pop = []
    for i in range(dim):
        x = np.random.randint(0, 2, 7)
        f = fitness(x)
        x = list(x)
        x += [f]
        pop.append(x)
    return pop


def recombinare(pop, pc):
    pop_c = pop.copy()
    dim = len(pop)
    n = len(pop[0])
    for i in range(0, dim - 1, 2):
        if np.random.uniform(0, 1) < pc:
            points = np.random.choice(range(1, n - 1), 2, replace=False)
            p1, p2 = sorted(points)
            c1 = np.concatenate([pop_c[i][:p1], pop_c[i + 1][p1:p2], pop_c[i][p2:]])
            c2 = np.concatenate([pop_c[i + 1][:p1], pop_c[i][p1:p2], pop_c[i + 1][p2:]])
            pop_c[i], pop_c[i + 1] = c1, c2

            # Recalculate fitness
            pop_c[i][-1] = fitness(c1[:-1])
            pop_c[i + 1][-1] = fitness(c2[:-1])
    return pop_c


pop_size = 6  # Size of the population
pop = gen_pop(pop_size)  # Generate initial population
pop = np.asarray(pop)
pc = 0.7  # Crossover probability
new_pop = recombinare(pop, pc)
new_pop = np.asarray(new_pop)
print(new_pop)

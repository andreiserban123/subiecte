import math

import numpy

def fitness(indiv):
    x1 = indiv[0]
    x2 = indiv[1]
    x3 = indiv[2]
    x4 = indiv[3]
    return (1 + math.sin(2*x1 - x3) + (x2+ x4) ** 1/3)

def generare_populatie_initiala(dim):
    population = []
    for i in range(dim):
        indiv = []
        x1 = numpy.random.uniform(-1, 1)
        x2 = numpy.random.uniform(0, 0.2)
        x3 = numpy.random.uniform(0, 1)
        x4 = numpy.random.uniform(0, 5)
        indiv.append(x1)
        indiv.append(x2)
        indiv.append(x3)
        indiv.append(x4)
        fit = fitness(indiv)
        indiv.append(fit)
        population.append(indiv)
    return population

populatie_initiala = generare_populatie_initiala(10)
print(populatie_initiala)

def mutatie_fluaj(pop, pm, t=0.6):
    dim = len(pop)
    nr_gene = len(pop[0]) - 1
    next_gen = [indiv[:-1] for indiv in pop]
    for i in range(dim):
        for j in range(nr_gene):
            r = numpy.random.uniform(0,1)
            if r < pm:
                next_gen[i][j] += numpy.random.uniform(-t, t)
                if j == 0 and next_gen[i][j] < -1:
                    next_gen[i][j] = -1
                elif j == 0 and next_gen[i][j] > 1:
                    next_gen[i][j] = 1
                elif j == 1 and next_gen[i][j] < 0:
                    next_gen[i][j] = 0
                elif j == 1 and next_gen[i][j] > 0.2:
                    next_gen[i][j] = 0.2
                elif j == 2 and next_gen[i][j] < 0:
                    next_gen[i][j] = 0
                elif j == 2 and next_gen[i][j] > 1:
                    next_gen[i][j] = 1
                elif j == 3 and next_gen[i][j] < 0:
                    next_gen[i][j] = 0
                elif j == 3 and next_gen[i][j] > 5:
                    next_gen[i][j] = 5
    for i in range(dim):
        fit = fitness(next_gen[i])
        next_gen[i].append(fit)
    return next_gen

pop_mutatie = mutatie_fluaj(populatie_initiala, 0.2)
print(pop_mutatie)
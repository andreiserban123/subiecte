# Problema 7
import numpy


def fitness(indiv):  # de tip permutare
    counter = 0
    n = len(indiv)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if indiv[i] == indiv[j] and indiv[j] == indiv[i]:
                counter += 1
    return counter


def pop_permutari(dim, nr_gene):
    pop = []
    for i in range(dim):
        indiv = numpy.random.permutation(nr_gene)
        fit = fitness(indiv)
        indiv = list(indiv)
        indiv.append(fit)
        pop.append(indiv)
    return pop


def mutatie_permutari(pop, pm):
    popm = []
    for indiv in pop:
        if numpy.random.rand() < pm:
            n = len(indiv) - 1  # Excluzând valoarea de fitness
            i, j = numpy.random.choice(range(n), 2, replace=False)  # Alegem două poziții la întâmplare
            # Schimbăm genele
            indiv[i], indiv[j] = indiv[j], indiv[i]
            # Recalculăm fitness-ul după mutație
            fit = fitness(indiv[:-1])  # Apelăm fitness fără valoarea de fitness veche
            indiv[-1] = fit  # Actualizăm valoarea de fitness
        popm.append(indiv)
    return popm


pop_i_permutari = pop_permutari(20, 20)
print(numpy.asarray(pop_i_permutari))

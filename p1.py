import numpy

def fitness(indiv):
    nr_gene = len(indiv)
    fit = 0
    for i in range(nr_gene - 1):
        for j in range(i + 1, nr_gene):
            if indiv[i] == j and indiv[j] == i:
                fit += 1
    return fit

def generare_populatie_initiala(dim, nr_gene):
    pop = []
    for i in range(dim):
        indiv = numpy.random.permutation(nr_gene)
        indiv = list(indiv)
        indiv.append(fitness(indiv))
        pop.append(indiv)
    return pop

pop = generare_populatie_initiala(5, 5)
print(pop)

def mutatie_inserare(pop, pm):
    for i in range(len(pop)):
        if numpy.random.uniform(0, 1) < pm:
            n = len(pop[i]) - 1
            indexes = numpy.random.choice(range(n), size=2, replace=False)
            index1 = min(indexes)
            index2 = max(indexes)
            valEliminata = pop[i].pop(index2)
            pop[i].insert(index1+1, valEliminata)
            pop[i][-1] = fitness(pop[i][0:-1])
    return pop

pop2 = mutatie_inserare(pop, 0.8)
print(pop2)
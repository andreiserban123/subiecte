import numpy

#Individ fara fitness
def fitness(indiv):
    fit = 0
    for i in range(len(indiv) - 1):
        for j in range(i + 1, len(indiv)):
            if indiv[i] == j and indiv[j] == i:
                fit += 1
    return fit

def generare_populatie(dim, n):
    pop = []
    for i in range(dim):
        indiv = numpy.random.permutation(n)
        indiv = list(indiv)
        indiv.append(fitness(indiv))
        pop.append(indiv)
    return pop

pop = generare_populatie(5, 5)
print(pop)

def mutatie_amestec(pop, pm):
    popm = []
    for indiv in pop:
        n = len(indiv)
        if numpy.random.uniform(0, 1) < pm:
            index1, index2 = numpy.random.choice(range(n), 2, replace=False)
            indiv[index1], indiv[index2] = indiv[index2], indiv[index1]
            indiv[-1] = fitness(indiv[0:-1])
        popm.append(indiv)
    return popm

popm = mutatie_amestec(pop, 0.2)
print(popm)
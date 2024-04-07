import numpy


def dec_to_bin(n, m):
    val = bin(n)[2:].zfill(m)
    x = [int(val[i], 2) for i in range(m)]
    return x


def bin_to_dec(n, m):
    y = ''
    for i in range(m):
        y = y + str(n[i])
    return int(y, 2)


def fitness(x):
    return numpy.sin(x - 2) ** 2


def gen(dim):
    pop = []
    for i in range(dim):
        x = numpy.random.randint(1, 25001)
        val = dec_to_bin(x, 12)
        f = fitness(x)
        val += [f]
        pop.append(val)
    return pop


def fps(fitnessuri, dim):
    fps = numpy.zeros(dim)
    suma = numpy.sum(fitnessuri)
    for i in range(dim):
        fps[i] = fitnessuri[i] / suma
    qfps = fps.copy()
    for i in range(1, dim):
        qfps[i] = qfps[i - 1] + fps[i]
    return qfps  # return array()


def ruleta(pop_initiala, dim, n):
    pop_initiala = numpy.asarray(pop_initiala)
    parinti = pop_initiala.copy()
    fitnessuri = numpy.zeros(dim, dtype="float")
    for i in range(dim):
        fitnessuri[i] = pop_initiala[i][n]
    qfps = fps(fitnessuri, dim)
    for i in range(dim):
        r = numpy.random.uniform(0, 1)
        pozitie = numpy.where(qfps >= r)
        index_buzunar_ruleta = pozitie[0][0]
        parinti[i][0:n] = pop_initiala[index_buzunar_ruleta][0:n]
        parinti[i][n] = fitnessuri[index_buzunar_ruleta]
    return parinti


pop = gen(10)
parinti = ruleta(pop, 10, 12)
print(parinti)

import numpy


def turneu(pop_initiala, dim, n, k):
    parinti = pop_initiala.copy()
    fitnessuri = numpy.zeros(dim)
    for i in range(dim):
        fitnessuri[i] = pop_initiala[i][n]
    for i in range(dim):
        submultimePozitiiIndivizi = numpy.random.randint(0, dim, k)
        fitnessuriIndiviziSelectati = [fitnessuri[submultimePozitiiIndivizi[i]] for i in range(k)]
        fitnessIndividCastigator = max(fitnessuriIndiviziSelectati)
        pozMax = numpy.where(fitnessuriIndiviziSelectati == fitnessIndividCastigator)
        indexPozMax = pozMax[0][0]
        # index = corespondentul lui indexPozMax in pop_initiala
        index = submultimePozitiiIndivizi[indexPozMax]
        parinti[i][0:n] = pop_initiala[index][0:n]
        parinti[i][n] = fitnessuri[index]
    return parinti

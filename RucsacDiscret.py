import numpy


######################## CALCUL FUNCTIE FITNESS + FEZ ######################
def ok(x, n, c, v, cmax):
    fitness = 0
    cost = 0
    for i in range(n):
        fitness = fitness + x[i] * v[i]
        cost = cost + x[i] * c[i]
    return cost <= cmax, fitness


########################## GENERAREA UNEI POPULATII ########################
def gen(cmax, dim):
    c = numpy.genfromtxt("cost.txt")
    v = numpy.genfromtxt("valoare.txt")
    n = len(c)
    pop = []
    for i in range(dim):
        flag = False
        while flag == False:
            x = numpy.random.randint(0, 2, n)
            flag, fitness = ok(x, n, c, v, cmax)
        x = list(x)
        x = x + [fitness]
        pop = pop + [x]
    return pop, dim, n, c, v, cmax


########################### OPERATOR MUTATIE BINARA #########################
def m_binara(gena):
    gena_mutanta = not gena
    return int(gena_mutanta)  # cast pentru trecerea True/False in 1/0


########################## APLICARE MUTATIE POPULATIE #########################
def mutatie_populatie(pop, dim, n, c, v, cost_max, probabilitate_m):
    pop_m = pop.copy()
    for i in range(dim):
        x = pop[i][:n].copy()
        for j in range(n):
            r = numpy.random.uniform(0, 1)
            if r <= probabilitate_m:
                x[j] = m_binara(x[j])
        fez, val = ok(x, n, c, v, cost_max)
        if fez:
            x = list(x)
            x = x + [val]
            pop_m[i] = x.copy()
    return pop_m


'''
import RucsacDiscret
populatie,dim,n,c,v,cost_max = RucsacDiscret.gen(30, 10)
populatie_m = RucsacDiscret.mutatie_populatie(populatie, dim, n, c, v, cost_max, 0.1)
import numpy
populatie = numpy.asarray(populatie)
populatie_m = numpy.asarray(populatie_m)
'''


def crossover_unipunct(x1, x2, n):
    # genereaza aleator gena in care este facuta recombinarea
    p = numpy.random.randint(0, n)
    c1 = x1.copy()
    c2 = x2.copy()
    c1[0:p] = x1[0:p]
    c1[p:n] = x2[p:n]
    c2[0:p] = x2[0:p]
    c2[p:n] = x1[p:n]
    return c1, c2

def crossover_populatie(pop, dim, n, c, v, cmax, probabilitate_crossover):
    copii = pop.copy()
    # populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0, dim - 1, 2):
        # selecteaza parintii
        x1 = pop[i][0:n].copy()
        x2 = pop[i + 1][0:n].copy()
        r = numpy.random.uniform(0, 1)
        if r <= probabilitate_crossover:
            c1, c2 = crossover_unipunct(x1, x2, n)
            flag, fitness = ok(c1, n, c, v, cmax)
            if flag == True:
                c1 = list(c1)
                c1 = c1 + [fitness]
                copii[i] = c1.copy()
            flag, fitness = ok(c2, n, c, v, cmax)
            if flag == True:
                c2 = list(c2)
                c2 = c2 + [fitness]
                copii[i + 1] = c2.copy()
    return copii

"""
import RucsacDiscret
import numpy
populatie, dim, n, c, v, cmax = RucsacDiscret.gen(30, 10)
copii = RucsacDiscret.crossover_populatie(populatie, dim, n, c, v, cmax, 0.7)
populatie = numpy.asarray(populatie)
copii = numpy.asarray(copii)
"""

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


def SUS(pop_initiala, dim, n):
    pop_initiala = numpy.asarray(pop_initiala)
    parinti = pop_initiala.copy()  # gene si fitness-uri
    fitnessuri = numpy.zeros(dim, dtype="float")
    for i in range(dim):
        fitnessuri[i] = pop_initiala[i][n]
    qfps = fps(fitnessuri, dim)
    r = numpy.random.uniform(0, 1 / dim)
    k, i = 0, 0
    while k < dim:
        while r <= qfps[i]:
            parinti[k][0:n] = pop_initiala[i][0:n]
            parinti[k][n] = fitnessuri[i]
            r = r + 1 / dim
            k = k + 1
        i = i + 1
    return parinti


def SelectieParinti():
    pop_initiala, dim, n, c, v, cost_max = gen(50, 10)
    parinti = ruleta(pop_initiala, dim, n)
    pop_initiala = numpy.asarray(pop_initiala)
    parinti = numpy.asarray(parinti)
    return pop_initiala, parinti


'''
import RucsacDiscret
pop_initiala, parinti = RucsacDiscret.SelectieParinti()
'''


def elitism(pop_curenta, pop_mutanta, dim, n):
    pop_curenta = numpy.asarray(pop_curenta)
    pop_mutanta = numpy.asarray(pop_mutanta)
    pop_urmatoare = numpy.copy(pop_mutanta)

    max_curent = numpy.max(pop_curenta[:, -1])
    max_mutant = numpy.max(pop_mutanta[:, -1])

    if max_curent > max_mutant:
        poz = numpy.where(pop_curenta[:, -1] == max_curent)
        imax = poz[0][0]
        ir = numpy.random.randint(dim)
        pop_urmatoare[ir, 0:n] = pop_curenta[imax, 0:n].copy()
        pop_urmatoare[ir, n] = max_curent
    return pop_urmatoare


def SelectieGeneratieUrmatoare():
    pop_initiala1, dim, n, c, v, cost_max = gen(50, 10)
    pop_initiala2, dim, n, c, v, cost_max = gen(50, 10)
    pop_urm = elitism(pop_initiala1, pop_initiala2, dim, n)
    pop_initiala1 = numpy.asarray(pop_initiala1)
    pop_initiala2 = numpy.asarray(pop_initiala2)
    pop_urm = numpy.asarray(pop_urm)
    return pop_initiala1, pop_initiala2, pop_urm


'''
import RucsacDiscret
pop_initiala1, pop_initiala2, pop_urm = RucsacDiscret.SelectieGeneratieUrmatoare()
'''

def GA(cost_max, dim, NMAX, pc, pm):
    # generarea populatiei la momentul initial
    pop_initiala, dim, n, c, v, cost_max = gen(cost_max, dim)
    pop_initiala = numpy.asarray(pop_initiala)
    # in istoric_v pastram cel mai bun cost din populatia curenta, la fiecare moment al evolutiei
    istoric_v = [numpy.max(pop_initiala[:, -1])]
    # evolutia - cat timp
    #                - nu am depasit NMAX  si
    #                - populatia are macar 2 indivizi cu calitati diferite  si
    #                - in ultimele NMAX/4 iteratii s-a schimbat macar o data calitatea cea mai buna

    # initializari pentru GA
    it = 0  # contor pentru numarul de iteratii (generatii) parcurse
    gata = False  # flag pentru eventuala oprire a algoritmului daca este atinsa una dintre conditiile de oprire
    nrm = 1  # contor pentru numarul maxim de iteratii consecutive fara imbunatatirea celui mai bun individ

    while it < NMAX and not gata:
        parinti = ruleta(pop_initiala, dim, n)
        pop_copii = crossover_populatie(parinti, dim, n, c, v, cost_max, pc)
        pop_copii_mutanti = mutatie_populatie(pop_copii, dim, n, c, v, cost_max, pm)
        pop_urmatoare = elitism(pop_initiala, pop_copii_mutanti, dim, n)
        minim = numpy.min(pop_urmatoare[:, -1])
        maxim = numpy.max(pop_urmatoare[:, -1])
        # daca cel mai bun individ de acum e egal cu ultimul adaugat in lista cu cei mai buni
        if maxim == istoric_v[it]:
            nrm = nrm + 1  # inseamna ca nu s-a imbunatatit in generatia curenta, incrementam nr de iteratii consecutive fara imbunatatire
        else:
            nrm = 0  # la orice imbunatatire resetam contorul la zero

        # daca max=min (adica toti indivizii sunt identici calitativ) sau daca in ultimele nmax/4 iteratii consecutive nu s-a imbunatatit calitatea
        if maxim == minim or nrm == int(NMAX / 4):
            gata = True  # opresc algoritmul la aceasta generatie
        else:
            it = it + 1  # altfel, incrementez contorul de generatii pentru ca voi trece la urmatoarea daca nu am ajuns la ultima

        # salvez cel mai bun individ in istoric
        istoric_v.append(numpy.max(pop_urmatoare[:, -1]))

        # initializez populatia initiala de la urmatorul pas cu populatia urmatoare de la generatia curenta (gene si fitness)
        pop_initiala = pop_urmatoare.copy()
        # de aici algoritmul se reia de sus, de la while, pentru (eventuala) urmatoare generatie

    # la acest moment s-a iesit din while, deci algoritmul a luat sfarsit, ramane sa procesam datele obtinute
    # transformarea din lista in vector pentru a aplica functia where corect
    poz_max = numpy.where(pop_urmatoare[:, -1] == maxim)
    print(poz_max)
    individ_max_gene = pop_urmatoare[poz_max[0][0], 0:n]
    individ_max_fitness = maxim

    return numpy.asarray(individ_max_gene), individ_max_fitness

######################################## RULARE ##############################################
individ_max_gene, individ_max_fitness = GA(50, 200, 250, 0.8, 0.1)
print(numpy.asarray(individ_max_gene))
print(individ_max_fitness)
import numpy


######################## CALCUL FUNCTIE FITNESS ######################
def fitnessTSP(x, n, cost):
    fitness = 0
    for i in range(n - 1):
        fitness = fitness + cost[int(x[i])][int(x[i + 1])]
    fitness = fitness + cost[int(x[0])][int(x[n - 1])]
    return fitness


######################## GENERAREA UNEI POPULATII ####################
def gen(dim):
    c = numpy.genfromtxt("costuri_tsp.txt")
    n = len(c)
    pop = []
    for i in range(dim):
        x = numpy.random.permutation(n)
        fitness = fitnessTSP(x, n, c)
        x = list(x)
        x = x + [fitness]
        pop = pop + [x]
    return pop, dim, n, c


##################### OPERATOR MUTATIE INTERSCHIMBARE #################
def m_perm_interschimbare(x, n):
    poz = numpy.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = numpy.random.randint(0, n, 2)
    p1 = numpy.min(poz)
    p2 = numpy.max(poz)
    y = x.copy()
    y[p1] = x[p2]
    y[p2] = x[p1]
    return y


####################### APLICARE MUTATIE POPULATIE #####################
def mutatie_populatie(pop, dim, n, c, probabilitate_m):
    pop_m = pop.copy()
    for i in range(dim):
        r = numpy.random.uniform(0, 1)
        if r <= probabilitate_m:
            x = pop[i][0:n].copy()
            x = m_perm_interschimbare(x, n)
            fitness = fitnessTSP(x, n, c)
            x = list(x)
            x = x + [fitness]
            pop_m[i] = x.copy()
    return pop_m


'''
import TSP
populatie,dim,n,c = TSP.gen(10)
populatie_m = TSP.mutatie_populatie(populatie, dim, n, c, 0.2)
import numpy
populatie = numpy.asarray(populatie)
populatie_m = numpy.asarray(populatie_m)
'''


def crossover_PMX(x1, x2, n):
    # generarea secventei de crossover
    poz = numpy.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = numpy.random.randint(0, n, 2)
    p1 = numpy.min(poz)
    p2 = numpy.max(poz)
    c1 = PMX(x2, x2, n, p1, p2)
    c2 = PMX(x2, x1, n, p1, p2)
    return c1, c2


# aplica PMX pe x1,x2 de dimensiune n, cu secventa de recombinare (p1,p2)
def PMX(x1, x2, n, p1, p2):
    # initializare copil - un vector cu toate elementele -1 - valori care s=sa nu fie in 0,...,n-1
    c = -numpy.ones(n, dtype=int)
    # copiaza secventa comuna in copilul c
    c[p1:p2 + 1] = x1[p1:p2 + 1]
    # analiza secventei comune - in permutarea y
    for i in range(p1, p2 + 1):
        # plasarea alelei a
        a = x2[i]
        if a not in c:
            curent = i
            plasat = False
            while not plasat:
                b = x1[curent]
                # poz=pozitia in care se afla b in y
                [poz] = [j for j in range(n) if x2[j] == b]
                if c[poz] == -1:
                    c[poz] = a
                    plasat = True
                else:
                    curent = poz
    # z= vectorul alelelor din y inca necopiate in c
    z = [x2[i] for i in range(n) if x2[i] not in c]
    # poz - vectorul pozitiilor libere in c - cele cu vaori -1
    poz = [i for i in range(n) if c[i] == -1]
    # copierea alelelor inca necopiate din y in c
    m = len(poz)
    for i in range(m):
        c[poz[i]] = z[i]
    return c


# operatorul OCX
# I: permutarile x,y de dimensiune n
# E: copiii rezultati c1,c2
def crossover_OCX(x, y, n):
    # generarea secventei de crossover
    poz = numpy.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = numpy.random.randint(0, n, 2)
    p1 = numpy.min(poz)
    p2 = numpy.max(poz)
    c1 = OCX(x, y, n, p1, p2)
    c2 = OCX(y, x, n, p1, p2)
    return c1, c2


# aplica OCX pe x,y de dimensiune n, cu secventa de recombinare (p1,p2)
def OCX(x, y, n, p1, p2):
    # copiaza secventa comuna in c2
    c2 = [x[i] for i in range(p1, p2 + 1)]
    # calculeaza z pe baza lui y:componentele incepand cu p2 pana la n si apoi de la 0 la p2-1, excluzand elementele care au fost deja copiate
    z1 = [y[i] for i in range(p2, n) if y[i] not in c2]
    z2 = [y[i] for i in range(p2) if y[i] not in c2]
    z = numpy.append(z1, z2)
    # calculeza secventa finala a individului rezultat  - din z de la 0 la n-p2
    c3 = [z[i] for i in range(n - p2 - 1)]
    # calculeaza secventa de inceput a individului rezultat - din z de la n-p2...len(z)
    c1 = [z[i] for i in range(n - p2 - 1, len(z))]
    # calculeaza copilul c
    c = numpy.append(c1, c2)
    c = numpy.append(c, c3)
    return c


def crossover_populatie(pop, dim, n, c, pc):
    copii = pop.copy()
    # initializeaza populatia de copii, po, cu matricea cu elementele 0
    for i in range(0, dim - 1, 2):
        # selecteaza parintii
        x = pop[i]
        y = pop[i + 1]

        r = numpy.random.uniform(0, 1)
        if r <= pc:
            # crossover x cu y - PMX
            c1, c2 = crossover_PMX(x[:n], y[:n], n)

            v1 = fitnessTSP(c1, n, c)
            v2 = fitnessTSP(c2, n, c)

            c1 = list(c1)
            c2 = list(c2)

            c1 = c1 + [v1]
            c2 = c2 + [v2]

            copii[i] = c1.copy()
            copii[i + 1] = c2.copy()
    return copii


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
    pop_initiala, dim, n, c = gen(10)
    parinti = ruleta(pop_initiala, dim, n)
    pop_initiala = numpy.asarray(pop_initiala)
    parinti = numpy.asarray(parinti)
    return pop_initiala, parinti


'''
import TSP
pop_initiala, parinti = TSP.SelectieParinti()
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
    pop_initiala1, dim, n, c = gen(10)
    pop_initiala2, dim, n, c = gen(10)
    pop_urm = elitism(pop_initiala1, pop_initiala2, dim, n)
    pop_initiala1 = numpy.asarray(pop_initiala1)
    pop_initiala2 = numpy.asarray(pop_initiala2)
    pop_urm = numpy.asarray(pop_urm)
    return pop_initiala1, pop_initiala2, pop_urm


'''
import TSP
pop_initiala1, pop_initiala2, pop_urm = TSP.SelectieGeneratieUrmatoare()
'''


def GA(dim, NMAX, pc, pm):
    # generarea populatiei la momentul initial
    pop_initiala, dim, n, c = gen(dim)
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
    n = 10

    while it < NMAX and not gata:
        parinti = ruleta(pop_initiala, dim, n)
        pop_copii = crossover_populatie(parinti, dim, n, c, pc)
        pop_copii_mutanti = mutatie_populatie(pop_copii, dim, n, c, pm)
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
        pop_initiala_gene = pop_urmatoare.copy()
        # de aici algoritmul se reia de sus, de la while, pentru (eventuala) urmatoare generatie

    # la acest moment s-a iesit din while, deci algoritmul a luat sfarsit, ramane sa procesam datele obtinute
    # transformarea din lista in vector pentru a aplica functia where corect
    poz_max = numpy.where(pop_urmatoare[:, -1] == maxim)
    individ_max_gene = pop_urmatoare[poz_max[0][0], 0:n]
    individ_max_fitness = maxim
    return numpy.asarray(individ_max_gene), individ_max_fitness


individ_max_gene, individ_max_fitness = GA(10, 100, 0.8, 0.1)
print(numpy.asarray(individ_max_gene))
print(individ_max_fitness)

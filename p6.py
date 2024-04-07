import numpy as np


# numerele de la 1 la 350 pot fi reprezentate pe 9 biti

# reprezentarea numarului natural x in sir binar Gray pe m biti
def nat_Gray(x, m):
    # obtine reprezentarea binara a lui x in forma '0b_sir de biti' si extrage sir_biti
    t = bin(x)[2:]
    # completarea cu 0 pentru reprezentarea pe m biti
    t = t.zfill(m)
    # t este un sir de caractere
    rezultat = t[0]
    for i in range(1, m):
        # efectuarea operatiei XOR la nivel de bit - lucreaza pe numere intregi
        bit = str(int(t[i]) ^ int(t[i - 1]))
        # adaugarea la sir a caracterului bit
        rezultat = rezultat + bit
    # rezultatul este un sir de biti - string cu elemente '0' si '1'
    return rezultat


# operatia inversa celei prezentate mai sus
def Gray_bin(bG):
    m = len(bG)
    # obtine reprezentarea binara standard, ca sir de caractere
    bS = bG[0]
    val = int(bG[0])
    for i in range(1, m):
        if bG[i] == '1':
            val = int(not (val))
        bS = bS + str(val)
    # obtine reprezentarea in baza 10 a sirului binar sir
    n = int(bS, 2)
    return n


def fitness(sir):
    x = Gray_bin(sir)
    return x ** 2


def cerinta_a(dim):
    populatie = []
    calitati = np.zeros(dim, dtype="int")
    for i in range(dim):
        x = np.random.randint(1, 351)
        populatie = populatie + [nat_Gray(x, 9)]
        calitati[i] = fitness(populatie[i])
    return populatie, calitati


# pop = gen_pop(100)
# pop = np.asarray(pop)
# print()

def recombinare(pop, pc):
    popc = pop.copy()
    dim = len(pop)
    n = len(pop[0]) - 1
    for i in range(0, dim - 1, 2):
        r = np.random.uniform(0, 1)
        if r <= pc:
            p1 = pop[i][:-1].copy()
            p2 = pop[i + 1][:-1].copy()
            punct = np.random.randint(0, n)
            c1 = p1[:punct] + p2[punct:]
            c2 = p2[:punct] + p1[punct:]
            x1 = Gray_bin(c1)
            x2 = Gray_bin(c2)
            f1 = fitness(x1)
            f2 = fitness(x2)
            c1.append(x1)
            c2.append(x2)
            popc[i] = c1
            popc[i + 1] = c2
    return popc

# pop = gen_pop(50)
# popc = recombinare(pop, 0.4)
# pop = np.asarray(pop)
# popc = np.asarray(popc)
# print(popc)

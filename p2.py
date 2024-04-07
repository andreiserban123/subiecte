import numpy as np


def dec_to_bin(n, m):
    val = bin(n)[2:]
    val = val.zfill(m)
    v = [int(val[i]) for i in range(m)]
    return v


def bin_to_dec(n, m):
    y = ''
    for i in range(m):
        y += str(n[i])
    y = int(y, 2)
    return y


def fitness(sir):
    x = bin_to_dec(sir[0:11], 11)
    y = bin_to_dec(sir[11:23], 12)
    return (y - 1) * (np.sin(x - 2) ** 2)


def cerinta_a(dim):
    pop = []
    for i in range(dim):
        x = np.random.randint(0, 1501)
        y = np.random.randint(0, 2502)
        print("Componentele in baza 10 (fenotipul):", x, y)
        individ = dec_to_bin(x, 11) + dec_to_bin(y + 1, 12)
        print("Reprezentarea genotipului", individ)
        calitate = fitness(individ)
        individ += [calitate]
        pop += [individ]
    return pop


def recombinare_3puncte(sir1, sir2):
    n = 23
    i = np.random.randint(0, n - 2)
    j = np.random.randint(i + 1, n - 1)
    k = np.random.randint(j + 1, n)
    copil1 = sir1.copy()
    copil2 = sir2.copy()
    copil1[j:k + 1] = sir2[j:k + 1]
    copil2[j:k + 1] = sir1[j:k + 1]
    return copil1, copil2


def cerinta_b(populatie, pc):
    print("\n\nPopulatia de copii")
    dim = len(populatie)
    copii = populatie.copy()
    for i in range(0, dim - 1, 2):
        r = np.random.uniform(0, 1)
        if r <= pc:
            p1 = populatie[i][:23].copy()
            p2 = populatie[i + 1][:23].copy()
            c1, c2 = recombinare_3puncte(p1, p2)
            copii[i][:23] = c1
            copii[i][23] = fitness(c1)
            copii[i + 1][:23] = c2
            copii[i + 1][23] = fitness(c2)
            print("Individ+calitate", copii[i])
            print("Individ+calitate", copii[i + 1])
    return copii


if __name__ == "__main__":
    p = cerinta_a(10)
    c = cerinta_b(p, 0.8)

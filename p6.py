import numpy

# Transformare din dec in cod Gray
def dec_to_gray(val):
    gray_rep = bin(val^(val>>1))[2:].zfill(9)
    gray_rep_int = [int(bit) for bit in gray_rep]
    return gray_rep_int

# Transmit individul fara fitness si returnez valoarea binara
def gray_to_dec(indiv):
    indiv_str = ''.join(str(bit) for bit in indiv)
    gray_str = indiv_str[0]
    for i in range(1, len(indiv_str)):
        gray_str += str(int(indiv_str[i-1]) ^ int(indiv_str[i]))
    return int(gray_str, 2)

# Functia de calculare a fitnessului. Primeste valoarea zecimala a individului
def fitness(val):
    return val**2

def generare_populatie_initiala(dim):
    population = []
    for i in range(dim):
        val = numpy.random.randint(1, 351)
        val_in_gray = dec_to_gray(val)
        val_in_gray.append(fitness(val))
        population.append(val_in_gray)
    return population

pop = generare_populatie_initiala(5)
print(pop)

def recombinare_unipunct(pop, pc):
    popc = pop.copy()
    for i in range(0, len(pop), 2):
        if i+1 < len(pop) and numpy.random.uniform(0, 1 ) < pc:
            indiv1 = pop[i]
            indiv2 = pop[i+1]
            index = numpy.random.randint(0, len(indiv1))
            copil1 = indiv1[:index] + indiv2[index:]
            copil2 = indiv2[:index] + indiv1[index:]
            popc[i] = copil1
            popc[i+1] = copil2
            popc[i][-1] = fitness(gray_to_dec(copil1[:-1]))
            popc[i+1][-1] = fitness(gray_to_dec(copil2[:-1]))
    return popc

popc = recombinare_unipunct(pop, 0.2)
print(popc)
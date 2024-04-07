import numpy as np


def fitness(x1, x2, x3, x4):
    return 1 + np.sin(2 * x1 - x3) + (x2 * x4) ** (1 / 3)


def gen(dim):
    pop = []
    for i in range(dim):
        x1 = np.random.uniform(-1, 1)
        x2 = np.random.uniform(0, 0.2)
        x3 = np.random.uniform(0, 1)
        x4 = np.random.uniform(0, 5)
        f = fitness(x1, x2, x3, x4)
        x = [x1, x2, x3, x4, f]
        pop.append(x)
    return pop


# Generate the initial population
pop = gen(12)
pop = np.asarray(pop)
pop.shape


def mutation(pop, pm, t=0.6):
    sigma = t / 3
    mutated_pop = pop.copy()
    for i in range(mutated_pop.shape[0]):
        if np.random.rand() < pm:
            for j in range(mutated_pop.shape[1] - 1):  # Exclude the fitness value from mutation
                mutated_pop[i][j] += np.random.normal(0, sigma)
                # Make sure the mutated gene is within the specified bounds
                if j == 0:
                    mutated_pop[i][j] = np.clip(mutated_pop[i][j], -1, 1)
                elif j == 1:
                    mutated_pop[i][j] = np.clip(mutated_pop[i][j], 0, 0.2)
                elif j == 2:
                    mutated_pop[i][j] = np.clip(mutated_pop[i][j], 0, 1)
                elif j == 3:
                    mutated_pop[i][j] = np.clip(mutated_pop[i][j], 0, 5)
            # Recalculate the fitness for the mutated individual
            mutated_pop[i][-1] = fitness(*mutated_pop[i][:-1])
    return mutated_pop


# Define mutation probability
pm = 0.1  # Example mutation probability

# Apply mutation to the population
mutated_pop = mutation(pop, pm)
mutated_pop

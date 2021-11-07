import numpy as np
import inspect
import enum
import random
import time
import math

class SelectionType(enum.Enum):
    STEADY_STATE = 1

class CrossoverType(enum.Enum):
    AVERAGE = 1

class MutationType(enum.Enum):
    TYPE_1 = 1

def optimize(objectiveFunction, nChromosomes, nGenes, selectionType, crossoverType, mutationType):

    nMinimumChromosomes = 3
    if nChromosomes < nMinimumChromosomes:
        raise Exception('Number of chromosomes cannot be less than {}.'.format(nMinimumChromosomes))

    population = np.random.uniform(100, 150, (nChromosomes, nGenes + 1))
    # population[:, -1] = -1e9

    # Calculate fitness.
    population[:, -1] = np.apply_along_axis(objectiveFunction, 1, population[:, 0:-1])

    # Sort by fitness in descending order.
    population = population[(-population[:, -1]).argsort()]

    nGenerations = 0

    while population[0, -1] < -1e-6:

        nGenerations += 1

        # Crossover.
        population[-1, 0:-1] = (population[0, 0:-1] + population[1, 0:-1]) / 2

        # Mutation.
        value = 6
        mutationFlag = np.random.rand(nGenes + 1) > 0.5
        mutationValue = np.random.uniform(-value, value, nGenes + 1)
        population[-1, mutationFlag] = population[-1, mutationFlag] + mutationValue[mutationFlag]

        # Recalculate fitness.
        population[-1, -1] = objectiveFunction(population[-1, 0:-1])

        # Resort by fitness.
        population = population[(-population[:, -1]).argsort()]

        # # Resort by fitness.
        # population = np.roll(population, 1, 0)
        # population[0:3] = population[(-population[0:3, -1]).argsort()]

        if nGenerations % 500 == 0:
            print("Generation: {}. Objective: {}".format(nGenerations, population[0, -1]))

    print("Genes: {}".format(population[0, 0:-1]))

def product(list):
    result = 1
    for i in range(len(list)):
        result *= list[i]
    return result

def griewankFunction(*xs):
    return 1 + (1 / 4000) * sum([x ** 2 for x in xs]) - product([math.cos(x / math.sqrt(i + 1)) for i, x in enumerate(xs)])

def objective(xs):
    return -griewankFunction(*xs)

# def objective(arguments):
#     x = arguments[0]
#     y = arguments[1]
#     return -((x) ** 2 + (y) ** 2)

startTime = time.time()
optimize(objective, 100, 3, SelectionType.STEADY_STATE, CrossoverType.AVERAGE, MutationType.TYPE_1)
print("Elapsed {} seconds.".format(time.time() - startTime))



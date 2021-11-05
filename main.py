import random
import enum
import time
import cmath

class Chromosome:

    def __init__(self, nGenes, f):
        self.nGenes = nGenes
        self.genes = []
        self.f = f
        self.fitness = 0

        for i in range(self.nGenes):
            self.genes.append(random.uniform(100, 200))

    def calculateFitness(self):
        self.fitness = self.f(*self.genes)

    def mutate(self):

        # if random.uniform(0, 1) < 0.75:
        #     return

        mutationPoint = random.randint(0, self.nGenes - 1)

        magnitude = 0.1
        value = random.uniform(-magnitude, magnitude)

        self.genes[mutationPoint] = self.genes[mutationPoint] + value

class Pool:

    def __init__(self, nChromosomes, nGenes, f):
        self.nChromosomes = nChromosomes
        self.nGenes = nGenes
        self.chromosomes = []
        self.f = f

        for i in range(self.nChromosomes):
            self.chromosomes.append(Chromosome(self.nGenes, self.f))

    def calculateFitness(self):
        for i in range(self.nChromosomes):
            self.chromosomes[i].calculateFitness()

    def sortByFitness(self):
        self.chromosomes.sort(key = lambda x: x.fitness, reverse = True)

class Genetic:

    class CrossoverType(enum.Enum):
        SWAP_N_POINT = 1
        AVERAGE_N_POINT = 2
        AVERAGE = 3
        TEST = 4

    def __init__(self, nChromosomes, nGenes, f):

        if nChromosomes < 2:
            raise Exception('Number of chromosomes in the pool must be greater than 2.')

        self.nChromosomes = nChromosomes
        self.nGenes = nGenes
        self.f = f
        self.pool = Pool(self.nChromosomes, self.nGenes, self.f)
        self.generationCount = 0

        self.pool.calculateFitness()
        self.pool.sortByFitness()

        while (self.getFittest().fitness < -0.0001):

            self.generationCount += 1

            self.selection()
            self.crossover(self.CrossoverType.AVERAGE)
            self.mutation()
            
            self.pool.calculateFitness()
            self.pool.sortByFitness()
            self.addFittest()
            self.pool.calculateFitness()
            self.pool.sortByFitness()

            print("Generation: {}. Fitness: {}".format(self.generationCount, self.getFittest().fitness))

        print("Objective: {}".format(self.f(*self.getFittest().genes)))
        print("Genes: {}".format(self.getFittest().genes))

    def addFittest(self):
        # self.pool.chromosomes[-1] = self.pool.chromosomes[0]
        pass

    def getFittest(self):
        return self.pool.chromosomes[0]

    def selection(self):
        pass # Chromosomes already sorted by fitness.

    def crossover(self, type):

        if type == self.CrossoverType.SWAP_N_POINT:

            self.pool.chromosomes[-1].genes = self.pool.chromosomes[0].genes

            crossoverPoint = random.randint(0, self.nGenes)

            for i in range(crossoverPoint):
                self.pool.chromosomes[-1].genes[i] = self.pool.chromosomes[1].genes[i]
        
        elif type == self.CrossoverType.AVERAGE_N_POINT:

            self.pool.chromosomes[-1].genes = self.pool.chromosomes[0].genes

            crossoverPoint = random.randint(0, self.nGenes)

            for i in range(crossoverPoint):
                self.pool.chromosomes[-1].genes[i] = (self.pool.chromosomes[0].genes[i] + self.pool.chromosomes[1].genes[i]) / 2

        elif type == self.CrossoverType.AVERAGE:

            for i in range(self.nGenes):
                self.pool.chromosomes[-1].genes[i] = (self.pool.chromosomes[0].genes[i] + self.pool.chromosomes[1].genes[i]) / 2

    def mutation(self):
        self.pool.chromosomes[-1].mutate()


# def objective(x, y, z):
#     return -((x + 2) ** 2 + (y - 3) ** 2 + (z + 10) ** 2)

def product(list):
    result = 1
    for i in range(len(list)):
        result *= list[i]
    return result

def griewankFunction(*xs):
    return 1 + (1 / 4000) * sum([x ** 2 for x in xs]) - product([cmath.cos(x / cmath.sqrt(1j)) for x in xs])

def objective(*xs):
    return -abs(griewankFunction(*xs))

startTime = time.time()
genetic = Genetic(10, 2, objective)
print("Elapsed {} seconds.".format(time.time() - startTime))
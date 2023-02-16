# A genetic algorithm is a stochastic search method based on
# natural selection and reproduction of a population of individuals.
# Each generation, the fittest candidates in the population are selected,
# paired, and recombined into a new generation.
# With each new generation the system converges towards an optimal fitness.
# Optimal fitness can be global or local.
# - The global optimum is the optimal solution among all possible solutions;
#   the goal of the the GA.
# - The local optimum occurs when the GA converges too fast and is trapped.
#   This occurs when the population is no longer diverse enough.
#   Therefore, we need to preserve some weaker candidates whose role
#   can become more prominent later on.
# - Stochastic: the process of selecting the fittest candidates in
#   the population involves an amount of randomness, so weaker candidates
#   are sometimes preserved.
# - Convergence: the approach toward a definite value or equilibrium state.

### GENETIC ALGORITHM FUNCTIONS ##########################################

def candidate():
    # Needs to be implemented.
    return None

def recombine(a, b, crossover=0.5):
    # Needs to be implemented.
    return None

def fitness(candidate):
    # Needs to be implemented.
    return 0

def population(size=500):
    """ Returns an initial list of random candidates (e.g. generation 0).
    """
    return [candidate() for i in range(size)]

def sort_by_fitness(candidates):
    """ Returns a sorted list of (fitness, candidate)-tuples; best-first.
    """
    return sorted([(fitness(x), x) for x in candidates], reverse=True)

def select(population, top=0.7, determinism=0.8):
    """ Returns a selection of fit candidates from the population.
    - top: roughly the fittest 70% candidates are allowed to reproduce.
    - determinism: there is a 20% chance that good candidates are ignored,
                   this keeps the population diverse.
    """
    population = sort_by_fitness(population)
    population = [candidate for (fitness, candidate) in population]
    parents = list(population)
    i = len(parents)
    while len(parents) > len(population)*top:
        i = (i-1) % len(parents)
        if random() < determinism:
            parents.pop(i)
    return parents

def reproduce(population, top=0.7, determinism=0.8, crossover=lambda: random()):
    """ Returns a new population of candidates.
    Selects parent that are fit to reproduce.
    Recombines random pairs of parents to new child candidates.
    """
    parents = select(population, top, determinism)
    children = []
    for i in range(len(population)):
        i = random(len(parents))
        j = choice( list(range(0,i)) + list(range(i+1, len(parents))) )
        k = crossover
        try: k = k()
        except:
            pass
        children.append(recombine(parents[i], parents[j], crossover=k))
    return children

def converged(population):
    """ Returns True when the population has reached its optimum.
    """
    for i in range(1, len(population)):
        if population[i-1] != population[i]:
            return False
    return True

### GRID CANDIDATE #######################################################
# Any kind of candidate can be used in the GA.
# Here's an example of random black & white grids that score better
# as they become more symmetrical.
# We just create one candidate (or agent) with a fitness property and
# the capability to recombine; the GA functions will create a population
# and keep improving it until it converges.

# Internally, the grid is just a list of colors (in this case: True (black)
# or False (white)). This makes it an ideal candidate to work with:
# lists are easy to examine and cut-and-splice in the recombine function.
# You can imagine how the values in the list could encompass a wider range
# of colors(for example: 0=black, 1=white, 2=red, ...)

class GridCandidate(list):

    def __init__(self, rows, cols, values=[]):
        self.rows = rows
        self.cols = cols
        # Cells in the grid are randomly black (True) or white (False).
        if len(values) == 0:
            values = [choice((True, False)) for i in range(rows*cols)]
        list.__init__(self, values)

    def draw(self, x, y, scale=10.0):
        for i in range(self.cols):
            for j in range(self.rows):
                is_black = self[i+j*cols]
                _ctx.fill(int(not is_black))
                _ctx.oval(x+i*scale, y+j*scale, scale, scale)

                # Triangles:
                #R = 1.11803398875 # equilateral width/height ratio
                #_ctx.push()
                #_ctx.translate(x+i*scale/2, y+j*scale/R)
                #if i % 2 == int(j & 2 == 0): # up for odd col in even row
                #    _ctx.beginpath(0, 0)
                #    _ctx.lineto(scale/2, scale/R)
                #    _ctx.lineto(scale, 0)
                #else:
                #    _ctx.beginpath(0, scale/R)
                #    _ctx.lineto(scale/2, 0)
                #    _ctx.lineto(scale, scale/R)
                #_ctx.endpath()
                #_ctx.pop()

    def contains(self, i):
        return i > 0 and i < len(self)

    def row(self, i):
        return i // self.cols # the row index i is in
    def col(self, i):
        return i % self.cols # the column index i is in

    def reflect(self, i, axis="horizontal"):
        """ Returns the index in the grid that is symmetrical to this one.
        For example:
        0 1 2 3 4
        5 6 7 8 9
        reflect(1, "horizontal") => 3
        reflect(4, "vertical") => 9
        """
        if axis == "horizontal":
            return self.row(i)*self.cols + self.cols - self.col(i) - 1
        if axis == "vertical":
            return (self.rows-self.row(i)-1)*self.cols + self.col(i)

    def recombine(self, other, crossover=0.5):
        i = int(len(self) * crossover)
        return GridCandidate(self.rows, self.cols, values=self[:i]+other[i:])

    @property
    def fitness(self):
        # Fitness is calculated in terms of symmetry.
        # Grids with the same color at symmetrical positions score better.
        score = 0
        for i in range(len(self)):
            j = self.reflect(i, "horizontal")
            if self.contains(j) and self[j] == self[i]:
                score += 1
            j = self.reflect(i, "vertical")
            if self.contains(j) and self[j] == self[i]:
                score += 1
        return score

    # Here are some functions you may want to use to determine fitness:

    def above(self, i) : return i-self.cols
    def below(self, i) : return i+self.cols
    def left( self, i) : return i+1
    def right(self, i) : return i-1

    north, south, east, west = above, below, left, right

    def northeast(self, i) : return self.north(self.east(i))
    def northwest(self, i) : return self.north(self.west(i))
    def southeast(self, i) : return self.south(self.east(i))
    def southwest(self, i) : return self.south(self.west(i))


# Grid size.
rows = 5
cols = 5

candidate = lambda: GridCandidate(rows, cols)
recombine = lambda a, b, crossover: a.recombine(b, crossover)
fitness = lambda candidate: candidate.fitness

# The initial random population:
p = population(size=500)

size(800, 2000)
# Process n generations:
for i in range(40):
    p = reproduce(p, top=0.6, determinism=0.65)

    #translate(0, 35)
    #push()
    #for candidate in p[:15]:
    #    translate(35, 0)
    #    candidate.draw(0, 0, scale=5)
    #pop()

    if converged(p):
        print( "converged at generation ", str(i) )
        break

# A list of scores for each member in the final population:
#print( [score for score, x in sort_by_fitness(p)] )

# The best solution in the final population:
p[0].draw(20, 20, scale=30)

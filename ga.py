from optimise import ObjectiveFunction

import random
import logging

class Individual(object):
    '''
    an individual in the population
    '''
    def __init__(self, solution, objective_function, move_operator, recombine_operator):
        self.solution=solution
        self.objective_function=objective_function
        self.move_operator=move_operator
        self.recombine_operator=recombine_operator
        self._score=None
    
    def _new_from_solution(self,solution):
        return Individual(solution, self.objective_function, self.move_operator, self.recombine_operator)
    
    def breed(self,parent):
        if random.random() < 1:
            solution=self.recombine_operator(self.solution, parent.solution)
            return self._new_from_solution(solution)
        return self
    
    def mutate(self):
        if random.random() < 1:
            solution=self.move_operator(self.solution).next()
            return self._new_from_solution(solution)
        return self
    
    def score(self):
        if self._score is None:
            self._score=self.objective_function(self.solution)
        return self._score
    
    #def __hash__(self):
    #    return hash(self.solution)
    #
    #def __eq__(self, other):
    #    return self.solution == other.solution
    
    def __repr__(self):
        return "Individual(%d)" % self.score()
    
    def __cmp__(self, other):
        if self.score() < other.score():
            return 1
        elif self.score() > other.score():
            return -1
        return 0

def pop_stats(population):
    pop_size=len(population)
    scores=[p.score() for p in population]
    avg=sum(scores)/float(pop_size)
    var=sum((score-avg)**2 for score in scores)/float(pop_size)
    logging.info("avg: %f var: %f", avg, var)

def tournament(population, size, reverse=False):
    population=list(population)
    selected=[random.choice(population) for i in xrange(size)]
    selected.sort()
    return selected

def replace_if_better(population, parent, child):
    if parent.score() < child.score():
        replace(population, parent, child)

def replace(population, parent, child):
    population.remove(parent)
    population.add(child)

def select_worst(population, tournament_size=None):
    if tournament_size is None:
        tournament_size=len(population)
    return tournament(population, tournament_size, reverse=True)

def replace_worst(population, child, tournament_size=None):
    worst=select_worst(population, tournament_size)
    replace(population, worst, child)

def replace_worst_if_better(population, child, tournament_size=None):
    worst=select_worst(population, tournament_size)
    replace_if_better(population, worst, child)

def replace_worst_parent(population, p1, p2, child):
    worst=p1
    if p2.score() < p1.score():
        worst=p2
    replace(population, worst, child)

def steady_state(init_function,move_operator,objective_function,max_evaluations,recombine_operator,pop_size,breed_size=50,replace_size=2):
    objective_function=ObjectiveFunction(objective_function)

    insert=lambda population, child: replace_worst_if_better(population, child, replace_size)

    population=set([Individual(init_function(),objective_function,move_operator,recombine_operator) for i in xrange(pop_size)])

    while objective_function.num_evaluations < max_evaluations:
        competitors=tournament(population, breed_size)
        p1,p2,worst=competitors[0],competitors[1],competitors[-1]
        child=p1.breed(p2)
        child=child.mutate()
        
        replace(population, worst, child)

        if objective_function.num_evaluations % 1000 == 0:
            pop_stats(population)

    return (objective_function.num_evaluations,objective_function.best_score,objective_function.best)


def cull(population, pop_size):
    return set(list(sorted(population,reverse=True))[:pop_size])

def generational(init_function,move_operator,objective_function,max_evaluations,recombine_operator,pop_size):
    objective_function=ObjectiveFunction(objective_function)

    insert=lambda population, child: replace_worst_if_better(population, child, replace_size)

    population=set([Individual(init_function(),objective_function,move_operator,recombine_operator) for i in xrange(pop_size)])
    
    while objective_function.num_evaluations < max_evaluations:
        next_population=set()
        #while len(next_population) < pop_size and objective_function.num_evaluations < max_evaluations:
        #    p1=tournament(population, 2)
            #p2=tournament(population, 2)
            #child=p1.breed(p2)
            #if random.random() < 0.1:
        for p1 in population:
            #p2=tournament(population, 2)
            #child=p1.breed(p2)
            child=p1.mutate()
            child.score()
            next_population.add(child)
            if objective_function.num_evaluations % 1000 == 0:
                pop_stats(population)
        else:
            # swap population over
            population.update(next_population)
            population=cull(population,pop_size)
            #print len(population)
    
    return (objective_function.num_evaluations,objective_function.best_score,objective_function.best)

def roulette_selection(population):
    total_fitness=sum(i.score() for i in population)
    r=random.random()
    s=0
    
    for i in population:
        s += i.score()
        p=((total_fitness-s)/total_fitness)
        if r <= p:
            return i
    return i # or return last one

def hillclimb(i):
    while True:
        i1=i.mutate()
        if i1.score() > i.score():
            i=i1
        if random.random() < 0.5:
            break
    return i

def generational2(init_function,move_operator,objective_function,max_evaluations,recombine_operator,pop_size):
    objective_function=ObjectiveFunction(objective_function)
    
    population=[Individual(init_function(),objective_function,move_operator,recombine_operator) for i in xrange(pop_size)]
    population.sort()
    next_population=[]
    
    elite_size=1
    
    while objective_function.num_evaluations < max_evaluations:
        if len(next_population)+elite_size < len(population):
            p1=roulette_selection(population)
            p2=roulette_selection(population)
            child=p1.breed(p2).mutate()
            #child=p1.mutate()
            #child=hillclimb(child)
            next_population.append(child)
        else:
            # keep some of the fittest individuals from last time
            population=population[:elite_size] + next_population
            population.sort()
            next_population=[]
    
    return (objective_function.num_evaluations,objective_function.best_score,objective_function.best)

evolve=steady_state


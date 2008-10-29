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
        solution=self.recombine_operator(self.solution, parent.solution)
        return self._new_from_solution(solution)
    
    def mutate(self):
        solution=self.move_operator(self.solution).next()
        return self._new_from_solution(solution)
    
    def score(self):
        if self._score is None:
            self._score=self.objective_function(self.solution)
        return self._score
    
    def __hash__(self):
        return hash(self.solution)
    
    def __eq__(self, other):
        return self.solution == other.solution
    
    def __repr__(self):
        return "Individual(%d)" % self.score()

def pop_stats(population):
    pop_size=len(population)
    scores=[p.score() for p in population]
    avg=sum(scores)/float(pop_size)
    var=sum((score-avg)**2 for score in scores)/float(pop_size)
    logging.info("avg: %f var: %f", avg, var)

def tournament(population, size, reverse=False):
    population=list(population)
    selected=(random.choice(population) for i in xrange(size))
    if reverse:
        scoring=min
    else:
        scoring=max
    best_score, best=scoring((i.score(), i) for i in selected)
    return best

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

def evolve(init_function,move_operator,objective_function,max_evaluations,recombine_operator):
    objective_function=ObjectiveFunction(objective_function)
    
    pop_size=10
    cull_size=pop_size
    breed_tournament_size=2
    replace_tournament_size=2
    
    insert=lambda population, child: replace_worst_if_better(population, child, replace_tournament_size)
    #insert=replace_worst_if_better
    #insert=replace_worst
    
    population=set([Individual(init_function(),objective_function,move_operator,recombine_operator) for i in xrange(pop_size)])
    
    while objective_function.num_evaluations < max_evaluations:
        p1=tournament(population, breed_tournament_size)
        p2=tournament(population, breed_tournament_size)
        child=p1.breed(p2)
        child=child.mutate()
        
        child.score()
        if child not in population:
            #worst=p1
            #if p2.score() < p1.score():
            #    worst=p2
            #replace(population, worst, child)
            insert(population, child)
        
        if objective_function.num_evaluations % 1000 == 0:
            pop_stats(population)
    
    return (objective_function.num_evaluations,objective_function.best_score,objective_function.best)




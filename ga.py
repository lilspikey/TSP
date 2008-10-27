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
    
    def __repr__(self):
        return "Individual(%d)" % self.score()

def pop_stats(population):
    pop_size=len(population)
    scores=[p.score() for p in population]
    avg=sum(scores)/float(pop_size)
    var=sum((score-avg)**2 for score in scores)/float(pop_size)
    logging.info("avg: %f var: %f", avg, var)

def tournament(population, size, reverse=False):
    selected=random.sample(population,size)
    if reverse:
        scoring=min
    else:
        scoring=max
    best_score, best=scoring((i.score(), i) for i in population)
    return best

def replace_if_better(population, parent, child):
    if parent.score() < child.score():
        replace(population, parent, child)

def replace(population, parent, child):
    population.remove(parent)
    population.append(child)

def select_worst(population):
    return tournament(population, len(population), reverse=True)

def replace_worst(population, child):
    worst=select_worst(population)
    replace(population, worst, child)

def replace_worst_if_better(population, child):
    worst=select_worst(population)
    replace_if_better(population, worst, child)

def in_population(population, child):
    for i in population:
        if i.solution == child.solution:
            return True
    return False

def evolve(init_function,move_operator,objective_function,max_evaluations,recombine_operator):
    objective_function=ObjectiveFunction(objective_function)
    
    pop_size=150
    cull_size=pop_size
    tournament_size=2
    mutation_rate=0.5
    breed_rate=1
    #insert=replace_worst
    insert=replace_worst_if_better
    
    population=[Individual(init_function(),objective_function,move_operator,recombine_operator) for i in xrange(pop_size)]
    
    while objective_function.num_evaluations < max_evaluations:
        p1=tournament(population, tournament_size)
        p2=tournament(population, tournament_size)
        child=p1.breed(p2)
        child=child.mutate()
        
        child.score()
        if not in_population(population, child):
            insert(population, child)
        
        if objective_function.num_evaluations % 1000 == 0:
            pop_stats(population)
    
    return (objective_function.num_evaluations,objective_function.best_score,objective_function.best)




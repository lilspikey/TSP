from optimise import ObjectiveFunction

import random

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
    print "avg: ", avg, " var: ", var

def evolve(init_function,move_operator,objective_function,max_evaluations,recombine_operator):
    objective_function=ObjectiveFunction(objective_function)
    
    pop_size=5
    mutation_rate=1.0
    breed_rate=0.1
    population=[Individual(init_function(),objective_function,move_operator,recombine_operator) for i in xrange(pop_size)]
    
    while objective_function.num_evaluations < max_evaluations:
        p1,p2=random.sample(population,2)
        #if p1.score() < p2.score():
        #    population.remove(p1)
        #else:
        #    population.remove(p2)
        if random.random() < breed_rate:
            child=p1.breed(p2)
        else:
            child=p1
        if random.random() < mutation_rate:
            child=child.mutate()
        
        if p1.score() < child.score():
            population.remove(p1)
            population.append(child)
        #population.append(child)
        #population.sort(key=Individual.score, reverse=True)
        #population=population[:pop_size]
        
        if objective_function.num_evaluations % 1000 == 0:
            pop_stats(population)
    
    return (objective_function.num_evaluations,objective_function.best_score,objective_function.best)




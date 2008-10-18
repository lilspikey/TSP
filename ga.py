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

def evolve(init_function,move_operator,objective_function,max_evaluations,recombine_operator):
    objective_function=ObjectiveFunction(objective_function)
    
    pop_size=4
    population=[Individual(init_function(),objective_function,move_operator,recombine_operator) for i in xrange(pop_size)]
    
    while objective_function.num_evaluations < max_evaluations:
        p1,p2=random.sample(population,2)
        p1=p1.mutate()
        p2=p2.mutate()
        child=p1.breed(p2)
        population.append(child)
        population.sort(key=Individual.score, reverse=True)
        population=population[:pop_size]
        
        #if objective_function.num_evaluations % 20 == 0:
        #    print population
    
    return (objective_function.num_evaluations,objective_function.best_score,objective_function.best)




import logging

class ObjectiveFunction(object):
    '''class to wrap an objective function and 
    keep track of the best solution evaluated'''
    def __init__(self,objective_function):
        self.objective_function=objective_function
        self.best=None
        self.best_score=None
        self.num_evaluations=0
    
    def __call__(self,solution):
        score=self.objective_function(solution)
        self.num_evaluations+=1
        if self.best is None or score > self.best_score:
            self.best_score=score
            self.best=solution
            logging.info('new best score: %f after %d', self.best_score, self.num_evaluations)
        return score
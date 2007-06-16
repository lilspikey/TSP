import random
import math
import logging

def P(prev_score,next_score,temperature):
    if next_score > prev_score:
        return 1.0
    else:
        return math.exp( -abs(next_score-prev_score)/temperature )

class ObjectiveFunction:
    '''class to wrap an objective function and make sure
    it is never called more than max_evaluation times.
    also used to keep track of the best solution evaluated'''
    def __init__(self,objective_function,max_evaluations):
        self.objective_function=objective_function
        self.num_evaluations=0
        self.max_evaluations=max_evaluations
        self.best=None
        self.best_score=None
    
    def __call__(self,solution):
        if self.num_evaluations >= self.max_evaluations:
            raise StopIteration # stop any further evaluations
        self.num_evaluations+=1
        score=self.objective_function(solution)
        if self.best is None or score > self.best_score:
            self.best_score=score
            self.best=solution
            logging.info('%d, new best score: %f',self.num_evaluations,self.best_score)
        return score

def kirkpatrick_cooling(T0,Tn,max_evaluations):
    T=T0
    alpha=(Tn/float(T0))**(1.0/max_evaluations)
    logging.info('alpha %f',alpha)
    while True:
        yield T
        T=alpha*T

def anneal(init_function,move_operator,objective_function,max_evaluations,start_temp,end_temp):
    
    # wrap the objective function
    objective_function=ObjectiveFunction(objective_function,max_evaluations)
    
    
    current=init_function()
    current_score=objective_function(current)
    
    cooling=kirkpatrick_cooling(start_temp,end_temp,max_evaluations)
    
    logging.info('anneal started: score=%f',current_score)
    temperature=0
    try:
        while True:
            # examine moves around our current position
            for next in move_operator(current):
                # see if this move is better than the current
                next_score=objective_function(next)
                
                temperature = cooling.next()
                
                p=P(current_score,next_score,temperature)
                if random.random() < p:
                    current=next
                    current_score=next_score
                    break
    except StopIteration:
        pass # StopIteration will be thrown by our wrapper to signal we're done
    
    num_evaluations=objective_function.num_evaluations
    best_score=objective_function.best_score
    best=objective_function.best
    logging.info('final temperature: %f',temperature)
    logging.info('anneal finished: num_evaluations=%d, best_score=%f',num_evaluations,best_score)
    return (num_evaluations,best_score,best)
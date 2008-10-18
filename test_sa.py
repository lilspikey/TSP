import sa

import random

def test_P():
    for i in xrange(100):
        prev,next=random.random(),random.random()
        temperature=10*random.random()
        p=sa.P(prev,next,temperature)
        if next > prev:
            assert p == 1.0
        else:
            # lower the temp and check we get a lower p
            lower_temperature=temperature*0.5
            p_lower=sa.P(prev,next,lower_temperature)
            assert p_lower < p

def test_objective_function():
    def score_function(solution):
        return int(solution)
    
    objective_function=sa.ObjectiveFunction(score_function)
    assert objective_function.best is None
    assert objective_function.best_score is None
    
    # should keep track of best solution so far
    assert 1 == objective_function("1")
    assert objective_function.best == "1"
    assert objective_function.best_score == 1
    
    assert 3 == objective_function("3")
    assert objective_function.best == "3"
    assert objective_function.best_score == 3
    
    assert 2 == objective_function("2")
    assert objective_function.best == "3"
    assert objective_function.best_score == 3

def test_kirkpatrick_cooling():
    start_temp=1
    rate=0.9
    coooling_schedule=sa.kirkpatrick_cooling(start_temp, rate)
    assert coooling_schedule.next() == start_temp
    assert coooling_schedule.next() == start_temp*rate
    assert coooling_schedule.next() == start_temp*rate*rate
    assert coooling_schedule.next() == start_temp*rate*rate*rate

def objective_function(i):
    return i

max_evaluations=500

def test_simple_anneal():
    '''
    check we perform the same as a hillclimb
    when score keeps improving
    '''
    
    def move_operator(i):
        yield i+1
    def init_function():
        return 1
        
    num_evaluations,best_score,best=sa.anneal(init_function,move_operator,objective_function,max_evaluations,1,0.9)
    
    assert num_evaluations == max_evaluations
    assert best == max_evaluations
    assert best_score == max_evaluations
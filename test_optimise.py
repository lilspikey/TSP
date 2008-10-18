import optimise

def test_objective_function():
    def score_function(solution):
        return int(solution)
    
    objective_function=optimise.ObjectiveFunction(score_function)
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
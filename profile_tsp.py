import tsp
import profile

coords=tsp.read_coords(file('city500.txt'))
init_function=lambda: tsp.init_random_tour(len(coords))
matrix=tsp.cartesian_matrix(coords)
objective_function=lambda tour: -tsp.tour_length(matrix,tour)
move_operator=tsp.reversed_sections
max_iterations=1000

#profile.run('tsp.run_hillclimb(init_function,move_operator,objective_function,max_iterations)')
profile.run('tsp.run_evolve(init_function,move_operator,objective_function,max_iterations)')
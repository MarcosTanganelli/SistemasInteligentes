from ortools.algorithms.python import knapsack_solver

#Função que retornar a solução otima
def solucaoOtima():
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )

    # values = [
    #   360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
    #   78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
    #   87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
    #   312
    # ]
    # weights = [
    #   [7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
    #    42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
    #    3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13],
    # ]
    # capacities = [850]
    # values = [36, 8, 6, 13, 43, 7, 23, 5, 9, 12, 67, 89, 60, 4, 5, 15, 8, 26, 6, 2, 12, 16, 43, 4, 9, 11, 2, 4, 5, 32, 51, 3, 9, 7, 8, 2, 3, 8, 21, 4, 9, 19, 27, 4, 3, 1, 2, 39, 28, 31]

    # weights = [
    #     [1, 0, 3, 2, 8, 9, 1, 8, 7, 6, 6, 2, 0, 4, 0, 1, 2, 4, 1, 0, 4, 5, 5, 3, 3, 5, 6, 1, 3, 8, 0, 1, 2, 6, 1, 3, 9, 4, 7, 0, 9, 7, 3, 6, 0, 8, 2, 7, 5, 1]
    # ]
    values = [36, 8, 6, 13, 43, 7, 23, 5, 9, 12, 67, 89, 60, 4, 5, 15, 8]

    weights = [[1, 0, 3, 2, 8, 9, 1, 8, 7, 6, 6, 2, 0, 4, 0, 1, 2]]

    capacities = [50]


    solver.init(values, weights, capacities)
    computed_value = solver.solve()

    packed_items = []
    packed_values = []
    packed_weights = []
    total_weight = 0
    print("Total value =", computed_value)
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(i)
            packed_values.append(values[i])
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print("Total weight:", total_weight)
    print("Packed items:", packed_items)
    print("Packed_weights:", packed_weights)
    print("Packed_values:", packed_values)



if __name__ == "__main__":
    solucaoOtima()

# Solução ótima
# Total value = 7534
# Total weight: 850
# Packed items: [0, 1, 3, 4, 6, 10, 11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 24, 27, 28, 29, 30, 31, 32, 34, 38, 39, 41, 42, 44, 47, 48, 49]
# Packed_weights: [7, 0, 22, 80, 11, 59, 18, 0, 3, 8, 15, 42, 9, 0, 47, 52, 26, 6, 29, 84, 2, 4, 18, 7, 71, 3, 66, 31, 0, 65, 52, 13]
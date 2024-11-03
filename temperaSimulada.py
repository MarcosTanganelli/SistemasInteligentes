import random
import math
import optuna
import matplotlib.pyplot as plt

#Preciso criar um problema da mochila
#A priori vai ser um problema fixo, depois gerar ele aleatoriamente 
#E buscar uma biblioteca que sempre resulta a solução otima

# Depois preciso criar a tempera Simulada, que se decompoem em:
# Solução inicial aleatoria - function
# Solução vizinha - function
# Temperatura - parametro - aumenta a probabilidade de pegar valores piores
# Alfa - parametro - vai diminuindo a temperatura da tempera simulada à cada iteração
# maxIteração ???? - parametro - será que é necessário inserir um máximo de iteração?


# def temperaSimulada(values, wights, capacity, alfa, temperature):




# Função para gerar uma solução inicial válida
def initial_solution(items, capacity):
    n = len(items)
    solution = [0] * n
    total_weight = 0
    for i in range(n):
        if total_weight + items[i][1] <= capacity:
            solution[i] = 1
            total_weight += items[i][1]
    return solution

# Função para calcular o valor total da solução
def evaluate(solution, items):
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_value += items[i][0]
            total_weight += items[i][1]
    return total_value if total_weight <= capacity else 0

# Função para gerar um vizinho (modificar um item aleatório)
def generate_neighbor(solution, items, capacity):
    neighbor = solution[:]
    
    # Escolhe um número aleatório de itens para alterar (pode alterar mais de um)
    num_changes = random.randint(1, len(solution) // 2)  # Pode alterar até metade dos itens
    indices = random.sample(range(len(solution)), num_changes)
    
    # Inverte os itens selecionados
    for index in indices:
        neighbor[index] = 1 - neighbor[index]
    
    # Calcula o peso total da nova solução
    total_weight = sum([neighbor[i] * items[i][1] for i in range(len(neighbor))])
    
    # Se o peso da solução for válido, retorna o vizinho
    if total_weight <= capacity:
        return neighbor
    
    # Tenta corrigir a solução se o peso for inválido
    for index in indices:
        if neighbor[index] == 1:  # Se o item foi adicionado, remove-o
            neighbor[index] = 0
            total_weight = sum([neighbor[i] * items[i][1] for i in range(len(neighbor))])
            if total_weight <= capacity:
                return neighbor
    
    # Se ainda assim não for válido, retorna a solução original
    return solution

# Função de têmpera simulada
def simulated_annealing_knapsack(items, capacity, T_0, alpha):
    n = len(items)
    solution = initial_solution(items, capacity)  # Gerar solução inicial válida
    current_value = evaluate(solution, items)
    
    T = T_0  # Temperatura inicial
    
    while(T > 1e-8):
        # Gerar uma solução vizinha
        neighbor = generate_neighbor(solution, items, capacity)
        neighbor_value = evaluate(neighbor, items)
        # print('neighbor_value', neighbor_value)
        # Calcular a diferença de valor
        delta_E = neighbor_value - current_value
        
        # Aceitar a nova solução se for melhor ou com uma certa probabilidade
        if delta_E > 0 or random.random() < math.exp(delta_E / T):
            solution = neighbor
            current_value = neighbor_value
        
        # Reduzir a temperatura
        T = T * alpha
        
        # Critério de parada (opcional)
        # if T < 1e-8:
        #     break
    
    return solution, current_value

def objective(trial):
    T_0 = trial.suggest_float('T_0', 1000, 12000)
    alpha = trial.suggest_float('alpha', 0.8, 0.999)
    # max_iter = trial.suggest_int('max_iter', 100, 2000)
    
    # Executa o algoritmo de têmpera simulada
    _, result_value = simulated_annealing_knapsack(items, capacity, T_0, alpha)
    
    # Avalia a solução relativa à solução ótima
    return abs(401 - result_value)  # Minimiza a diferença da solução ótima


values = [
  360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
  78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
  87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
  312
]
weights = [
  [7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
   42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
   3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13],
]
capacity = [850]

items = list(zip(values, weights))

T_0 = 7476.989953418831  # Temperatura inicial
alpha = 0.8793924680321088  # Taxa de resfriamento
max_iter = 1293  # Número máximo de iterações

# solution, max_value = simulated_annealing_knapsack(items, capacity, T_0, alpha)
# print(f"Melhor solução encontrada: {solution}")
# print(f"Valor máximo obtido: {max_value}")


# Executa a otimização
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)

# Mostra os melhores parâmetros
print(f"Melhores parâmetros encontrados: {study.best_params}")
# optuna.visualization.plot_optimization_history(study)
# optuna.visualization.plot_param_importances(study)
# plt.show()  # Adiciona plt.show() para exibir os gráficos
# Melhores parâmetros encontrados: {'T_0': 9384.106336261832, 'alpha': 0.9472087008472314}
# Melhores parâmetros encontrados: {'T_0': 5294.666017673908, 'alpha': 0.9658615944154878}
# Melhores parâmetros encontrados: {'T_0': 8517.807738678814, 'alpha': 0.9872587599656775}
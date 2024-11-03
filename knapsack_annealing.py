import numpy as np
import time
import optuna

def calcular_valor_e_tamanho(lista_itens, valores, tamanhos, tamanho_maximo):
    """
    Esta função calcula o valor total e o tamanho dos itens selecionados (lista_itens) 
    com base em seus valores e tamanhos. Se o tamanho total exceder o permitido, 
    o valor é definido como 0.
    
    Args:
        lista_itens (array): Array de 0s e 1s indicando os itens selecionados.
        valores (array): Array de valores dos itens.
        tamanhos (array): Array de tamanhos dos itens.
        tamanho_maximo (int): Tamanho máximo permitido da mochila.
    
    Retorna:
        tuple: Valor total e tamanho dos itens selecionados.
    """
    valor_total = 0.0
    tamanho_total = 0.0
    n = len(lista_itens)

    # Calcula o valor e o tamanho total com base nos itens selecionados
    for i in range(n):
        if lista_itens[i] == 1:  # Se o item está selecionado
            valor_total += valores[i]
            tamanho_total += tamanhos[i]

    # Se o tamanho total excede o limite, invalida a seleção
    if tamanho_total > tamanho_maximo:
        valor_total = 0.0

    return valor_total, tamanho_total

def gerar_solucao_adj(lista_itens, rnd):
    """
    Gera uma solução vizinha alterando aleatoriamente a inclusão (1 para 0 ou 0 para 1) 
    de um item no pacote atual.
    
    Args:
        lista_itens (array): Solução de embalagem atual.
        rnd (RandomState): Gerador de números aleatórios.
    
    Retorna:
        array: Nova solução de embalagem adjacente à atual.
    """
    n = len(lista_itens)
    nova_solucao = np.copy(lista_itens)

    # Seleciona aleatoriamente um item para mudar (1 para 0 ou 0 para 1)
    i = rnd.randint(n)
    nova_solucao[i] = 1 if lista_itens[i] == 0 else 0

    return nova_solucao

def tempera_simulada(n_itens, rnd, valores, tamanhos, tamanho_maximo, temp_inicial, alpha):
    """
    Resolve o problema da mochila usando têmpera simulada.
    
    Args:
        n_itens (int): Número de itens disponíveis.
        rnd (RandomState): Gerador de números aleatórios.
        valores (array): Array de valores dos itens.
        tamanhos (array): Array de tamanhos dos itens.
        tamanho_maximo (int): Tamanho máximo permitido da mochila.
        temp_inicial (float): Temperatura inicial da têmpera.
        alpha (float): Taxa de resfriamento da temperatura.
    
    Retorna:
        array: A melhor solução de embalagem encontrada.
    """
    # Configuração inicial
    temperatura_atual = temp_inicial
    packing_atual = np.ones(n_itens, dtype=np.int64)  # Começa com todos os itens incluídos
    valor_atual, tamanho_atual = calcular_valor_e_tamanho(packing_atual, valores, tamanhos, tamanho_maximo)
    
    print("Mochila Inicial: ", packing_atual)

    iteracao = 0

    # Executa enquanto a temperatura for maior que o limite
    while temperatura_atual > 0.00001:
        # Gera uma solução vizinha
        adj_packing = gerar_solucao_adj(packing_atual, rnd)
        valor_adj, _ = calcular_valor_e_tamanho(adj_packing, valores, tamanhos, tamanho_maximo)

        # Se a solução vizinha for melhor, aceita-a
        if valor_adj > valor_atual:
            packing_atual = adj_packing
            valor_atual = valor_adj
        else:
            # Caso contrário, aceita com uma probabilidade baseada na temperatura
            prob_aceitacao = np.exp((valor_adj - valor_atual) / temperatura_atual)
            if rnd.random() < prob_aceitacao:
                packing_atual = adj_packing
                valor_atual = valor_adj

        # Imprime o progresso periodicamente
        if iteracao % 50 == 0:
            print(f"Iteração {iteracao}: Valor atual = {valor_atual:.0f}, Temperatura = {temperatura_atual:.2f}")

        # Resfriamento da temperatura
        temperatura_atual = max(0.00001, temperatura_atual * alpha)

        iteracao += 1

    return packing_atual



def objective(trial):
    valores = np.array([360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
                        78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
                        87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
                        312])
    tamanhos = np.array([7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
                         42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
                         3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13])
    tamanho_maximo = 850

    # Parâmetros a serem otimizados
    temp_inicial = trial.suggest_float("temp_inicial", 100, 10000)
    alpha = trial.suggest_float("alpha", 0.9, 0.9999)
    rnd = np.random.RandomState(seed=int(time.time()))  

    melhor_packing = tempera_simulada(
        n_itens=len(valores),
        rnd=rnd,
        valores=valores,
        tamanhos=tamanhos,
        tamanho_maximo=tamanho_maximo,
        temp_inicial=temp_inicial,
        alpha=alpha
    )
    melhor_valor, _ = calcular_valor_e_tamanho(melhor_packing, valores, tamanhos, tamanho_maximo)

    return melhor_valor

def main():
    print("Otimizando parâmetros com Optuna...")
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=50)

    print("Melhores parâmetros:")
    print(study.best_params)

    print("Melhor valor de solução:")
    print(study.best_value)




# def main():
#     """
#     Função principal para configurar e executar a demonstração de têmpera simulada para o problema da mochila.
#     """
#     # Definindo os valores e tamanhos dos itens
#     valores = np.array([360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
#                         78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
#                         87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
#                         312])
#     tamanhos = np.array([7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
#                          42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
#                          3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13])
#     tamanho_maximo = 850

#     print("Valores dos itens: ", valores)
#     print("Tamanhos dos itens: ", tamanhos)

#     # Parâmetros para a têmpera simulada 
#     rnd = np.random.RandomState(5)  # Semente aleatória para reprodutibilidade
#     temp_inicial = 10000.0
#     alpha = 0.8  # Taxa de resfriamento

#     print(f"Configurações: temp_inicial = {temp_inicial}, alpha = {alpha}")
#     melhor_packing = tempera_simulada(50, rnd, valores, tamanhos, tamanho_maximo, temp_inicial, alpha)
#     print("----------------------------------")
#     print("Melhor solução encontrada: ", melhor_packing)
#     melhor_valor, melhor_tamanho = calcular_valor_e_tamanho(melhor_packing, valores, tamanhos, tamanho_maximo)
#     print(f"Valor total da melhor embalagem = {melhor_valor:.1f}")
#     print(f"Tamanho total da melhor embalagem = {melhor_tamanho:.1f}")

if __name__ == "__main__":
    main()

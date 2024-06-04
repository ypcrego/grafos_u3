import os # para manipulação dos arquivos
import random # para o algoritmo
import math # para calcular log(n)
import time # para contabilizar o tempo de execução
import copy # para permitir múltiplas iterações do algoritmo


def list_files(directory):
    files = os.listdir(directory)
    return [file for file in files if os.path.isfile(os.path.join(directory, file))]


def get_description_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip().startswith('# Descrição:'):
                return line.strip()[13:]
    return "Sem descrição."


def choose_file(files):
    print("-----------------------------------------------------\nArquivos disponíveis:\n")
    for i, (file, description) in enumerate(files, start=1):
        print(f"{i}: {file} - {description}")
    
    while True:
        choice = input("\nEscolha o número do arquivo que deseja usar: \n-----------------------------------------------------\n")
        try:
            choice = int(choice)
            if 1 <= choice <= len(files):
                return files[choice - 1][0]
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

# Diretório/pasta dos casos de teste
directory = 'test_cases'


# Listar arquivos disponíveis
files = list_files(directory)
files_with_descriptions = [(file, get_description_from_file(os.path.join(directory, file))) for file in files]

if not files_with_descriptions:
    print("Nenhum arquivo encontrado no diretório.")
else:
    chosen_file = choose_file(files_with_descriptions)
    print("Você escolheu o arquivo:", chosen_file)

# Leitura e construção do grafo (como dicionário de adjacência)
def read_graph_as_dict(filename):

    with open(filename, 'r', encoding='utf-8') as file:
        graph = {}

        # Itera sobre as linhas do arquivo
        for line in file:
            # Remoção de espaços em branco e quebras de linha no início e fim da linha
            line = line.strip()
            
            if line and not line.startswith('#'):
                # Divide a linha em uma lista de inteiros
                vertices = list(map(int, line.split()))
                vertex = vertices[0]
                adjacent_vertices = vertices[1:]
                
                # Adiciona as arestas em ambos os vértices (grafo não-direcionado)
                if vertex not in graph:
                    graph[vertex] = []
                for adj_vertex in adjacent_vertices:
                    graph[vertex].append(adj_vertex)
                    if adj_vertex not in graph:
                        graph[adj_vertex] = []
                    graph[adj_vertex].append(vertex)
    
    return graph

# Caminho completo para o arquivo
filename = os.path.join(directory, chosen_file)

# Grafo na forma de dicionário de adjacência
dict_adj = read_graph_as_dict(filename)
CONST_N_VERTICES = len(dict_adj)


# Contrai a aresta entre os vértices u e v
def contract(graph, u, v):
    # Remove o vértice v do grafo e substitui todas as ocorrências de v por u
    for vertex in graph[v]:
        if vertex != u:
            graph[u].append(vertex)
            graph[vertex].append(u)
        graph[vertex].remove(v)
    del graph[v]


def karger(graph):
    # Enquanto houver mais de 2 vértices no grafo
    while len(graph) > 2:
    
        # Escolhe uma aresta aleatória
        u = random.choice(list(graph.keys()))
        v = random.choice(graph[u])
        
        # Contrai a aresta
        contract(graph, u, v)
    
    # Retorna o tamanho do corte mínimo
    return len(graph[list(graph.keys())[0]])


# Função para executar o algoritmo Karger várias vezes
def run_karger_multiple_times(graph, num_trials):
    min_cut = float('inf') # Inicializa o menor corte encontrado como infinito
    start_time = time.time() # Inicializa a contagem de tempo

    for _ in range(num_trials):
        graph_copy = copy.deepcopy(graph) # Outros tipos de cópia não reinicializam corretamente o grafo
        cut = karger(graph_copy)

        if cut < min_cut: # Verifica se o corte atual é menor que o menor corte encontrado até agora
            min_cut = cut
            min_cut_count = 1
        elif cut == min_cut: # Se o corte atual for igual ao menor corte encontrado, incrementa a contagem de quantas vezes o corte foi encontrado
            min_cut_count += 1

    end_time = time.time() # Termina a contagem de tempo
    execution_time = end_time - start_time # Calcula o tempo de execução
    return min_cut, min_cut_count, execution_time



def choose_iterations():
    default = int(math.comb(CONST_N_VERTICES, 2) * math.log(CONST_N_VERTICES))
    user_choice = input(f"Pressione Enter para usar o número padrão de iterações ({default}), ou digite outro número para escolher o número de iterações: ")
    if user_choice:
        try:
            num_iterations = int(user_choice)
            if num_iterations <= 0:
                raise ValueError
            return num_iterations
        except ValueError:
            print("Entrada inválida. Usando o número padrão de iterações.")
    return default


# Número de vezes que o algoritmo será executado. O recomendado é: n^2 * ln(n); n = |V| de G = (V, E).
num_trials = int(choose_iterations())

print(f"-----------------------------------------------------\n|V| = {CONST_N_VERTICES};\t {num_trials} ITERAÇÕES SERÃO FEITAS.\nProcessando...")
min_cut, min_cut_count, execution_time = run_karger_multiple_times(dict_adj, num_trials)


print(f"\n\n\nO menor corte encontrado para o arquivo {chosen_file} foi de tamanho {min_cut}, ocorrendo {min_cut_count} vezes em {num_trials} tentativas.")
print(f"Tempo de execução total: {execution_time:.5f} segundos.")

save_report = input("\n\nDeseja salvar o relatório em um arquivo? (s/n): ").lower()

if save_report == 's':

    report_directory = 'reports'

    # Cria o diretório se não existir
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)

    # Nome do arquivo
    report_filename = os.path.splitext(chosen_file)[0] + '_report.txt'
    report_filepath = os.path.join(report_directory, report_filename)

    # Escrita no arquivo
    with open(report_filepath, 'w', encoding='utf-8') as report_file:
        report_file.write(f"Menor corte encontrado para o arquivo {chosen_file}:\n")
        report_file.write(f"Tamanho do corte: {min_cut}\n")
        report_file.write(f"Ocorreu {min_cut_count} vezes em {num_trials} tentativas.\n")
        report_file.write(f"Tempo de execução total: {execution_time:.5f} segundos.\n")

    print(f"Relatório salvo em: {report_filepath}")
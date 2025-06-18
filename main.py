from services.cluster import Cluster
from services.calcular import Calcular
from models.aluno import Aluno
import matplotlib.pyplot as plt
import random
import string
import math
from typing import Tuple, Dict, List

def generate_random_name():
    """Gera um nome aleatório para um aluno."""
    first_names = ["Ana", "Bruno", "Carla", "Daniel", "Eva", "Felipe", "Gabriela", "Hugo", "Isabela", "Joao", "Karen", "Lucas", "Mariana", "Nuno", "Olivia", "Pedro", "Quiteria", "Rafael", "Sofia", "Tiago", "Ursula", "Vitor", "Wanessa", "Xavier", "Yasmin", "Zeca"]
    last_names = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Fernandes", "Pereira", "Almeida", "Costa", "Rodrigues", "Martins", "Carvalho", "Gomes", "Ribeiro", "Monteiro", "Freitas", "Machado", "Dias", "Nunes", "Melo"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_student_raw_data():
    """Gera dados brutos de um aluno (não normalizados)."""
    name = generate_random_name()
    idade = random.randint(15, 100)
    nota = round(random.uniform(0.0, 10.0), 2)
    faltas = round(random.uniform(0.0, 10.0), 2)
    return Aluno(name, idade, nota, faltas)

def get_manual_student_input_raw_data():
    """Solicita ao usuário os dados brutos do aluno."""
    while True:
        try:
            name = input("Digite o nome do aluno (ou 'pronto' para finalizar a entrada manual): ")
            if name.lower() == 'pronto':
                return None
            idade = int(input(f"Digite a idade de {name} (15-100): "))
            if not (15 <= idade <= 100):
                print("A idade deve estar entre 15 e 100.")
                continue
            nota = float(input(f"Digite a nota de {name} (0.0-10.0): "))
            if not (0.0 <= nota <= 10.0):
                print("A nota deve estar entre 0.0 e 10.0.")
                continue
            faltas = float(input(f"Digite as faltas de {name} (0.0-10.0): "))
            if not (0.0 <= faltas <= 10.0):
                print("As faltas devem estar entre 0.0 e 10.0.")
                continue
            return Aluno(name, idade, nota, faltas)
        except ValueError:
            print("Entrada inválida. Por favor, digite números válidos para idade, nota e faltas.")

def normalize_data(students: list[Aluno]):
    """Normaliza os dados dos alunos para a escala de 0 a 1."""
    if not students:
        return {} 

    min_idade = min(s.idade for s in students)
    max_idade = max(s.idade for s in students)
    min_nota = min(s.nota for s in students)
    max_nota = max(s.nota for s in students)
    min_faltas = min(s.faltas for s in students)
    max_faltas = max(s.faltas for s in students)

    range_idade = max_idade - min_idade if max_idade - min_idade > 0 else 1
    range_nota = max_nota - min_nota if max_nota - min_nota > 0 else 1
    range_faltas = max_faltas - min_faltas if max_faltas - min_faltas > 0 else 1

    for student in students:
        student.idade_norm = (student.idade - min_idade) / range_idade
        student.nota_norm = (student.nota - min_nota) / range_nota
        student.faltas_norm = (student.faltas - min_faltas) / range_faltas

    return {
        'idade': (min_idade, max_idade),
        'nota': (min_nota, max_nota),
        'faltas': (min_faltas, max_faltas)
    }

def denormalize_centroid(normalized_centroid: Tuple[float, float, float], min_max_values: Dict[str, Tuple[float, float]]):
    """Desnormaliza um centróide para a escala original para visualização."""
    denorm_idade = normalized_centroid[0] * (min_max_values['idade'][1] - min_max_values['idade'][0]) + min_max_values['idade'][0]
    denorm_nota = normalized_centroid[1] * (min_max_values['nota'][1] - min_max_values['nota'][0]) + min_max_values['nota'][0]
    denorm_faltas = normalized_centroid[2] * (min_max_values['faltas'][1] - min_max_values['faltas'][0]) + min_max_values['faltas'][0]
    return (denorm_idade, denorm_nota, denorm_faltas)

def perform_kmeans_iteration(clusters: List[Cluster], all_students: List[Aluno], calculator: Calcular, max_iterations=50, convergence_threshold=1e-4):
    print("\nIniciando iterações de K-Means para refinamento...")
    for iteration in range(max_iterations): 
        old_centroids = [cluster.centroide for cluster in clusters] #

        students_for_reassignment = []
        for cluster in clusters:
            students_for_reassignment.extend(cluster.alunos)
            cluster.alunos = [] 
        

        for student in students_for_reassignment: 
            closest_cluster = calculator.definir_cluster_mais_proximo(student) #
            if closest_cluster:
                closest_cluster.adicionar_aluno(student)
        
        for cluster in clusters:
            cluster.calcular_centroide()

        converged = True
        if len(old_centroids) != len(clusters):
            converged = False
        else:
            for i in range(len(clusters)):
                current_centroid = clusters[i].centroide
                previous_centroid = old_centroids[i]
                
                if (not math.isclose(current_centroid[0], previous_centroid[0], rel_tol=convergence_threshold) or
                    not math.isclose(current_centroid[1], previous_centroid[1], rel_tol=convergence_threshold) or
                    not math.isclose(current_centroid[2], previous_centroid[2], rel_tol=convergence_threshold)):
                    converged = False
                    break
        
        print(f"  Iteração {iteration + 1} concluída. Centroides atualizados. Convergido: {converged}")
        if converged:
            print("  Algoritmo K-Means convergiu.")
            break
    print("Refinamento de cluster concluído.")


def main():
    all_students_raw_data: list[Aluno] = []

    add_manual = input("Deseja adicionar alunos manualmente? (sim/nao): ").lower()
    if add_manual == 'sim':
        print("\nAdicionando alunos manualmente...")
        while True:
            student = get_manual_student_input_raw_data()
            if student is None:
                break
            all_students_raw_data.append(student)
            print(f"Aluno adicionado manualmente: {student.nome}")

    add_automatic = input("Deseja adicionar alunos automaticamente? (sim/nao): ").lower()
    if add_automatic == 'sim':
        num_auto_students = int(input("Digite o número de alunos para gerar automaticamente: "))
        print(f"\nGerando {num_auto_students} alunos automaticamente...")
        for _ in range(num_auto_students):
            all_students_raw_data.append(generate_random_student_raw_data())

    if not all_students_raw_data:
        print("Nenhum aluno para processar. Saindo.")
        return

    # --- PASSO DE NORMALIZAÇÃO ---
    print("\nNormalizando dados dos alunos...")
    min_max_values = normalize_data(all_students_raw_data)
    if not min_max_values: 
        print("Erro na normalização: Nenhum aluno válido para processar.")
        return

    initial_clusters: list[Cluster] = []

    num_initial_centroids = int(input("Digite o número de centroides iniciais que você deseja criar: "))
    if num_initial_centroids <= 0:
        print("O número de centroides iniciais deve ser no mínimo 1. Saindo.")
        return

    print("Gerando centroides iniciais aleatórios (na escala normalizada)...")
    for _ in range(num_initial_centroids):
        idade_c_norm = random.uniform(0.0, 1.0)
        nota_c_norm = random.uniform(0.0, 1.0)
        faltas_c_norm = random.uniform(0.0, 1.0)
        initial_clusters.append(Cluster((idade_c_norm, nota_c_norm, faltas_c_norm)))
        
        denorm_c = denormalize_centroid((idade_c_norm, nota_c_norm, faltas_c_norm), min_max_values)
        print(f"Centróide inicial criado (normalizado): ({idade_c_norm:.2f}, {nota_c_norm:.2f}, {faltas_c_norm:.2f}) (Original: Idade:{denorm_c[0]:.0f}, Nota:{denorm_c[1]:.1f}, Faltas:{denorm_c[2]:.1f})")


    calculate = Calcular(initial_clusters)

    NEW_CENTROID_DISTANCE_THRESHOLD = 0.6

    print("\nAtribuindo alunos aos clusters e criando novos centroides dinamicamente...")
    for student_to_assign in all_students_raw_data:
        
        if not calculate.clusters:
            new_cluster_centroid_norm = (student_to_assign.idade_norm, student_to_assign.nota_norm, student_to_assign.faltas_norm)
            new_cluster = Cluster(new_cluster_centroid_norm)
            new_cluster.adicionar_aluno(student_to_assign)
            calculate.clusters.append(new_cluster)
            print(f"Adicionado {student_to_assign.nome} (primeiro aluno) e criado um novo cluster: {new_cluster_centroid_norm}")
            perform_kmeans_iteration(calculate.clusters, all_students_raw_data[:all_students_raw_data.index(student_to_assign) + 1], calculate, max_iterations=10, convergence_threshold=1e-4) # Um pequeno refinamento
            continue

        closest_cluster = calculate.definir_cluster_mais_proximo(student_to_assign)
        
        distances = [student_to_assign.calcular_distancia_euclidiana(c.centroide) for c in calculate.clusters]
        
        create_new_centroid = False
        min_distance = float('inf')
        if distances:
            min_distance = min(distances)
            if min_distance > NEW_CENTROID_DISTANCE_THRESHOLD:
                create_new_centroid = True
        
        if create_new_centroid:
            new_cluster_centroid_norm = (student_to_assign.idade_norm, student_to_assign.nota_norm, student_to_assign.faltas_norm)
            new_cluster = Cluster(new_cluster_centroid_norm)
            new_cluster.adicionar_aluno(student_to_assign)
            calculate.clusters.append(new_cluster)
            print(f"Adicionado {student_to_assign.nome} e criado automaticamente novo cluster {len(calculate.clusters)} com centróide: {new_cluster_centroid_norm} (dist_min: {min_distance:.2f})")
            
            # --- NOVO BLOCO: Recalcula e reatribui todos os alunos após a criação de um novo centróide ---
            # Isso é crucial para que alunos existentes possam "pular" para o novo cluster se ele for mais próximo.
            perform_kmeans_iteration(calculate.clusters, all_students_raw_data[:all_students_raw_data.index(student_to_assign) + 1], calculate, max_iterations=10, convergence_threshold=1e-4)
            
        elif closest_cluster:
            closest_cluster.adicionar_aluno(student_to_assign)
            print(f"Adicionado {student_to_assign.nome} ao cluster existente com centróide: {closest_cluster.centroide} (dist_min: {min_distance:.2f})")
        else:
            print(f"Não foi possível atribuir {student_to_assign.nome} a nenhum cluster.")

    for cluster in calculate.clusters:
        cluster.calcular_centroide()


    print("\nRefinando clusters (recálculo iterativo de centróides)...")
    MAX_ITERATIONS = 50 
    CONVERGENCE_THRESHOLD = 1e-4 

    perform_kmeans_iteration(calculate.clusters, all_students_raw_data, calculate, max_iterations=MAX_ITERATIONS, convergence_threshold=CONVERGENCE_THRESHOLD)
            

    cores = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'black', 'brown', 'pink', 'gray']
    plt.figure(figsize=(12, 8))

    for idx, cluster in enumerate(calculate.clusters):
        if cluster.alunos:
            notas = [aluno.nota for aluno in cluster.alunos]
            faltas = [aluno.faltas for aluno in cluster.alunos]
            plt.scatter(notas, faltas, color=cores[idx % len(cores)], label=f'Cluster {idx+1} (Alunos: {len(cluster.alunos)})', alpha=0.7)
        
        denormalized_centroid = denormalize_centroid(cluster.centroide, min_max_values)
        
        plt.scatter(denormalized_centroid[1], denormalized_centroid[2], 
                    color=cores[idx % len(cores)], 
                    marker='X', s=250, edgecolor='black', linewidth=1.5,
                    label=f'Centróide {idx+1}' if cluster.alunos else f'Centróide {idx+1} (Vazio)')


    plt.xlabel('Nota')
    plt.ylabel('Faltas')
    plt.title('Clusters de Alunos Dinâmicos (Nota vs. Faltas) - Dados Originalmente Dimensionados')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
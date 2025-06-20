from services.cluster import Cluster
from services.calcular import Calcular
from models.aluno import Aluno
import matplotlib.pyplot as plt
import random
import math
from typing import Tuple, Dict, List
from utils.normalize import normalize_data, denormalize_centroid
from utils.input_helpers import get_manual_student_input_raw_data, generate_random_student_raw_data

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

    calculate = Calcular(initial_clusters)

    for student_to_assign in all_students_raw_data:
        if not calculate.clusters:
            new_cluster_centroid_norm = (student_to_assign.idade_norm, student_to_assign.nota_norm, student_to_assign.faltas_norm)
            new_cluster = Cluster(new_cluster_centroid_norm)
            new_cluster.adicionar_aluno(student_to_assign)
            calculate.clusters.append(new_cluster)
            continue

        closest_cluster = calculate.definir_cluster_mais_proximo(student_to_assign)

        distances = [student_to_assign.calcular_distancia_euclidiana(c.centroide) for c in calculate.clusters]
        create_new_centroid = False
        if distances:
            min_distance = min(distances)
            if min_distance > 0.6:
                create_new_centroid = True

        if create_new_centroid:
            new_cluster_centroid_norm = (student_to_assign.idade_norm, student_to_assign.nota_norm, student_to_assign.faltas_norm)
            new_cluster = Cluster(new_cluster_centroid_norm)
            new_cluster.adicionar_aluno(student_to_assign)
            calculate.clusters.append(new_cluster)
        elif closest_cluster:
            closest_cluster.adicionar_aluno(student_to_assign)

    for cluster in calculate.clusters:
        cluster.calcular_centroide()

    cores = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'black', 'brown', 'pink', 'gray']
    plt.figure(figsize=(12, 8))

    for idx, cluster in enumerate(calculate.clusters):
        if cluster.alunos:
            notas = [aluno.nota for aluno in cluster.alunos]
            faltas = [aluno.faltas for aluno in cluster.alunos]
            plt.scatter(notas, faltas, color=cores[idx % len(cores)], label=f'Cluster {idx+1} (Alunos: {len(cluster.alunos)})', alpha=0.7)

    plt.xlabel('Nota')
    plt.ylabel('Faltas')
    plt.title('Clusters de Alunos Dinâmicos (Nota vs. Faltas)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    while True:
        print("\n--- ADICIONAR NOVO ALUNO ---")
        novo_aluno = get_manual_student_input_raw_data()
        if novo_aluno is None:
            print("Encerrando adição de novos alunos.")
            break

        novo_aluno.idade_norm = (novo_aluno.idade - min_max_values['idade'][0]) / (min_max_values['idade'][1] - min_max_values['idade'][0])
        novo_aluno.nota_norm = (novo_aluno.nota - min_max_values['nota'][0]) / (min_max_values['nota'][1] - min_max_values['nota'][0])
        novo_aluno.faltas_norm = (novo_aluno.faltas - min_max_values['faltas'][0]) / (min_max_values['faltas'][1] - min_max_values['faltas'][0])

        cluster_mais_proximo = calculate.definir_cluster_mais_proximo(novo_aluno)
        if cluster_mais_proximo:
            cluster_mais_proximo.adicionar_aluno(novo_aluno)
            print(f"{novo_aluno.nome} foi adicionado ao cluster com centróide: {cluster_mais_proximo.centroide}")
        else:
            print(f"Não foi possível classificar o aluno {novo_aluno.nome}")

        plt.figure(figsize=(12, 8))
        for idx, cluster in enumerate(calculate.clusters):
            if cluster.alunos:
                notas = [aluno.nota for aluno in cluster.alunos]
                faltas = [aluno.faltas for aluno in cluster.alunos]
                plt.scatter(notas, faltas, color=cores[idx % len(cores)], label=f'Cluster {idx+1} (Alunos: {len(cluster.alunos)})', alpha=0.7)

        plt.xlabel('Nota')
        plt.ylabel('Faltas')
        plt.title('Clusters Atualizados Após Novo Aluno')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
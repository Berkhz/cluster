from services.leitorcsv import LeitorCSV
from services.centroide_inicial import centroide_inicial
from services.cluster import Cluster
from services.calcular import Calcular
import matplotlib.pyplot as plt


def main():
    csv_file = 'alunos1.csv'
    students = LeitorCSV.ler_csv(csv_file)
    initialCentroids = centroide_inicial(students)
    initialClusters = [Cluster(initialCentroids[0]), Cluster(initialCentroids[1])]
    calculate = Calcular(initialClusters)
    
    for student in students:
        cluster = calculate.definir_cluster(student, initialClusters[0], initialClusters[1])
    
    cores = ['red', 'blue', 'green', 'orange', 'purple']
    for idx, cluster in enumerate(calculate.clusters):
        notas = [aluno.nota for aluno in cluster.alunos]
        faltas = [aluno.faltas for aluno in cluster.alunos]
        plt.scatter(notas, faltas, color=cores[idx % len(cores)], label=f'Cluster {idx+1}')
        plt.scatter(cluster.centroide[1], cluster.centroide[2], color=cores[idx % len(cores)], marker='X', s=200, edgecolor='black')

    plt.xlabel('Nota')
    plt.ylabel('Faltas')
    plt.title('Clusters de Alunos')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
from services.cluster import Cluster
from typing import Tuple, List
from models.aluno import Aluno

class Calcular:
    
    def __init__(self, clusters: List[Cluster]):
        self.clusters = clusters
    
    def definir_cluster_mais_proximo(self, aluno: Aluno) -> Cluster | None:
        """
        Determina o cluster mais próximo para um determinado aluno com base na distância euclidiana
        dos centróides do cluster.
        """
        if not self.clusters:
            return None

        distances_to_clusters = []
        for cluster in self.clusters:
            distance = aluno.calcular_distancia_euclidiana(cluster.centroide)
            distances_to_clusters.append((cluster, distance))
        
        distances_to_clusters.sort(key=lambda x: x[1])
        
        if len(distances_to_clusters) == 0:
            return None
        
        return distances_to_clusters[0][0]

    def calcular_novos_clusters(self):
        """
        Recalcula o centróide para cada cluster existente com base em seus membros atuais.
        Este método seria normalmente chamado iterativamente em um algoritmo K-Means completo.
        """
        for cluster in self.clusters:
            cluster.calcular_centroide()
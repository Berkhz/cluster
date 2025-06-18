from models.aluno import Aluno
from typing import Tuple, List

class Cluster:     
        
    def __init__(self, centroide: Tuple[float, float, float]):
        self.centroide = centroide
        self.alunos: List[Aluno] = []
    
    def adicionar_aluno(self, aluno: Aluno):
        self.alunos.append(aluno)
       
    def calcular_centroide(self):
        idade_total_norm: float = 0.0
        nota_total_norm: float = 0.0
        faltas_total_norm: float = 0.0
        quantidade: float = len(self.alunos)
        
        if quantidade == 0:
            return 
        for aluno in self.alunos:
            idade_total_norm += aluno.idade_norm
            nota_total_norm += aluno.nota_norm
            faltas_total_norm += aluno.faltas_norm
        
        self.centroide = (
            idade_total_norm / quantidade,
            nota_total_norm / quantidade,
            faltas_total_norm / quantidade
        )
    
    def __str__(self):
        return f"Centróide: {self.centroide}, Alunos: {len(self.alunos)}"
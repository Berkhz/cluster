# berkhz/cluster/cluster-a50bc9bf5a4af1eff4613df126459fc6f338604c/models/aluno.py
from dataclasses import dataclass
from services.distancia_euclidiana import distancia_euclidiana
from typing import Tuple, Dict

@dataclass
class Aluno:
    nome: str
    idade: int
    nota: float
    faltas: float
    
    # Adicionar campos para os valores normalizados
    idade_norm: float = 0.0
    nota_norm: float = 0.0
    faltas_norm: float = 0.0

    def calcular_distancia_euclidiana(self, centroide: Tuple[float, float, float]): # Centróide agora usa floats para todas as dimensões
        # Usar os valores normalizados para o cálculo da distância
        return distancia_euclidiana(centroide, (self.idade_norm, self.nota_norm, self.faltas_norm))

    def __str__(self):
        return f"{self.nome} (Idade: {self.idade}, Nota: {self.nota}, Faltas: {self.faltas})"
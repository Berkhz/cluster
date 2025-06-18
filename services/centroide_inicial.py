import random
from typing import List
from models.aluno import Aluno

def centroide_inicial_aleatorio(alunos: List[Aluno], n: int = 2):
    """
    Seleciona N alunos aleatórios para servir como centróides iniciais.
    Isso ainda pode ser útil para uma configuração inicial totalmente automatizada, se não houver entrada do usuário.
    """
    if len(alunos) < n:
        raise ValueError("Não há alunos suficientes para selecionar centróides iniciais.")
    
    centroides_iniciais_alunos = random.sample(alunos, n)
    return [(a.idade, a.nota, a.faltas) for a in centroides_iniciais_alunos]
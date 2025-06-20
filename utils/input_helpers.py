import random
from models.aluno import Aluno

def generate_random_name():
    first_names = ["Ana", "Bruno", "Carla", "Daniel", "Eva", "Felipe", "Gabriela", "Hugo", "Isabela", "Joao", "Karen", "Lucas", "Mariana", "Nuno", "Olivia", "Pedro", "Quiteria", "Rafael", "Sofia", "Tiago", "Ursula", "Vitor", "Wanessa", "Xavier", "Yasmin", "Zeca"]
    last_names = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Fernandes", "Pereira", "Almeida", "Costa", "Rodrigues", "Martins", "Carvalho", "Gomes", "Ribeiro", "Monteiro", "Freitas", "Machado", "Dias", "Nunes", "Melo"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_student_raw_data():
    name = generate_random_name()
    idade = random.randint(15, 100)
    nota = round(random.uniform(0.0, 10.0), 2)
    faltas = round(random.uniform(0.0, 10.0), 2)
    return Aluno(name, idade, nota, faltas)

def get_manual_student_input_raw_data():
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
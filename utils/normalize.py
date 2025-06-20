def normalize_data(students):
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

def denormalize_centroid(normalized_centroid, min_max_values):
    denorm_idade = normalized_centroid[0] * (min_max_values['idade'][1] - min_max_values['idade'][0]) + min_max_values['idade'][0]
    denorm_nota = normalized_centroid[1] * (min_max_values['nota'][1] - min_max_values['nota'][0]) + min_max_values['nota'][0]
    denorm_faltas = normalized_centroid[2] * (min_max_values['faltas'][1] - min_max_values['faltas'][0]) + min_max_values['faltas'][0]
    return (denorm_idade, denorm_nota, denorm_faltas)
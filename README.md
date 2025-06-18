# 📊 Projeto de Clusterização de Alunos com K-Means

Este projeto realiza a **clusterização de alunos** com base em dados como **idade, nota e faltas**, utilizando o algoritmo **K-Means** e visualização via **matplotlib**.

## 🧠 Objetivo

Agrupar alunos de forma automática em dois ou mais grupos, de acordo com a semelhança entre seus dados, e exibir o resultado graficamente.

---

## 📁 Estrutura do Projeto

```
.
├── main.py
├── alunos1.csv
├── models/
│   └── aluno.py
├── services/
│   ├── leitorcsv.py
│   ├── centroide_inicial.py
│   ├── cluster.py
│   └── calcular.py
```

---

## 🧪 Funcionalidades

- Leitura de dados de alunos via arquivo CSV.
- Cálculo de distância euclidiana entre pontos e centróides.
- Criação de dois clusters iniciais com centróides aleatórios.
- Agrupamento dos alunos de acordo com a menor distância.
- Visualização dos clusters com matplotlib (`nota x faltas`).
- Cálculo dinâmico dos centróides de cada cluster.

---

## 🖥️ Como Executar

### 1. Instale as dependências:

```bash
pip install matplotlib scikit-learn
```

### 2. Execute o projeto:

```bash
python main.py
```

---

## 📌 Exemplo de Dados (`alunos1.csv`)

```csv
nome,anos,media,faltas
Joao,23,7.5,0.24
Maria,17,9.4,0.00
...
```

---

## 📊 Resultado Esperado

- Um gráfico com os alunos divididos em clusters de cores diferentes.
- Um **X grande** representa o centróide de cada grupo.

---

## 🚀 Tecnologias Utilizadas

- Python 3
- matplotlib
- scikit-learn
- Programação orientada a objetos

---

## 👨‍💻 Alunos

- Kauan Henrique Bertalha – RA: 22262074-2
- Matheus Toscano Rossini – RA: 22212262-2
- Willyan Santos Tomaz e Silva – RA: 22014128-2

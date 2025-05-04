import csv
from hipoteses.atuariais import carregar_hipoteses

# Carregar dados dos benefícios
def carregar_beneficios(path="dados/beneficios.csv"):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# Cálculo de provisões matemáticas
def calcular_provisao(beneficios):
    hipoteses = carregar_hipoteses()
    provisao_total = 0
    for beneficio in beneficios:
        tipo = beneficio["tipo"].lower()
        valor_beneficio = float(beneficio["beneficio"])
        idade = int(beneficio["idade"])

        # Projeção simples com base na taxa de mortalidade
        taxa_mortalidade = hipoteses["taxa_mortalidade"].get(str(idade), 0.01)
        provisao = valor_beneficio / taxa_mortalidade  # Simplificado

        provisao_total += provisao

    return provisao_total

# Cálculo da alíquota de contribuição necessária
def calcular_aliquota_contribuicao(provisao_total, salario_total):
    return provisao_total / salario_total

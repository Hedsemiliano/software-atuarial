import csv
from statistics import mean

def carregar_massa(path="dados/massa.csv"):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def calcular_estatisticas(massa):
    tipos = {"ativo": [], "aposentado": [], "pensionista": []}
    for pessoa in massa:
        tipo = pessoa["tipo"].lower()
        if tipo in tipos:
            tipos[tipo].append(int(pessoa["idade"]))

    estatisticas = {}
    for grupo, idades in tipos.items():
        estatisticas[grupo] = {
            "quantidade": len(idades),
            "idade_media": round(mean(idades), 1) if idades else 0
        }
    estatisticas["total"] = sum(v["quantidade"] for v in estatisticas.values())
    return estatisticas

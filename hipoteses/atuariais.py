import json

def carregar_hipoteses(path="dados/hipoteses.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def mostrar_hipoteses():
    hipoteses = carregar_hipoteses()
    print("\n--- HIPÓTESES ATUARIAIS ---")
    for chave, valor in hipoteses.items():
        if isinstance(valor, dict):
            print(f"{chave.capitalize()}:")
            for idade, taxa in valor.items():
                print(f"  Idade {idade}: {taxa*100:.2f}%")
        else:
            print(f"{chave.capitalize()}: {valor*100:.2f}%")

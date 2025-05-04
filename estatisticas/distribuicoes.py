import numpy as np
import scipy.stats as sts
import csv

import numpy as np
import scipy.stats as sts
import csv

# Lista de distribuições a testar
DISTRIBUICOES = [
    sts.norm, sts.lognorm, sts.expon, sts.gamma, sts.weibull_min
]

def carregar_idades(path="dados/massa.csv"):
    """
    Lê o CSV de massa e retorna um array NumPy com as idades.
    """
    with open(path, newline="", encoding="utf-8") as f:
        data = [int(row["idade"]) for row in csv.DictReader(f)]
    return np.array(data)

def ajustar_e_testar(data):
    """
    Para cada distribuição em DISTRIBUICOES:
      1. Ajusta parâmetros via MLE
      2. Executa teste de Kolmogorov–Smirnov
      3. Retorna estatística D e p-valor
    """
    resultados = []

    for dist in DISTRIBUICOES:
        nome = dist.name
        try:
            # Ajustar parâmetros da distribuição ao conjunto de dados
            params = dist.fit(data)
            # Realizar o teste de K-S
            D, p_valor = sts.kstest(data, nome, args=params)
            resultados.append((nome, D, p_valor))
        except Exception as e:
            resultados.append((nome, None, f"Erro: {e}"))

    # Ordena pelos melhores p-valores (quanto maior, melhor ajuste)
    resultados.sort(key=lambda x: x[2] if isinstance(x[2], float) else 0, reverse=True)
    return resultados

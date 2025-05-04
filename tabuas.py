import pandas as pd
import os

def carregar_tabua_mortalidade(nome_tabua=None):
    """
    Carrega a tábua de mortalidade padrão ou uma tábua personalizada em CSV.
    :param nome_tabua: Nome do arquivo CSV na pasta 'dados/tabuas/'
    :return: Dicionário {idade: qx}
    """
    if nome_tabua:
        caminho = os.path.join("dados", "tabuas", nome_tabua)
        if os.path.exists(caminho):
            df = pd.read_csv(caminho)
            return dict(zip(df["idade"], df["qx"]))
        else:
            print(f"Arquivo {caminho} não encontrado. Usando tábua padrão.")

    # Tábua padrão fixa
    tabua_padrao = {
        20: 0.0003,
        21: 0.00031,
        22: 0.00032,
        23: 0.00033,
        24: 0.00034,
        25: 0.00035,
        30: 0.00045,
        35: 0.0006,
        40: 0.001,
        45: 0.002,
        50: 0.004,
        55: 0.008,
        60: 0.015,
        65: 0.03,
        70: 0.06,
        75: 0.10,
        80: 0.20,
        85: 0.30,
        90: 0.45,
        95: 0.60,
        100: 0.8,
        105: 1.0
    }
    return tabua_padrao

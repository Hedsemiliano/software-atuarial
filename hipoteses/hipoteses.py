from flask import Blueprint, render_template, request
import pandas as pd
import os

# Criando o blueprint
hipoteses_bp = Blueprint('hipoteses', __name__)

# Funções de carregamento de dados
def carregar_tabua(caminho=None):
    if caminho is None:
        caminho = os.path.join("dados", "tabuas", "tabua_padrao.csv")
    return pd.read_csv(caminho)

def carregar_hipotese_aposentadoria(caminho=None):
    if caminho is None:
        caminho = os.path.join("dados", "hipoteses", "hipotese_aposentadoria.csv")
    return pd.read_csv(caminho)

def carregar_parametros_economicos():
    return {
        "taxa_juros_real": 0.05,
        "indice_reajuste": "INPC (IBGE)"
    }

@hipoteses_bp.route("/", methods=["GET", "POST"])
def mostrar_hipoteses():
    tabua = pd.DataFrame()
    aposentadoria = pd.DataFrame()
    valor_patrimonio = None
    analise_ativos = False

    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename.endswith(".csv"):
                tabua = pd.read_csv(file)
        if "patrimonio" in request.form:
            valor_patrimonio = request.form["patrimonio"]
            analise_ativos = "analise_ativos" in request.form

    if tabua.empty:
        tabua = pd.DataFrame({
            "idade": list(range(20, 71)),
            "qx_m": [0.001 + i * 0.0001 for i in range(51)],
            "qx_f": [0.0008 + i * 0.00009 for i in range(51)],
        })

    aposentadoria = pd.DataFrame({
        "idade": list(range(50, 71)),
        "taxa_entrada_aposentadoria": [0.02 + (i - 50) * 0.005 for i in range(50, 71)],
    })

    parametros = {
        "taxa_juros_real": 0.05,
        "indice_reajuste": "IPCA",
    }

    return render_template(
        "hipoteses.html",
        tabua=tabua.to_dict(orient="records"),
        aposentadoria=aposentadoria.to_dict(orient="records"),
        parametros=parametros,
        valor_patrimonio=valor_patrimonio,
        analise_ativos=analise_ativos
    )

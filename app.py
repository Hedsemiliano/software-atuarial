from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from validate_docbr import CNPJ
from hipoteses.hipoteses import carregar_parametros_economicos
from hipoteses.hipoteses import carregar_hipotese_aposentadoria
from werkzeug.utils import secure_filename
from tabuas import carregar_tabua_mortalidade
import os
import PyPDF2
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from introducao.dados_gerais import carregar_dados_ente
from estatisticas.massa import carregar_massa, calcular_estatisticas
from hipoteses.atuariais import carregar_hipoteses
from projecao.atuarial import carregar_beneficios, calcular_provisao, calcular_aliquota_contribuicao
from plano_custeio.custeio import calcular_plano_custeio
from relatorios.gerar_pdf import gerar_relatorio_pdf
from hipoteses import hipoteses_bp  # Importa o blueprint
from estatisticas import estatisticas_bp  # Importa o blueprint# Registra o blueprint para estatísticas





# Inicializando o aplicativo Flask
app = Flask(__name__)

# Registra o blueprint
app.register_blueprint(hipoteses_bp, url_prefix="/hipoteses")
# Registra o blueprint para estatísticas
app.register_blueprint(estatisticas_bp, url_prefix="/estatisticas")





# Criando o aplicativo Dash
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Caminho padrão da tábua de mortalidade
CAMINHO_TABUA_PADRAO = os.path.join("dados", "tabuas", "tabua_padrao.csv")



# Gerando um gráfico de barras inicial com dados fictícios
df = pd.DataFrame({
    "Distribuição": ["Observado", "Estimado", "Ajustado"],
    "Valor": [150, 180, 175]
})

fig = px.bar(df, x="Distribuição", y="Valor", title="Distribuição Observada vs Estimada")

# Definindo o layout do Dash (painel interativo)
dash_app.layout = html.Div([
    html.H1("Painel Interativo - Distribuição Atuarial"),
    
    # Slider para definir uma taxa de juros (exemplo)
    html.Label("Taxa Real Anual de Juros (%)"),
    dcc.Slider(
        id='juros-slider',
        min=1,
        max=10,
        step=0.01,
        value=5.53,  # valor inicial
        marks={i: f'{i}%' for i in range(1, 11)},
    ),

    # Dropdown para escolher a tábua de mortalidade
    html.Label("Escolha a Tábua de Mortalidade"),
    dcc.Dropdown(
        id='tabua-dropdown',
        options=[
            {'label': 'AT-2000', 'value': 'AT-2000'},
            {'label': 'RRB-1983', 'value': 'RRB-1983'}
        ],
        value='AT-2000'  # valor inicial
    ),
    
    # Gráfico
    dcc.Graph(id='distribuicao-graph', figure=fig),

    # Link para download do PDF
    html.A("Baixar Relatório PDF", href="/download", target="_blank")
])

# Função para atualizar o gráfico com base nas entradas
@dash_app.callback(
    Output('distribuicao-graph', 'figure'),
    [Input('juros-slider', 'value'),
     Input('tabua-dropdown', 'value')]
)
def update_graph(taxa_juros, tabua):
    # Aqui você pode ajustar os dados do gráfico com base nos inputs
    # Exemplo simples: o valor de "Valor" no gráfico pode ser ajustado pela taxa de juros
    df = pd.DataFrame({
        "Distribuição": ["Observado", "Estimado", "Ajustado"],
        "Valor": [150 * (1 + taxa_juros / 100), 180 * (1 + taxa_juros / 100), 175 * (1 + taxa_juros / 100)]
    })
    fig = px.bar(df, x="Distribuição", y="Valor", title=f"Distribuição com Tábua: {tabua} e Taxa de Juros: {taxa_juros}%")
    return fig

# Definindo a função index() com os cálculos principais

# Função para carregar a tábua (padrão ou personalizada)
def carregar_tabua(caminho=CAMINHO_TABUA_PADRAO):
    try:
        tabua = pd.read_csv(caminho)
        return tabua
    except Exception as e:
        print(f"Erro ao carregar a tábua: {e}")
        return None







# Definindo a função index() com os cálculos principais
@app.route("/")
def index():
    tabua = carregar_tabua_mortalidade()  # usa a padrão
    # ou, se quiser testar outra:
    # tabua = carregar_tabua_mortalidade("AT2000.csv")
    dados_ente = carregar_dados_ente()
    massa = carregar_massa()
    estatisticas = calcular_estatisticas(massa)
    hipoteses = carregar_hipoteses()
    beneficios = carregar_beneficios()
    provisao = calcular_provisao(beneficios)
    salario_base = sum(float(b["beneficio"]) for b in beneficios)
    aliquota = calcular_aliquota_contribuicao(provisao, salario_base)
    plano = calcular_plano_custeio(
                        0.08 * salario_base,
                        0.12 * salario_base,
                        provisao
                   )

    # Gerar o relatório PDF
    gerar_relatorio_pdf(dados_ente, estatisticas, hipoteses, provisao, aliquota, plano, distribuicoes_resultados=[])

    # URL do PDF para download
    pdf_url = url_for('static', filename='relatorio_rpps.pdf')

    return render_template("index.html",
                           dados_ente=dados_ente,
                           estatisticas=estatisticas,
                           hipoteses=hipoteses,
                           provisao=provisao,
                           aliquota=aliquota,
                           plano=plano,
                           pdf_url=pdf_url)







@app.route("/hipoteses/patrimonio", methods=["GET", "POST"])
def mostrar_patrimonio():
    valor_patrimonio = None
    analise_ativos = False
    if request.method == "POST":
        valor_patrimonio = request.form.get("patrimonio")
        analise_ativos = "analise_ativos" in request.form
    return render_template("hipoteses/patrimonio.html",
                           valor_patrimonio=valor_patrimonio,
                           analise_ativos=analise_ativos)





# Rota para mostrar o plano de custeio
@app.route("/custeio", methods=["GET", "POST"])
def mostrar_custeio():
    plano = None
    if request.method == "POST":
        try:
            receita = float(request.form["receita"])
            despesa = float(request.form["despesa"])
            folha_ativa = float(request.form["folha_ativa"])

            # Novos campos dos participantes ativos
            ativos_qtd = int(request.form["ativos_qtd"])
            idade_media = float(request.form["idade_media"])
            folha_ativos = float(request.form["folha_ativos"])

            diferenca = receita - despesa
            status = "Superavitário" if diferenca >= 0 else "Deficitário"
            aliquota = (abs(diferenca) / folha_ativa) * 100 if folha_ativa > 0 else 0

            plano = {
                "receita_total": receita,
                "status": status,
                "diferenca": diferenca,
                "aliquota_ativa_pct": aliquota,
                "ativos_qtd": ativos_qtd,
                "idade_media": idade_media,
                "folha_ativos": folha_ativos
            }
        except (ValueError, KeyError) as e:
            plano = {
                "erro": f"Ocorreu um erro nos dados informados: {e}"
            }

    return render_template("custeio.html", plano=plano)


# app.py

@app.route("/simulacao", methods=["GET", "POST"])
def simulacao_atuarial():
    resultados = None
    tabua = None  # Inicializando a variável da tábua como None
    valor_patrimonio = None  # Placeholder para o valor do patrimônio
    analise_ativos = False  # Placeholder para a análise de ativos
    
    if request.method == "POST":
        ano = int(request.form["ano"])
        folha = float(request.form["folha"])
        receita = float(request.form["receita"])
        despesa = float(request.form["despesa"])

        # Realizando os cálculos
        resultado = receita - despesa
        saldo = resultado + folha  # Exemplo de saldo com a folha

        # Definindo os resultados a serem enviados à página
        resultados = {
            "ano": ano,
            "resultado": resultado,
            "saldo": saldo
        }

        # Carregando a tábua de mortalidade (exemplo)
        # Se a tábua de mortalidade for um DataFrame do pandas, faça o seguinte:
        # tabua = carregar_tabua_mortalidade()  # Carregar ou inicializar sua tábua de mortalidade aqui

        # Se o valor do patrimônio for enviado via POST
        if "patrimonio" in request.form:
            valor_patrimonio = request.form["patrimonio"]
            analise_ativos = "analise_ativos" in request.form

    return render_template("simulacao.html", resultados=resultados, tabua=tabua, valor_patrimonio=valor_patrimonio, analise_ativos=analise_ativos)

@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():
    if request.method == "POST":
        resultado_realizado = float(request.form["resultado"])
        ajuste = float(request.form["ajuste"])
        dados = calcular_equilibrio_tecnico(resultado_realizado, ajuste)
        return render_template("relatorio.html", dados=dados)
    return render_template("relatorio.html", dados=None)



@app.route('/resultados', methods=['GET', 'POST'])
def mostrar_resultados():
    if request.method == 'POST':
        # Recuperando os valores do formulário
        duracao_passivo = float(request.form['duracao_passivo'])
        provisoes_matematicas = float(request.form['provisoes_matematicas'])

        # Calculando o limite do déficit com base na fórmula
        limite_pct = 0.01 * (duracao_passivo - 4)
        limite_deficit = limite_pct * provisoes_matematicas

        return render_template('resultados.html', 
                               duracao=duracao_passivo,
                               provisoes=provisoes_matematicas,
                               limite_pct=limite_pct * 100,
                               limite_deficit=limite_deficit)
    else:
        return render_template('resultados.html')




# Rota para fazer o download do relatório PDF
@app.route("/download")
def download_report():
    return send_from_directory("static", "relatorio_rpps.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

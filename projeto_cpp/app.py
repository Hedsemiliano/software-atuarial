from flask import Flask, render_template, send_from_directory, url_for
from introducao.dados_gerais import carregar_dados_ente
from estatisticas.massa import carregar_massa, calcular_estatisticas
from hipoteses.atuariais import carregar_hipoteses
from projecao.atuarial import carregar_beneficios, calcular_provisao, calcular_aliquota_contribuicao
from plano_custeio.custeio import calcular_plano_custeio

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    dados_ente   = carregar_dados_ente()
    massa        = carregar_massa()
    estatisticas = calcular_estatisticas(massa)
    hipoteses    = carregar_hipoteses()
    beneficios   = carregar_beneficios()
    provisao     = calcular_provisao(beneficios)
    salario_base = sum(float(b["beneficio"]) for b in beneficios)
    aliquota     = calcular_aliquota_contribuicao(provisao, salario_base)
    plano        = calcular_plano_custeio(
                        0.08 * salario_base,
                        0.12 * salario_base,
                        provisao
                   )
    pdf_url = url_for('static', filename='relatorio_rpps.pdf')
    return render_template("index.html",
                           dados_ente=dados_ente,
                           estatisticas=estatisticas,
                           hipoteses=hipoteses,
                           provisao=provisao,
                           aliquota=aliquota,
                           plano=plano,
                           pdf_url=pdf_url)

@app.route("/download")
def download_report():
    return send_from_directory("static", "relatorio_rpps.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

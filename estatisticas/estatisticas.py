from flask import Blueprint, render_template, request

# Criando o Blueprint para Estatísticas
estatisticas_bp = Blueprint('estatisticas', __name__)

# Rota para mostrar as Estatísticas
@estatisticas_bp.route("/", methods=["GET", "POST"])
def mostrar_estatisticas():
    estatisticas = None
    erro = None

    if request.method == "POST":
        try:
            # Coleta dos dados do formulário, usando get() para evitar KeyError
            estatisticas = {
                "data_base": request.form.get("data_base"),
                "ativos_qtd": int(request.form.get("ativos_qtd", 0)),
                "autopatrocinados_qtd": int(request.form.get("autopatrocinados_qtd", 0)),
                "bpd_qtd": int(request.form.get("bpd_qtd", 0)),
                "idade_media": float(request.form.get("idade_media", 0.0)),
                "tempo_servico": float(request.form.get("tempo_servico", 0.0)),
                "tempo_contribuicao": float(request.form.get("tempo_contribuicao", 0.0)),
                "tempo_servico_futuro": float(request.form.get("tempo_servico_futuro", 0.0)),
                "folha_ativos": float(request.form.get("folha_ativos", 0.0)),
                "aposentadoria_normal_qtd": int(request.form.get("aposentadoria_normal_qtd", 0)),
                "aposentadoria_normal_idade": float(request.form.get("aposentadoria_normal_idade", 0.0)),
                "aposentadoria_normal_valor": float(request.form.get("aposentadoria_normal_valor", 0.0)),
                "aposentadoria_antecipada_qtd": int(request.form.get("aposentadoria_antecipada_qtd", 0)),
                "aposentadoria_antecipada_idade": float(request.form.get("aposentadoria_antecipada_idade", 0.0)),
                "aposentadoria_antecipada_valor": float(request.form.get("aposentadoria_antecipada_valor", 0.0)),
                "beneficio_proporcional_qtd": int(request.form.get("beneficio_proporcional_qtd", 0)),
                "beneficio_proporcional_idade": float(request.form.get("beneficio_proporcional_idade", 0.0)),
                "beneficio_proporcional_valor": float(request.form.get("beneficio_proporcional_valor", 0.0)),
                "aposentadoria_invalidez_qtd": int(request.form.get("aposentadoria_invalidez_qtd", 0)),
                "aposentadoria_invalidez_idade": float(request.form.get("aposentadoria_invalidez_idade", 0.0)),
                "pensao_morte_qtd": int(request.form.get("pensao_morte_qtd", 0)),
                "pensao_morte_idade": float(request.form.get("pensao_morte_idade", 0.0)),
                "pensao_morte_valor": float(request.form.get("pensao_morte_valor", 0.0))
            }
        except (ValueError, TypeError) as e:
            erro = f"Ocorreu um erro ao processar os dados: {e}"

    return render_template("estatisticas.html", estatisticas=estatisticas, erro=erro)

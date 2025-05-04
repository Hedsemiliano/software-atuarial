# plano_custeio/custeio.py

def calcular_plano_custeio(contrib_ativos, contrib_patronal, provisao_total):
    """
    Monta o plano de custeio:
    - contrib_ativos: soma de contribuições dos ativos (R$)
    - contrib_patronal: soma de contribuições do ente (R$)
    - provisao_total: valor das provisões (R$)
    Retorna dicionário com necessidade líquida e alíquotas ajustadas.
    """
    receita_total = contrib_ativos + contrib_patronal
    diferenca = provisao_total - receita_total

    # Se diferenca > 0: déficit; se < 0: superávit
    aliquota_ativa = (contrib_ativos / receita_total) * 100 if receita_total else 0
    aliquota_patronal = (contrib_patronal / receita_total) * 100 if receita_total else 0

    return {
        "receita_total": receita_total,
        "diferenca": diferenca,
        "aliquota_ativa_pct": aliquota_ativa,
        "aliquota_patronal_pct": aliquota_patronal,
        "status": "Déficit" if diferenca > 0 else "Superávit"
    }

from flask import Flask, render_template, send_from_directory, url_for
from estatisticas.distribuicoes import carregar_idades, ajustar_e_testar
from relatorios.gerar_pdf import gerar_relatorio_pdf
from plano_custeio.custeio import calcular_plano_custeio
from introducao.dados_gerais import carregar_dados_ente
from introducao.validador import validar_dados_ente
from estatisticas.massa import carregar_massa, calcular_estatisticas
from hipoteses.atuariais import carregar_hipoteses
from projecao.atuarial import carregar_beneficios, calcular_provisao, calcular_aliquota_contribuicao

app = Flask(__name__, static_folder="static")

def mostrar_custeio():
    # Exemplos de alíquotas hipotéticas
    beneficios = carregar_beneficios()
    base_salario = sum(float(b["beneficio"]) for b in beneficios)
    contrib_ativos = 0.08 * base_salario      # 8% sobre a base de salários
    contrib_patronal = 0.12 * base_salario    # 12% sobre a base de salários
    provisao_total = calcular_provisao(beneficios)

    plano = calcular_plano_custeio(contrib_ativos, contrib_patronal, provisao_total)
    print("\n--- PLANO DE CUSTEIO ---")
    print(f"Receita Total (Ativos + Patronal): R${plano['receita_total']:.2f}")
    print(f"{plano['status']}: R${abs(plano['diferenca']):.2f}")
    print(f"Alíquota Ativa: {plano['aliquota_ativa_pct']:.2f}%")
    print(f"Alíquota Patronal: {plano['aliquota_patronal_pct']:.2f}%")





def mostrar_dados_ente():
    try:
        dados = carregar_dados_ente()
        validar_dados_ente(dados)  # Valida os dados
        print("\n--- INFORMAÇÕES DO ENTE ---")
        for chave, valor in dados.items():
            print(f"{chave.upper()}: {valor}")
    except Exception as e:
        print(f"Erro ao carregar ou validar os dados do ente: {e}")


def mostrar_estatisticas():
    massa = carregar_massa()
    stats = calcular_estatisticas(massa)
    print("\n--- ESTATÍSTICAS DA MASSA ---")
    for grupo in ["ativo", "aposentado", "pensionista"]:
        print(f"{grupo.capitalize()}: {stats[grupo]['quantidade']} pessoas, idade média: {stats[grupo]['idade_media']:.1f} anos")
    print(f"Total geral: {stats['total']} segurados")


def mostrar_hipoteses():
    hipoteses = carregar_hipoteses()
    print("\n--- HIPÓTESES ATUARIAIS ---")
    for chave, valor in hipoteses.items():
        if isinstance(valor, dict):
            print(f"{chave.capitalize()}:")
            for idade, taxa in valor.items():
                print(f"  Idade {idade}: {taxa * 100:.2f}%")
        else:
            print(f"{chave.capitalize()}: {valor * 100:.2f}%")


def mostrar_projecao():
    beneficios = carregar_beneficios()
    provisao_total = calcular_provisao(beneficios)
    salario_total = sum([float(b["beneficio"]) for b in beneficios])
    aliquota = calcular_aliquota_contribuicao(provisao_total, salario_total)

    print("\n--- PROJEÇÃO ATUARIAL ---")
    print(f"Provisão total necessária: R${provisao_total:.2f}")
    print(f"Alíquota de contribuição necessária: {aliquota:.2f}%")




def calcular_equilibrio_tecnico(resultado_realizado, ajuste_precificacao):
    superavit = 0.0
    deficit = abs(resultado_realizado) if resultado_realizado < 0 else 0.0
    equilibrio_ajustado = resultado_realizado + ajuste_precificacao

    return {
        "resultado_realizado": resultado_realizado,
        "superavit": superavit,
        "deficit": deficit,
        "ajuste": ajuste_precificacao,
        "equilibrio_ajustado": equilibrio_ajustado
    }





def gerar_relatorio():
    dados_ente   = carregar_dados_ente()
    massa        = carregar_massa()
    estatisticas = calcular_estatisticas(massa)
    hipoteses    = carregar_hipoteses()
    beneficios   = carregar_beneficios()

    # Calcular provisão e salário base
    provisao = calcular_provisao(beneficios)
    salario_base = sum(float(b["beneficio"]) for b in beneficios)

    # Calcular a alíquota de contribuição e o plano de custeio
    aliquota = calcular_aliquota_contribuicao(provisao, salario_base)
    plano = calcular_plano_custeio(
        0.08 * salario_base,  # 8% sobre o salário base
        0.12 * salario_base,  # 12% sobre o salário base
        provisao
    )

    # Análise estatística das idades com teste de distribuições
    print("\n--- TESTE DE DISTRIBUIÇÕES ---")
    idades = carregar_idades()
    resultados = ajustar_e_testar(idades)

    melhor = None
    distribuicoes_resultados = []
    for nome, D, p in resultados:
        if isinstance(p, float):
            distribuicoes_resultados.append(f"{nome}: D = {D:.4f}, p-valor = {p:.4f}")
            if melhor is None or p > melhor[2]:
                melhor = (nome, D, p)
        else:
            distribuicoes_resultados.append(f"{nome}: {p}")

    if melhor:
        distribuicoes_resultados.append(f"\nMelhor aderência: {melhor[0]} (p-valor = {melhor[2]:.4f})")
    else:
        distribuicoes_resultados.append("\nNenhuma distribuição pôde ser ajustada corretamente.")


if __name__ == "__main__":
    # Carregar os dados necessários
    dados_ente = carregar_dados_ente()  # <<-- Adicionado
    massa = carregar_massa()
    estatisticas = calcular_estatisticas(massa)
    hipoteses = carregar_hipoteses()
    beneficios = carregar_beneficios()

    # Calcular provisão e salário base
    provisao = calcular_provisao(beneficios)
    salario_base = sum(float(b["beneficio"]) for b in beneficios)

    # Calcular a alíquota e plano de custeio
    aliquota = calcular_aliquota_contribuicao(provisao, salario_base)
    plano = calcular_plano_custeio(0.08 * salario_base, 0.12 * salario_base, provisao)

    # Análise estatística das idades
    print("\n--- TESTE DE DISTRIBUIÇÕES ---")
    idades = carregar_idades()
    resultados = ajustar_e_testar(idades)

    melhor = None
    distribuicoes_resultados = []
    for nome, D, p in resultados:
        if isinstance(p, float):
            distribuicoes_resultados.append(f"{nome}: D = {D:.4f}, p-valor = {p:.4f}")
            if melhor is None or p > melhor[2]:
                melhor = (nome, D, p)
        else:
            distribuicoes_resultados.append(f"{nome}: {p}")

    if melhor:
        distribuicoes_resultados.append(
            f"\nMelhor aderência: {melhor[0]} (p-valor = {melhor[2]:.4f})"
        )
    else:
        distribuicoes_resultados.append(
            "\nNenhuma distribuição pôde ser ajustada corretamente."
        )

    # Geração do relatório
    try:
        gerar_relatorio_pdf(
            dados_ente=dados_ente,
            estatisticas=estatisticas,
            hipoteses=hipoteses,
            provisao=provisao,
            aliquota=aliquota,
            plano=plano,
            distribuicoes_resultados=distribuicoes_resultados
        )
    except Exception as e:
        print(f"Erro ao gerar o relatório PDF: {e}")

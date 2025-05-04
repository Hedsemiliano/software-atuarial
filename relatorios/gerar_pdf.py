import os
from datetime import datetime
import platform
from fpdf import FPDF
import PyPDF2

def gerar_relatorio_pdf(dados_ente, estatisticas, hipoteses, provisao, aliquota, plano, distribuicoes_resultados):
    # Garantir que o diretório 'static' exista
    os.makedirs("static", exist_ok=True)

    # Criar o objeto PDF
    pdf = FPDF()
    pdf.add_page()

    # Definir a fonte
    pdf.set_font("Arial", size=10)

    # Função para substituir caracteres problemáticos
    def substituir_caracteres(texto):
        return texto.replace("–", "-").replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')

    # Nome de arquivo dinâmico
    nome_arquivo = f"static/relatorio_rpps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # Informações do Ente
    pdf.set_font("Arial", 'B', size=10)  # Título em negrito
    pdf.cell(30, 10, txt="--- INFORMAÇÕES DO ENTE ---", ln=True)
    pdf.set_font("Arial", size=10)  # Voltar ao estilo normal
    for chave, valor in dados_ente.items():
        texto = f"{chave.upper()}: {valor}"
        pdf.multi_cell(100, 10, txt=substituir_caracteres(texto))

    # Adicionar espaço entre as seções
    pdf.ln(5)    
    # Estatísticas
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(100, 10, txt="--- ESTATÍSTICAS DA MASSA ---", ln=True)
    pdf.set_font("Arial", size=10)
    for grupo in ["ativo", "aposentado", "pensionista"]:
        texto = f"{grupo.capitalize()}: {estatisticas[grupo]['quantidade']} pessoas, idade média: {estatisticas[grupo]['idade_media']:.2f}"
        pdf.multi_cell(100, 10, txt=substituir_caracteres(texto))
    pdf.multi_cell(100, 10, txt=f"Total geral: {estatisticas['total']} segurados")

    pdf.ln(5)

    # Hipóteses Atuariais
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(30, 10, txt="--- HIPÓTESES ATUARIAIS ---", ln=True)
    pdf.set_font("Arial", size=10)
    for chave, valor in hipoteses.items():
        if isinstance(valor, dict):
            pdf.multi_cell(100, 10, txt=f"{chave.capitalize()}:")
            for idade, taxa in valor.items():
                texto = f"  Idade {idade}: {taxa * 100:.2f}%"
                pdf.multi_cell(100, 10, txt=substituir_caracteres(texto))
        else:
            texto = f"{chave.capitalize()}: {valor * 100:.2f}%"
            pdf.multi_cell(100, 10, txt=substituir_caracteres(texto))

    pdf.ln(5)

    # Projeção Atuarial
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(30, 10, txt="--- PROJEÇÃO ATUARIAL ---", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(100, 10, txt=f"Provisão total necessária: R${provisao:.2f}")
    pdf.multi_cell(100, 10, txt=f"Alíquota de contribuição necessária: {aliquota:.2f}%")

    pdf.ln(5)

    # Plano de Custeio
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(30, 10, txt="--- PLANO DE CUSTEIO ---", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(100, 10, txt=f"Receita Total (Ativos + Patronal): R${plano['receita_total']:.2f}")
    pdf.multi_cell(100, 10, txt=f"{plano['status']}: R${abs(plano['diferenca']):.2f}")
    pdf.multi_cell(100, 10, txt=f"Alíquota Ativa: {plano['aliquota_ativa_pct']:.2f}%")
    pdf.multi_cell(100, 10, txt=f"Alíquota Patronal: {plano['aliquota_patronal_pct']:.2f}%")

    pdf.ln(5)

    # Teste de Distribuições
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(30, 10, txt="--- TESTE DE DISTRIBUIÇÕES ---", ln=True)
    pdf.set_font("Arial", size=10)
    for linha in distribuicoes_resultados:
        pdf.multi_cell(100, 10, txt=substituir_caracteres(linha))

    # Salvar o arquivo PDF
    pdf.output(nome_arquivo)

    # Verificar se o arquivo foi criado
    if os.path.exists(nome_arquivo):
        print(f"PDF gerado com sucesso: {nome_arquivo}")
        if platform.system() == "Linux":
            os.system(f"xdg-open {nome_arquivo}")
        elif platform.system() == "Darwin":
            os.system(f"open {nome_arquivo}")
        elif platform.system() == "Windows":
            os.system(f"start {nome_arquivo}")

     # Verificar conteúdo do PDF
    with open(nome_arquivo, "rb") as arquivo_pdf:
        leitor = PyPDF2.PdfReader(arquivo_pdf)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""  # Evita erro se extract_text() retornar None

        if "INFORMAÇÕES DO ENTE" in texto:
            print("PDF gerado corretamente!")
        else:
            print("Erro: conteúdo esperado não encontrado no PDF.")

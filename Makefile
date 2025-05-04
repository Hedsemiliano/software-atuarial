# Diretórios importantes
APP_DIR=.
TEMPLATES_DIR=templates
DADOS_DIR=dados
TABUAS_DIR=$(DADOS_DIR)/tabuas
RELATORIOS_DIR=relatorios
STATIC_DIR=static
VENV_DIR=venv

# Ativa o ambiente virtual e roda o app Flask
run:
	. $(VENV_DIR)/bin/activate && flask run

# Abre o app no navegador
open-app:
	xdg-open http://127.0.0.1:5000

# Editar arquivos principais
edit-app:
	nano $(APP_DIR)/app.py

edit-hipoteses:
	nano $(TEMPLATES_DIR)/hipoteses.html

edit-relatorio:
	nano $(RELATORIOS_DIR)/gerar_pdf.py

edit-index:
	nano $(TEMPLATES_DIR)/index.html

# Abrir o relatório gerado
open-pdf:
	xdg-open $(STATIC_DIR)/relatorio_rpps.pdf

# Lista as tábuas disponíveis
list-tabuas:
	ls -1 $(TABUAS_DIR)

# Ativar shell no ambiente virtual
shell:
	. $(VENV_DIR)/bin/activate && bash

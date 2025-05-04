def validar_dados_ente(dados):
    """
    Verifica se todos os campos obrigatórios do ente estão presentes.
    Lança ValueError se algum campo estiver ausente.
    """
    campos_obrigatorios = ["ente", "cnpj", "regime", "periodo_avaliacao", "atuario"]
    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] in (None, ""):
            raise ValueError(f"Campo obrigatório ausente ou vazio: {campo}")
    return True


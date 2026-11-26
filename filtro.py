def montar_filtro(chave, campos, campo, valor):
    if campo not in chave and (campo not in campos or campo == "senha"):
        raise ValueError("Campo inválido.")
    if valor is None:
        condicao = f"{campo} IS NULL"
        parametros = ()
    elif campos.get(campo, "").startswith("texto"):
        condicao = f"INSTR({campo}, %s) > 0"
        parametros = (valor,)
    else:
        condicao = f"{campo} = %s"
        parametros = (valor,)
    return condicao, parametros

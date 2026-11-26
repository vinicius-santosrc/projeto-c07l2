from conexao import cursor_mysql

ENTIDADES = {
    "usuario": (("id_usuario",), {
        "nome": "texto", "email": "texto", "senha": "senha", "data_cadastro": "data",
    }),
    "perfil": (("id_perfil",), {
        "nickname": "texto", "foto": "texto?", "biografia": "texto?",
        "id_usuario": "id",
    }),
    "desenvolvedora": (("id_desenvolvedora",), {
        "nome": "texto", "pais": "texto?", "site": "texto?",
    }),
    "categoria": (("id_categoria",), {
        "nome": "texto", "descricao": "texto?",
    }),
    "jogo": (("id_jogo",), {
        "titulo": "texto", "descricao": "texto?", "preco": "valor",
        "data_lancamento": "data?", "classificacao_indicativa": "texto?",
        "id_desenvolvedora": "id", "id_categoria": "id",
    }),
    "compra": (("id_usuario", "id_jogo"), {
        "data_compra": "data_hora", "valor_pago": "valor",
        "forma_pagamento": "texto?",
    }),
}

JOINS = {
    "Usuários e perfis (1:1)": """
        SELECT u.id_usuario, u.nome, p.nickname, p.biografia
        FROM usuario AS u
        INNER JOIN perfil AS p ON p.id_usuario = u.id_usuario
        ORDER BY u.id_usuario
    """,
    "Desenvolvedoras e jogos (1:N)": """
        SELECT d.nome AS desenvolvedora, j.id_jogo, j.titulo, j.preco
        FROM desenvolvedora AS d
        INNER JOIN jogo AS j ON j.id_desenvolvedora = d.id_desenvolvedora
        ORDER BY d.nome, j.titulo
    """,
    "Usuários e jogos comprados (N:M)": """
        SELECT u.nome AS usuario, j.titulo, c.data_compra, c.valor_pago, c.forma_pagamento
        FROM usuario AS u
        INNER JOIN compra AS c ON c.id_usuario = u.id_usuario
        INNER JOIN jogo AS j ON j.id_jogo = c.id_jogo
        ORDER BY u.nome, j.titulo
    """,
}


def campos_busca(tabela):
    chaves, campos = ENTIDADES[tabela]
    return dict.fromkeys(chaves, "id") | {
        campo: tipo for campo, tipo in campos.items() if tipo != "senha"
    }


def consultar(config, sql, parametros=()):
    with cursor_mysql(config) as cursor:
        cursor.execute(sql, parametros)
        return cursor.fetchall()


def gravar(config, sql, parametros):
    with cursor_mysql(config, escrita=True) as cursor:
        cursor.execute(sql, parametros)
        return cursor.rowcount, cursor.lastrowid


def clausula_where(tabela, filtros):
    campos = campos_busca(tabela)
    condicoes = []
    parametros = []
    for campo, valor in filtros.items():
        tipo = campos[campo]
        if valor is None:
            condicoes.append(f"{campo} IS NULL")
        else:
            condicao = f"INSTR({campo}, %s) > 0" if tipo.startswith("texto") else f"{campo} = %s"
            condicoes.append(condicao)
            parametros.append(valor)
    where = " WHERE " + " AND ".join(condicoes) if condicoes else ""
    return where, tuple(parametros)


def listar(config, tabela, filtros):
    colunas = ", ".join(campos_busca(tabela))
    ordem = ", ".join(ENTIDADES[tabela][0])
    where, parametros = clausula_where(tabela, filtros)
    return consultar(config, f"SELECT {colunas} FROM {tabela}{where} ORDER BY {ordem}", parametros)


def cadastrar(config, tabela, dados):
    campos = ENTIDADES[tabela][1]
    colunas = ", ".join(dados)
    valores = ", ".join("SHA2(%s, 256)" if campos[campo] == "senha" else "%s" for campo in dados)
    _, novo_id = gravar(config, f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})", tuple(dados.values()))
    return novo_id


def registrar_compra(config, usuario, jogo, pagamento):
    with cursor_mysql(config, escrita=True) as cursor:
        cursor.execute("CALL sp_registrar_compra(%s, %s, %s)", (usuario, jogo, pagamento))
        mensagem = cursor.fetchall()[0]["Resultado"]
        while cursor.nextset():
            if cursor.with_rows:
                cursor.fetchall()
        return mensagem


def atualizar(config, tabela, campo, valor, filtros):
    tipo = ENTIDADES[tabela][1][campo]
    atribuicao = "SHA2(%s, 256)" if tipo == "senha" else "%s"
    where, parametros = clausula_where(tabela, filtros)
    quantidade, _ = gravar(config, f"UPDATE {tabela} SET {campo} = {atribuicao}{where}", (valor, *parametros))
    return quantidade


def remover(config, tabela, filtros):
    chaves = ENTIDADES[tabela][0]
    if set(filtros) != set(chaves) or any(filtros[chave] is None for chave in chaves):
        raise ValueError("Informe todos os campos da chave primária para remover.")
    where, parametros = clausula_where(tabela, filtros)
    quantidade, _ = gravar(config, f"DELETE FROM {tabela}{where}", parametros)
    return quantidade

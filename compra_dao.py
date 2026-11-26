from mysql.connector import Error

from filtro import montar_filtro
from connection_dao import close_connection, get_connection

TABELA = "compra"
CHAVE = ('id_usuario', 'id_jogo')
CAMPOS = {'data_compra': 'data_hora', 'valor_pago': 'valor', 'forma_pagamento': 'texto?'}


def listar():
    conn = get_connection()
    if conn is None:
        return []
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, id_jogo, data_compra, valor_pago, forma_pagamento FROM compra ORDER BY id_usuario, id_jogo")
        return cursor.fetchall()
    except Error as e:
        print(f"Erro na operação: {e}")
        return []
    finally:
        close_connection(conn, cursor)


def buscar(campo, valor):
    conn = get_connection()
    if conn is None:
        return []
    cursor = None
    try:
        cursor = conn.cursor()
        condicao, parametros = montar_filtro(CHAVE, CAMPOS, campo, valor)
        cursor.execute(f"SELECT id_usuario, id_jogo, data_compra, valor_pago, forma_pagamento FROM compra WHERE {condicao} ORDER BY id_usuario, id_jogo", parametros)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro na operação: {e}")
        return []
    finally:
        close_connection(conn, cursor)


def inserir(id_usuario, id_jogo, forma_pagamento):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("CALL sp_registrar_compra(%s, %s, %s)", (id_usuario, id_jogo, forma_pagamento))
        mensagem = cursor.fetchone()[0]
        while cursor.nextset():
            if cursor.with_rows:
                cursor.fetchall()
        conn.commit()
        return mensagem
    except Error as e:
        print(f"Erro na operação: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)


def atualizar(campo, novo_valor, filtro=None, valor=None):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        if campo not in CAMPOS:
            raise ValueError("Campo inválido.")
        expressao = "SHA2(%s, 256)" if campo == "senha" else "%s"
        sql = f"UPDATE compra SET {campo} = {expressao}"
        parametros = (novo_valor,)
        if filtro is not None:
            condicao, valores = montar_filtro(CHAVE, CAMPOS, filtro, valor)
            sql += " WHERE " + condicao
            parametros += valores
        cursor.execute(sql, parametros)
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Erro na operação: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)


def remover(id_usuario, id_jogo):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM compra WHERE id_usuario = %s AND id_jogo = %s"
        cursor.execute(sql, (id_usuario, id_jogo,))
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Erro na operação: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

from mysql.connector import Error

from filtro import montar_filtro
from connection_dao import close_connection, get_connection

TABELA = "desenvolvedora"
CHAVE = ('id_desenvolvedora',)
CAMPOS = {'nome': 'texto', 'pais': 'texto?', 'site': 'texto?'}


def listar():
    conn = get_connection()
    if conn is None:
        return []
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_desenvolvedora, nome, pais, site FROM desenvolvedora ORDER BY id_desenvolvedora")
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
        cursor.execute(f"SELECT id_desenvolvedora, nome, pais, site FROM desenvolvedora WHERE {condicao} ORDER BY id_desenvolvedora", parametros)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro na operação: {e}")
        return []
    finally:
        close_connection(conn, cursor)


def inserir(nome, pais, site):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO desenvolvedora (nome, pais, site) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, pais, site))
        conn.commit()
        return cursor.lastrowid
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
        sql = f"UPDATE desenvolvedora SET {campo} = {expressao}"
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


def remover(id_desenvolvedora):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM desenvolvedora WHERE id_desenvolvedora = %s"
        cursor.execute(sql, (id_desenvolvedora,))
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Erro na operação: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

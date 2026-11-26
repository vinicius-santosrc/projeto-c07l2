from mysql.connector import Error

from filtro import montar_filtro
from connection_dao import close_connection, get_connection

TABELA = "perfil"
CHAVE = ('id_perfil',)
CAMPOS = {'nickname': 'texto', 'foto': 'texto?', 'biografia': 'texto?', 'id_usuario': 'id'}


def listar():
    conn = get_connection()
    if conn is None:
        return []
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_perfil, nickname, foto, biografia, id_usuario FROM perfil ORDER BY id_perfil")
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
        cursor.execute(f"SELECT id_perfil, nickname, foto, biografia, id_usuario FROM perfil WHERE {condicao} ORDER BY id_perfil", parametros)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro na operação: {e}")
        return []
    finally:
        close_connection(conn, cursor)


def inserir(nickname, foto, biografia, id_usuario):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO perfil (nickname, foto, biografia, id_usuario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nickname, foto, biografia, id_usuario))
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
        sql = f"UPDATE perfil SET {campo} = {expressao}"
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


def remover(id_perfil):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM perfil WHERE id_perfil = %s"
        cursor.execute(sql, (id_perfil,))
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Erro na operação: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

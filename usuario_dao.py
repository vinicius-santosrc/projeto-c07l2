from mysql.connector import Error

from filtro import montar_filtro
from connection_dao import close_connection, get_connection

TABELA = "usuario"
CHAVE = ('id_usuario',)
CAMPOS = {'nome': 'texto', 'email': 'texto', 'senha': 'senha', 'data_cadastro': 'data'}


def listar():
    conn = get_connection()
    if conn is None:
        return []
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nome, email, data_cadastro FROM usuario ORDER BY id_usuario")
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
        cursor.execute(f"SELECT id_usuario, nome, email, data_cadastro FROM usuario WHERE {condicao} ORDER BY id_usuario", parametros)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro na operação: {e}")
        return []
    finally:
        close_connection(conn, cursor)


def inserir(nome, email, senha, data_cadastro):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO usuario (nome, email, senha, data_cadastro) VALUES (%s, %s, SHA2(%s, 256), %s)"
        cursor.execute(sql, (nome, email, senha, data_cadastro))
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
        sql = f"UPDATE usuario SET {campo} = {expressao}"
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


def remover(id_usuario):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM usuario WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Erro na operação: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

from mysql.connector import Error

from filtro import montar_filtro
from connection_dao import close_connection, get_connection

TABELA = "jogo"
CHAVE = ('id_jogo',)
CAMPOS = {'titulo': 'texto', 'descricao': 'texto?', 'preco': 'valor', 'data_lancamento': 'data?', 'classificacao_indicativa': 'texto?', 'id_desenvolvedora': 'id', 'id_categoria': 'id'}


def listar():
    conn = get_connection()
    if conn is None:
        return []
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_jogo, titulo, descricao, preco, data_lancamento, classificacao_indicativa, id_desenvolvedora, id_categoria FROM jogo ORDER BY id_jogo")
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
        cursor.execute(f"SELECT id_jogo, titulo, descricao, preco, data_lancamento, classificacao_indicativa, id_desenvolvedora, id_categoria FROM jogo WHERE {condicao} ORDER BY id_jogo", parametros)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro na operação: {e}")
        return []
    finally:
        close_connection(conn, cursor)


def inserir(titulo, descricao, preco, data_lancamento, classificacao_indicativa, id_desenvolvedora, id_categoria):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO jogo (titulo, descricao, preco, data_lancamento, classificacao_indicativa, id_desenvolvedora, id_categoria) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (titulo, descricao, preco, data_lancamento, classificacao_indicativa, id_desenvolvedora, id_categoria))
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
        sql = f"UPDATE jogo SET {campo} = {expressao}"
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


def remover(id_jogo):
    conn = get_connection()
    if conn is None:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM jogo WHERE id_jogo = %s"
        cursor.execute(sql, (id_jogo,))
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Erro na operação: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

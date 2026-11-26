
from mysql.connector import Error
from connection_dao import close_connection, get_connection


def consulta_1():
    conn = get_connection()

    if conn is None:
        return []

    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            SELECT u.id_usuario, u.nome, p.nickname, p.biografia
            FROM usuario AS u
            INNER JOIN perfil AS p
            ON p.id_usuario = u.id_usuario
            ORDER BY u.id_usuario
        """

        cursor.execute(sql)
        resultado = cursor.fetchall()

        return resultado

    except Error as e:
        print("Erro na consulta:", e)
        return []

    finally:
        close_connection(conn, cursor)


def consulta_2():
    conn = get_connection()

    if conn is None:
        return []

    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            SELECT d.nome, j.id_jogo, j.titulo, j.preco
            FROM desenvolvedora AS d
            INNER JOIN jogo AS j
            ON j.id_desenvolvedora = d.id_desenvolvedora
            ORDER BY d.nome, j.titulo
        """

        cursor.execute(sql)
        resultado = cursor.fetchall()

        return resultado

    except Error as e:
        print("Erro na consulta:", e)
        return []

    finally:
        close_connection(conn, cursor)


def consulta_3():
    conn = get_connection()

    if conn is None:
        return []

    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            SELECT u.nome, j.titulo, c.data_compra,
                   c.valor_pago, c.forma_pagamento
            FROM usuario AS u
            INNER JOIN compra AS c
            ON c.id_usuario = u.id_usuario
            INNER JOIN jogo AS j
            ON j.id_jogo = c.id_jogo
            ORDER BY u.nome, j.titulo
        """

        cursor.execute(sql)
        resultado = cursor.fetchall()

        return resultado

    except Error as e:
        print("Erro na consulta:", e)
        return []

    finally:
        close_connection(conn, cursor)

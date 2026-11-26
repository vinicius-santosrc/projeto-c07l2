import os
from contextlib import contextmanager
from getpass import getpass

import mysql.connector


def configurar():
    senha = os.getenv("MYSQL_PASSWORD")
    if senha is None:
        senha = getpass("Senha do MySQL (Enter se estiver vazia): ")
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": senha,
        "database": "STEAM_DB",
        "charset": "utf8mb4",
        "connection_timeout": 5,
    }


@contextmanager
def cursor_mysql(config, *, escrita=False):
    conexao = mysql.connector.connect(**config)
    try:
        with conexao.cursor(dictionary=True) as cursor:
            yield cursor
        if escrita:
            conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()

# connection_dao.py
# Módulo responsável por abrir e fechar a conexão com o MySQL.
# Todos os DAOs do projeto usam este módulo, então a configuração fica em um lugar só.

import os

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "STEAM_DB"),
}


def get_connection():
    """Abre uma conexão com o MySQL e a devolve (ou None se falhar)."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    return None


def close_connection(connection, cursor=None):
    """Fecha o cursor e depois a conexão."""
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"Erro ao fechar a conexão: {e}")


# Teste rápido: python connection_dao.py
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Conexão estabelecida com sucesso!")
        close_connection(conn)

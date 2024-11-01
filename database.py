import sqlite3


def conectar():
    conn = sqlite3.connect("sistema_backup_sws.db")
    return conn


def desconectar(conn):
    conn.close()


# Código para criação da tabela
conn = conectar()
cursor = conn.cursor()
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
""")
conn.commit()
desconectar(conn)

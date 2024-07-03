import psycopg2
from psycopg2 import sql


# Configurações do banco de dados
db_config = {
    'dbname': '',
    'user': '',
    'password': '',
    'host': '',
    'port': ''
}

# Função para conectar ao banco de dados
def connect_db():
    conn = psycopg2.connect(**db_config)
    return conn

# Função para inserir dados no banco de dados
def insert_data(data, umidade_solo, precisa_irrigar):
    conn = connect_db()
    cur = conn.cursor()
    query = sql.SQL("INSERT INTO inrrigar (data, umidade_solo, precisa_irrigar) VALUES (%s, %s, %s)")
    cur.execute(query, (data, umidade_solo, precisa_irrigar))
    conn.commit()
    cur.close()
    conn.close()

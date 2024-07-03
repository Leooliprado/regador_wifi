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

# Função para calcular a média de umidade do solo por dia e armazená-la
def calcular_media_diaria():
    conn = connect_db()
    cur = conn.cursor()
    query = """
    SELECT 
        SUBSTRING(data FROM 1 FOR 10) AS data,
        AVG(umidade_solo) AS media_umidade_solo
    FROM 
        inrrigar
    GROUP BY 
        SUBSTRING(data FROM 1 FOR 10)
    ORDER BY 
        data;
    """
    cur.execute(query)
    resultados = cur.fetchall()
    for linha in resultados:
        data = linha[0]
        media_umidade = linha[1]
        inserir_media_diaria(data, media_umidade)
    cur.close()
    conn.close()

# Função para inserir a média diária no banco de dados
def inserir_media_diaria(data, media_umidade_solo):
    conn = connect_db()
    cur = conn.cursor()
    query = sql.SQL("INSERT INTO medias_diarias (data, media_umidade_solo) VALUES (%s, %s) ON CONFLICT (data) DO UPDATE SET media_umidade_solo = EXCLUDED.media_umidade_solo")
    cur.execute(query, (data, media_umidade_solo))
    conn.commit()
    cur.close()
    conn.close()

# Função para obter a última média diária calculada
def obter_ultima_media_diaria():
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT media_umidade_solo FROM medias_diarias ORDER BY data DESC LIMIT 1"
    cur.execute(query)
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    return resultado[0] if resultado else None

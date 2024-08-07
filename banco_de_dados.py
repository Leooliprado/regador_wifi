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
    inrrigar_limpar()

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





def obter_medias_diarias_semana():
    conn = connect_db()
    cur = conn.cursor()
    query = """
        SELECT data, media_umidade_solo 
        FROM medias_diarias 
        WHERE data >= CURRENT_DATE - INTERVAL '7 days'
        ORDER BY data;
    """
    cur.execute(query)
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return [{'data': linha[0], 'media_umidade_solo': linha[1]} for linha in resultados] if resultados else None




# Função para contar quantas vezes precisa_irrigar foi TRUE
def contar_precisa_irrigar():
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT COUNT(*) FROM inrrigar WHERE precisa_irrigar = TRUE"
    cur.execute(query)
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    return resultado[0] if resultado else 0

def pegar_tudo_tebala_irrigar():
    conn = connect_db()  # Função para conectar ao banco de dados
    cur = conn.cursor()
    query = "SELECT data, umidade_solo FROM inrrigar"
    cur.execute(query)
    resultado = cur.fetchall()  # Usar fetchall para pegar todas as linhas
    cur.close()
    conn.close()
    return resultado if resultado else None







def inrrigar_limpar():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM inrrigar")
    conn.commit()
    cur.close()
    conn.close()




def limpar_tabela_media_diarias():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM medias_diarias")
    conn.commit()
    cur.close()
    conn.close()


from datetime import datetime
from flask import Flask, request
from psycopg2 import sql
from datetime import datetime
import schedule

from threading import Thread

from banco_de_dados import connect_db

# Função para obter a data e hora atuais
def dataehora():
    data = datetime.now()
    return data.strftime('%Y-%m-%d %H:%M:%S')





# Função para inserir dados no banco de dados
def insert_data(data, umidade_solo, precisa_irrigar):
    conn = connect_db()
    cur = conn.cursor()
    query = sql.SQL("INSERT INTO inrrigar (data, umidade_solo, precisa_irrigar) VALUES (%s, %s, %s)")
    cur.execute(query, (data, umidade_solo, precisa_irrigar))
    conn.commit()
    cur.close()
    conn.close()

# Função para calcular a média de umidade do solo por dia
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
    cur.close()
    conn.close()
    for linha in resultados:
        print(f"\033[92m Data: {linha[0]}, Média de Umidade do Solo: {linha[1]} \n\033[0m")

# Agendar a tarefa para executar às 24 horas todos os dias
schedule.every().day.at("20:08").do(calcular_media_diaria)





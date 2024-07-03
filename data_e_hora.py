from datetime import datetime
from flask import Flask, request
from psycopg2 import sql
from datetime import datetime
import schedule

from threading import Thread

from banco_de_dados import calcular_media_diaria, connect_db

# Função para obter a data e hora atuais
def dataehora():
    data = datetime.now()
    return data.strftime('%Y-%m-%d %H:%M:%S')



# Agendar a tarefa para calcular a média diária às 24 horas todos os dias
schedule.every().day.at("00:00").do(calcular_media_diaria)





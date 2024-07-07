from datetime import datetime
from flask import Flask, request
from psycopg2 import sql
from datetime import datetime


from threading import Thread


# Função para obter a data e hora atuais
def dataehora():
    data = datetime.now()
    return data.strftime('%Y-%m-%d %H:%M:%S')








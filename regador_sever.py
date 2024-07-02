from datetime import datetime
from flask import Flask, request
import socket
from psycopg2 import sql
import schedule
import time
from threading import Thread

from banco_de_dados import insert_data  # Corrigido o import para a função insert_data
from data_e_hora import dataehora

app = Flask(__name__)

# Variável global para armazenar a umidade
umidade = None


# Rota para receber dados de umidade do Arduino
@app.route('/umidade', methods=['POST'])
def coloca_umidade():
    global umidade
    dados = request.form.get("dados")
    if dados is not None:
        umidade = float(dados)
        precisa_irrigar = umidade > 3001  # Ajustado o valor de comparação da umidade

        data = dataehora()  # Obtem a data e hora atual
        
        # Inserir os dados no banco de dados
        insert_data(data, umidade, precisa_irrigar)

        print("\033[34m************************>> RECEBI <<************************\n\033[0m")
        print(f'\033[92m Umidade recebida: {dados}\n\033[0m') 
        print("\033[34m************************************************************\n\033[0m")

        return f'Umidade salva com sucesso: {umidade}'
    else:
        print('\033[91mDados não fornecidos\033[0m')  
        return 'Dados não fornecidos', 400

# Rota para solicitar dados de umidade
@app.route('/puxar', methods=['GET'])
def puxa_umidade():
    global umidade
    if umidade is not None:
        print("\033[38;5;214m**********************>> SOLICITADA <<**********************\n\033[0m")
        print(f'\033[92m Umidade solicitada: {umidade}\n \033[0m')
        print("\033[38;5;214m************************************************************\n\033[0m")

        return f'{umidade}'
    else:
        print('\033[91m Umidade não disponível\033[0m')  
        return 'Umidade não disponível', 404


# Função para executar as tarefas agendadas
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f"Operando no IP: {ip}")

    # Iniciar a thread para enviar umidade ao banco de dados a cada 30 minutos
    umidade_thread = Thread(target=run_schedule)  # Corrigido o target da thread para run_schedule
    umidade_thread.daemon = True
    umidade_thread.start()

    app.run(host=ip, port=4000, debug=False)

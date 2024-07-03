from datetime import datetime
from flask import Flask, request
import socket
import schedule
import time
from threading import Thread

from banco_de_dados import  insert_data, obter_ultima_media_diaria  # Import para a função insert_data
from data_e_hora import dataehora

app = Flask(__name__)

# Variável global para armazenar a umidade
umidade = None
scheduled_job = None  # Variável para armazenar o job agendado

# Rota para receber dados de umidade do Arduino
@app.route('/umidade', methods=['POST'])
def coloca_umidade():
    global umidade, scheduled_job
    dados = request.form.get("dados")
    if dados is not None:
        try:
            umidade = float(dados)
        except ValueError:
            return 'Dados fornecidos são inválidos', 400

        precisa_irrigar = umidade > 3001
        data = dataehora()  # Obtém a data e hora atuais
        
        if scheduled_job:
            schedule.cancel_job(scheduled_job)  # Cancela o job agendado se existir

        if umidade < 3001:
            # Agenda a gravação dos dados de umidade a cada 30 minutos
            scheduled_job = schedule.every(30).minutes.do(insert_data, data, umidade, precisa_irrigar)
        else:
            # Grava os dados de umidade imediatamente
            insert_data(data, umidade, precisa_irrigar)

        print("\033[34m*********>> RECEBI <<*********\n\033[0m")
        print(f'\033[92m Umidade recebida: {dados}\n\033[0m') 
        print("\033[34m**********************\n\033[0m")

        return f'Umidade salva com sucesso: {umidade}'
    else:
        print('\033[91mDados não fornecidos\033[0m')  
        return 'Dados não fornecidos', 400

# Rota para solicitar dados de umidade
@app.route('/puxar', methods=['GET'])
def puxa_umidade():
    global umidade
    if umidade is not None:
        print("\033[38;5;214m********>> SOLICITADA <<********\n\033[0m")
        print(f'\033[92m Umidade solicitada: {umidade}\n \033[0m')
        print("\033[38;5;214m**********************\n\033[0m")

        ultima_media = obter_ultima_media_diaria()
        if ultima_media:
            print(f'\033[92m Média diária mais recente: {ultima_media}\n\033[0m')
            return f'{umidade} {ultima_media}'
        else:
            print('\033[91m Nenhuma média diária disponível\033[0m')
            return f'{umidade}'
    else:
        print('\033[91m Umidade não disponível\033[0m')  
        return 'Umidade não disponível', 404

# Função para executar tarefas agendadas
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f"Operando no IP: {ip}")

    # Inicia a thread para executar tarefas agendadas
    schedule_thread = Thread(target=run_schedule)
    schedule_thread.daemon = True
    schedule_thread.start()

    app.run(host=ip, port=4000, debug=False)

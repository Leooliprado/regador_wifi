from datetime import datetime
from flask import Flask, request, jsonify
import socket
import schedule
import time
from threading import Thread
from multiprocessing import Value
from banco_de_dados import calcular_media_diaria, contar_precisa_irrigar, insert_data, limpar_tabela_media_diarias, obter_medias_diarias_semana, obter_ultima_media_diaria, pegar_tudo_tebala_irrigar  # Import para a função insert_data
from data_e_hora import dataehora

app = Flask(__name__)


ultima_data = Value('i',0)


# Variável global para armazenar a umidade
umidade = None
scheduled_job = None  # Variável para armazenar o job agendado

umidade_ideal = 2000



# Rota para receber dados de umidade do Arduino
@app.route('/umidade', methods=['POST'])
def coloca_umidade():
    global umidade
    dados = request.form.get("dados")
    if dados is not None:
        try:
            umidade = float(dados)
        except ValueError:
            return 'Dados fornecidos são inválidos', 400

        precisa_irrigar = umidade > umidade_ideal
        data = dataehora()  # Obtém a data e hora atuais

        
        # print(int(time.time()))
        # print(ultima_data.value)
        if int(time.time())-ultima_data.value > 1800:
            print("\033[34m************>> passou 30 minutos \n\033[0m")
            # fas mais que trita minutos
            ultima_data.value = int(time.time()) 
            
            insert_data(data, umidade, precisa_irrigar)
        
        if umidade > umidade_ideal:
            # schedule_insert_data(data, umidade, precisa_irrigar)
            insert_data(data, umidade, precisa_irrigar)
       
            

        print("\033[34m*****************>> RECEBI <<*****************\n\033[0m")

        print(f'\033[92m Umidade recebida: {dados}\n\033[0m') 

        print("\033[34m**********************************************\n\033[0m")

        return f'Umidade salva com sucesso: {umidade}'
    else:
        print('\033[91mDados não fornecidos\033[0m')  
        return 'Dados não fornecidos', 400

# Rota para solicitar dados de umidade
@app.route('/puxar', methods=['GET'])
def puxa_umidade():
    global umidade
    if umidade is not None:
        print("\033[38;5;214m***************>> SOLICITADA <<***************\n\033[0m")

        print(f'\033[92m Umidade solicitada: {umidade}\n \033[0m')

        print("\033[38;5;214m**********************************************\n\033[0m")
        

        if umidade > umidade_ideal:
            bomba_estado = True
        else:
            bomba_estado = False


        ultima_media = obter_ultima_media_diaria()
        medias_diarias_semana = obter_medias_diarias_semana()
        precisa_irrigar = contar_precisa_irrigar()
        tudo_tebala_irrigar = pegar_tudo_tebala_irrigar()


        if ultima_media is not None:
            print(f'\033[92m Média diária mais recente: {ultima_media}\n\033[0m')
            
            return jsonify({'umidade': umidade,
                             'media_diaria': ultima_media,
                             'medias_diarias_semana': medias_diarias_semana,
                             'precisa_irrigar':precisa_irrigar,
                             'estado_bomba': bomba_estado,
                             'tudo_tebala_irrigar':tudo_tebala_irrigar
                             })
        else:
            print('\033[91m ************>> Nenhuma média diária disponível\033[0m')

            return jsonify({'umidade': umidade,
                             'media_diaria': None,
                             'medias_diarias_semana': medias_diarias_semana,
                             'precisa_irrigar':precisa_irrigar,
                             'estado_bomba': bomba_estado,
                             'tudo_tebala_irrigar':tudo_tebala_irrigar
                             })
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

    schedule.every().day.at("00:00").do(calcular_media_diaria)
    schedule.every().saturday.at("23:59").do(limpar_tabela_media_diarias)

    schedule_thread = Thread(target=run_schedule)
    schedule_thread.daemon = True
    schedule_thread.start()

    app.run(host=ip, port=4000, debug=False)
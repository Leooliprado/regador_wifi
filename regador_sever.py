from flask import Flask, request
import socket

app = Flask(__name__)

# Variável global para armazenar a umidade
umidade = None

# arduino
@app.route('/umidade', methods=['POST'])
def coloca_umidade():
    global umidade
    dados = request.form.get("dados")
    if dados is not None:
        umidade = dados

        print("\033[34m************************>> RECEBI <<************************\n\033[0m")
        print(f'\033[92m Umidade recebida: {dados}\n\033[0m') 
        print("\033[34m************************************************************\n\033[0m")

        return f'Umidade salva com sucesso: {umidade}'
    else:
        print('\033[91mDados não fornecidos\033[0m')  
        return 'Dados não fornecidos', 400

# celular
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

if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f"Operando no IP: {ip}")

    app.run(host=ip, port=4000, debug=False)

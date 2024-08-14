import requests
from deep_translator import GoogleTranslator

def previsão_de_chuva():
    api_key = ""  
    city_name = "São Sebastião do Paraíso, BR"

    # URL base da API do OpenWeather
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
    
    # Concatenando a URL com o nome da cidade e a chave da API
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    complete_forecast_url = forecast_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    
    # Fazendo a solicitação para a API
    response = requests.get(complete_url)
    forecast_response = requests.get(complete_forecast_url)
    
    # Convertendo a resposta para o formato JSON
    data = response.json()
    forecast_data = forecast_response.json()
    
    # Criando uma instância do tradutor
    translator = GoogleTranslator(source='auto', target='pt')
    
    # Verificando se a cidade foi encontrada
    if data["cod"] != "404":
        # Extraindo os principais parâmetros da resposta
        main = data["main"]
        weather = data["weather"][0]
        rain = data.get("rain", {}).get("3h", 0)  # Precipitação nos últimos 3h ou 0 se não houver dados
        
        # Traduzindo a descrição para o português
        description = weather['description']
        translated_description = translator.translate(description)
        pop = forecast_data["list"][0]["pop"] * 100  # Convertendo para porcentagem
        
        # Exibindo as informações do clima
        print(f"Temperatura: {main['temp']}°C")
        print(f"Descrição: {translated_description}\n")
        #print(f"\033[34m  Precipitação (últimas 3 horas): {rain} mm \n\033[0m")
        print(f"\033[34mProbabilidade de chuva: {pop}%\n\033[0m")
        
        # Retornando os dados relevantes
        return {'pop': pop, 'temp': main['temp'], 'description': translated_description}
    else:
        print("Cidade não encontrada!")
        return None

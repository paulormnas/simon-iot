import requests
import json

dados = {
			'id':"dispositivo"
             'location': [22.3]
             'property': "temperatura",
             'date':12/12,
             'value': 22.1
        }

dados_json = json.dumps(dados)
enviar_dados = requests.post("http://192.168.1.4:8080/registrar_dados", data = dados_json)
print(enviar_dados)

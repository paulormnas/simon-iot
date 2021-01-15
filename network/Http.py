import requests
import json

class NetworkManager():
	def __init__(self, server_url, porta):
		self.server = server_url    #TODO: Inserir informaçoes do servidor em um arquivo de confiuraçao
		self.port = porta

	def enviar_dados(self, dados):
		''' Função para enviar os dados dos sensores para o servidor via POST HTTP '''
		json_data = json.dumps(dados)
		url = "http://" + self.server + ":" + str(self.port) + "/registrar_dados"
		request = requests.post(url, data=json_data)
		print(request)

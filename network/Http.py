# -*- coding: utf-8 -*-

import requests
import json

class HttpManager():
	def __init__(self, server_url, porta):
		self.server = server_url
		self.port = porta

	def enviar_dados(self, dados):
		''' Função para enviar os dados dos sensores para o servidor via POST HTTP '''
		json_data = json.dumps(dados)
		url = "http://" + self.server + ":" + str(self.port) + "/registrar_dados"
		request = requests.post(url, data=json_data)
		print(request)
	
	def conferir_assinatura(self, assinatura):
		''' Função para enviar assinatura para o servidor verifica-la via GET HTTP '''
		json_data = json.dumps(dados)
		url = "http://" + self.server + ":" + str(self.port) + "/verifica_dispositivo?device_id={}&data={}"
		response = requests.get(url.format(device_id, json_data), data=assinatura)
		print(response)


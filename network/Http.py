# -*- coding: utf-8 -*-

import requests
import json
from utils.Config import ConfigServer


class HttpManager():
	def __init__(self):
		self.config = ConfigServer()
		self.server_url = self.config.url
		self.port = self.config.port

	def enviar_dados(self, dados):
		''' Função para enviar os dados dos sensores para o servidor via POST HTTP '''
		json_data = json.dumps(dados)
		url = "http://" + self.server_url + ":" + str(self.port) + "/registrar_dados"
		request = requests.post(url, data=json_data)
		print(request)
	
	def conferir_assinatura(self, assinatura):
		''' Função para enviar assinatura para o servidor verifica-la via GET HTTP '''
		json_data = json.dumps(dados)
		url = "http://" + self.server_url + ":" + str(self.port) + "/verifica_dispositivo?device_id={}&data={}"
		response = requests.get(url.format(device_id, json_data), data=assinatura)
		print(response)


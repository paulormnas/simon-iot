import time
import json
import Adafruit_DHT
import RPi.GPIO as GPIO
from network.Http import NetworkManager

class Sensor():

    def __init__(self):
        self.nm = NetworkManager(server_url="192.168.1.8", porta=8080)

    def registrar_dados(dados):
        """
        Converte dicionario com informaçoes de mediçao em formato JSON e registra em um arquivo com extensão .json.

            :dados - dict
            :return - None
        """
        dados_json = json.dumps(dados)
        caminho_do_arquivo = "registro/" + dados["property"] + "/" + str(dados["date"]) + ".json"

        with open(caminho_do_arquivo, "a+") as f:
            f.write(dados_json)

    def formatar_dados(self, propriedade, valor):
        id = "dispositivo_001"      #TODO: Inserir ID do dispositivo em um arquivo de confiuraçao
        localizacao = ["-22.597412, -43.289396"] #TODO: Inserir informaçoes de localizaçao em um arquivo de confiuraçao
        data = time.time()

        dados = {'id': id,
                 'location': localizacao,
                 'property': propriedade,
                 'date': data,
                 'value': valor
                 }

        self.registrar_dados(dados)
        self.nm.enviar_dados(dados)

class DHT22(Sensor):
    def __init__(self, pino, quantidade_leituras, intervalo_medicao):
        self.DHT_SENSOR = Adafruit_DHT.DHT22
        self.DHT_PIN = pino
        self.NUMBER_OF_READINGS = quantidade_leituras
        self.INTERVAL = intervalo_medicao

    def ler_dados(self):
        #TODO: Implementar codigo de leitura dos dados do DHT
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return humidity, temperature

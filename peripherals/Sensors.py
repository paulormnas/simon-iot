# -*- coding: utf-8 -*-

import time
import json
import Adafruit_DHT
import RPi.GPIO as GPIO
import numpy as np

from security import Signature
from network.Http import NetworkManager
from utils.DataStructures import Fila


class Sensor():

    def __init__(self):
        # TODO: Inserir informaçoes do servidor em um arquivo de confiuraçao
        self.nm = NetworkManager(server_url="192.168.1.8", porta=8080)
        self.LAST_READ_TIME = time.time()
        self.signature = Signature()

    def registrar_dados(self, dados):
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
        """
        Verifica o desvio padrao de um conjunto de leituras em lista.

        :propriedade - string
        :valor - number

        """
        id = "dispositivo_001"      #TODO: Inserir ID do dispositivo em um arquivo de confiuraçao
        localizacao = [
            "-22.597412, -43.289396"]  # TODO: Inserir informaçoes de localizaçao em um arquivo de confiuraçao
        data = time.time()

        dados = {'id': id,
                 'location': localizacao,
                 'property': propriedade,
                 'date': data,
                 'value': valor
                 }

        assinatura = self.signature.sign(dados)
        dados["signature"] = assinatura
        self.registrar_dados(dados)
        self.nm.enviar_dados(dados)

    def verificar_desv_pad(self, leituras):
        """
        Verifica o desvio padrao de um conjunto de leituras em lista.

        :leituras - list
        :return - boolean

        """

        desv_pad = np.std(leituras)

        if (desv_pad < 10):
            return True
        else:
            return False

class DHT22(Sensor):
    def __init__(self, pino, quantidade_leituras, intervalo_medicao):
        '''
        Construtor da classe DHT22, onde pino identifica e a porta GPIO do Raspberry no qual o sensor se encontra
        conectado, quantidade_leituras esta relacionando com a quantidade de leituras que o sensor devera realizar
        para verificar o desvio padrao e consolidar uma unica mediçao e intervalo_medicao e o tempo, em segundos,
        entre mediçoes consecutivas.
        :pino - int
        :quantidade_leituras - int
        :intervalo_medicao: - int

        '''
        super().__init__()
        self.DHT_SENSOR = Adafruit_DHT.DHT22
        self.DHT_PIN = pino
        self.NUMBER_OF_READINGS = quantidade_leituras
        self.INTERVAL = intervalo_medicao
        self.fila_umidade = Fila(tamanho=self.NUMBER_OF_READINGS)
        self.fila_temperatura = Fila(tamanho=self.NUMBER_OF_READINGS)

    def ler_dados(self):
        tamanho_temperatura = 0
        tamanho_umidade = 0
        while (tamanho_temperatura <= self.NUMBER_OF_READINGS and
               tamanho_umidade <= self.NUMBER_OF_READINGS and
               time.time() - self.LAST_READ_TIME <= self.INTERVAL):

            umidade, temperatura = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
            if umidade is not None and temperatura is not None:
                print('{0},{1},{2:0.1f}*C,{3:0.1f}%rn'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'),
                                                              temperatura, umidade))
                lista_temporaria = []
                lista_temporaria.extend(self.fila_umidade.ler_itens())
                lista_temporaria.append(umidade)
                if self.verificar_desv_pad(lista_temporaria):
                    self.fila_umidade.adicionar_item(umidade)
                    self.formatar_dados("UMIDADE", umidade)

                lista_temporaria = []
                lista_temporaria.extend(self.fila_temperatura.ler_itens())
                lista_temporaria.append(temperatura)
                if self.verificar_desv_pad(lista_temporaria):
                    self.fila_temperatura.adicionar_item(temperatura)
                    self.formatar_dados("TEMPERATURA", temperatura)

            else:
                print("Falha ao receber os dados do sensor DHT22.")

            tamanho_temperatura = len(self.fila_temperatura.ler_itens())
            tamanho_umidade = len(self.fila_umidade.ler_itens())

class PIR(Sensor):
    def __init__(self, pino, intervalo_medicao):
        '''
        Construtor da classe DHT22, onde pino identifica e a porta GPIO do Raspberry no qual o sensor se encontra
        conectado e intervalo_medicao e o tempo, em segundos, entre mediçoes consecutivas.
        :pino - int
        :intervalo_medicao: - int

        '''
        super().__init__()
        self.PIN = pino
        self.INTERVAL = intervalo_medicao
        GPIO.setup(self.PIN, GPIO.IN)

    def ler_dados(self):
        if (time.time() - self.LAST_READ_TIME > self.INTERVAL and
                GPIO.input(self.PIN)):
            self.formatar_dados("MOVIMENTO", 1)
            self.LAST_READ_TIME = time.time()

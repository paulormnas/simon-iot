# -*- coding: utf-8 -*-
import configparser

from peripherals.Sensors import *
from network.Http import NetworkManager


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    ### Funcao principal do programa que controla todos o fluxos de execuçao ###
    # TODO: desenvolver funcionalidade de registro de reinicializaçao

    #Configura objeto para tratar requisiçoes via http
    # TODO: Inserir informaçoes do servidor em um arquivo de confiuraçao
    URL = config.get('server','url')
    Porta = config.getint('server','porta')
    
    nm = NetworkManager(server_url = URL, porta = Porta)

    # Configura sensores
    pinoDHT = config.getint('DHT','pino')
    leiturasDHT = config.getint('DHT','leituras')
    intervaloDHT = config.getint('DHT','intervalo')
    pinoPIR = config.getint('PIR','pino')
    intervaloPIR = config.getint('PIR','intervalo')
    
    dht = DHT22(pino = pinoDHT, quantidade_leituras = leiturasDHT, intervalo_medicao = intervaloDHT)
    pir = PIR(pino = pinoPIR, intervalo_medicao = intervaloPIR)
    lista_de_sensores = [dht, pir]


    # Loop infinito para realizar mediçoes e enviar dados para o servidor
    while (True):
        lista_de_envio = []
        for sensor in lista_de_sensores:
            lista_de_envio.extend(sensor.ler_dados)
        for dados in lista_de_envio:
            nm.enviar_dados(dados)


if __name__ == "__main__":
    main()

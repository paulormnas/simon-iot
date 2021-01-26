# -*- coding: utf-8 -*-
import subprocess

from peripherals.Sensors import *
from network.Http import NetworkManager
from utils.Log import log

def main():
    ### Funcao principal do programa que controla todos o fluxos de execuçao ###
    # Funcionalidade de registro de boot  
    log = log()
    log_register = log.boot_log()
    # Configura objeto para tratar requisiçoes via http
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    server = config['server']['url']
    port = config['server']['porta']
    nm = NetworkManager(server_url="192.168.1.8", porta=8080)

    # Configura sensores
    DHTconfig['pino'= config['DHT']['pino'], 'leituras'= config['DHT']['leituras'], 'intervalo'= config['DHT']['intervalo']]
    PIRconfig['pino'= config['PIR']['pino'], 'intervalo'= config['PIR']['intervalo']]
    
    dht = DHT22(pino= DHTconfig[pino], quantidade_leituras= DHTconfig[leituras], intervalo_medicao= DHTconfig[intervalo])
    pir = PIR(pino= PIRconfig[pino], intervalo_medicao= PIRconfig[intervalo])
    lista_de_sensores = [dht, pir]

    # Loop infinito para realizar mediçoes e enviar dados para o servidor
    while (True):
        lista_de_envio = []
        for sensor in lista_de_sensores:
            lista_de_envio.extend(sensor.ler_dados())
        for dados in lista_de_envio:
            nm.enviar_dados(dados)


if __name__ == "__main__":
    main()

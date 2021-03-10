# -*- coding: utf-8 -*-

from peripherals.Sensors import *
from network.Http import NetworkManager

def main():
    ### Funcao principal do programa que controla todos o fluxos de execuçao ###
    # TODO: desenvolver funcionalidade de registro de reinicializaçao

    #Configura objeto para tratar requisiçoes via http
    # TODO: Inserir informaçoes do servidor em um arquivo de confiuraçao
    nm = NetworkManager(server_url="192.168.1.8", porta=8080)

    # Configura sensores
    dht = DHT22(pino=4, quantidade_leituras=10, intervalo_medicao=300)
    pir = PIR(pino=11, intervalo_medicao=60)
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

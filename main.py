# -*- coding: utf-8 -*-

from peripherals.Sensors import *


def main():
    ### Funcao principal do programa que controla todos o fluxos de execuçao ###
    # TODO: desenvolver funcionalidade de registro de reinicializaçao

    # Configura sensores
    dht = DHT22(pino=22, quantidade_leituras=10, intervalo_medicao=300)
    pir = PIR(pino=17, intervalo_medicao=60)
    lista_de_sensores = [dht, pir]

    # Loop infinito para realizar mediçoes e enviar dados para o servidor
    while (True):
        for sensor in lista_de_sensores:
            sensor.ler_dados()


if __name__ == "__main__":
    main()

#-*- coding: UTF-8 -*-

import json
import subprocess
import random
import configparser
import time
from bluetooth import *
from security.Sign import Signature
from utils.Log import bluetooth_log_verify
from utils.Log import bluetooth_log_calibre

class bluetooth:
    
    def __init__(self):
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')        
        self.signature = Signature()
        self.log = LogManager()
        
    def bluetooth_connect(self):

        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
        signature = Signature()

        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)

        print("Criando serviço.")
        advertise_service(server_sock, "SiMon Meter Calibration", service_classes = [SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])
        print("Aguardando conexão.")

        client_sock, client_info = server_sock.accept()
        print("Conexão aceita com dispostivo ", client_info)
        client_sock.send("Rasp meter say Hello!")
        self.bluetooth_challenge()
    
    def bluetooth_challenge(self):
    
        while True:
            client_sock.send("Assine a informacao abaixo")
            # challenge = random.random()
            challenge = 0.033434099161654296
            print(challenge)
            assinatura = signature.sign(challenge)
            # print(assinatura)
            client_sock.send('challenge')
            data = client_sock.recv(2048)
            self.bluetooth_verify()
            
            # TODO: enviar data para o servidor conferir a assinatura
            
    def bluetooth_verify(self)
    
            data = data[:len(data)-2]
            if data == assinatura:
                print('Assinatura é válida')
                log_accept = self.log.bluetooth_log_connection(is_valid="valid", addr=client_info)
                print("Autenticado")
                print('Iniciando processo de calibração')
                log_calib = self.log.bluetooth_log_calibre()
                
            else:
                print('Assinatura é inválida')
                print("Resultado incorreto")
                log_refuse = self.log.bluetooth_log_connection(is_valid="invalid", addr=client_info)
                print("Closing sockets")
                client_sock.close()
                server_sock.close()
                break
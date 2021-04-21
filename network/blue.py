#-*- coding: UTF-8 -*-

import configparser
import json
import random
import subprocess
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
        self.client_sock = None
        self.client_info = None
        self.server_sock = None
        self.enable_device_scan()
        self.enable_calibration_service()
        
        self.challenge()        
        self.verify()
        self.close_connections()
        
    def enable_device_scan(self)
        
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
    
    def enable_calibration_service(self):    
              
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)

        print("Criando serviço.")
        advertise_service(self.server_sock, "SiMon Meter Calibration", service_classes = [SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])
        print("Aguardando conexão.")
        
    def service(self):
    
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Conexão aceita com dispostivo ", self.client_info)
        self.client_sock.send("Rasp meter say Hello!")
    
    def challenge(self):

        self.client_sock.send("Assine a informacao abaixo")
        # challenge = random.random()
        challenge = 0.033434099161654296
        print(challenge)
        assinatura = signature.sign(challenge)
        # print(assinatura)
        self.client_sock.send('challenge')
        self.client_sock.settimeout(5.0)
        data = self.client_sock.recv(2048)
            
        # TODO: enviar data para o servidor conferir a assinatura
            
    def verify(self)
    
        data = data[:len(data)-2]        
        if data == assinatura:
            print('Assinatura é válida')
            log_accept = self.log.bluetooth_log_connection(is_valid="valid", addr=self.client_info)
            print("Autenticado")
            print('Iniciando processo de calibração')
            log_calib = self.log.bluetooth_log_calibre()
                
        else:
            print('Assinatura é inválida')
            print("Resultado incorreto")
            log_refuse = self.log.bluetooth_log_connection(is_valid="invalid", addr=self.client_info)
            print("Closing sockets")
        
    def close_connections(self)
        self.client_sock.close()
        self.server_sock.close()
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'noscan'])
#-*- coding: UTF-8 -*-

import json
import subprocess
import random
import configparser
import time
from bluetooth import *
from security.Sign import Signature
from utils.Log import bluetooth_log

class bluetooth:
    
    def __init__(self):
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')        
        self.signature = Signature()        
        
    def bluetooth_start(self):

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

        while True:
            client_sock.send("Assine a informacao abaixo")
            # challenge = random.random()
            challenge = 0.033434099161654296
            print(challenge)
            assinatura = signature.sign(challenge)
            # print(assinatura)
            client_sock.send('challenge')
            data = client_sock.recv(2048)
            
            # TODO: enviar data para o servidor conferir a assinatura
            
            data = data[:len(data)-2]
            if data == assinatura:
                print('Assinatura é válida')
                print("Autenticado")
                print('Iniciando processo de calibração')
                timeStart = datetime.now().timestamp()
                self.bluetooth_log_accept()
                self.bluetooth_register(log)
                
            else:
                print('Assinatura é inválida')
                print("Resultado incorreto")
                self.bluetooth_log_refuse()
                self.bluetooth_register(log)
                print("Closing sockets")
                client_sock.close()
                server_sock.close()
                break

    def bluetooth_log_accept(self, timeStart):
                    
        date = datetime.now().timestamp()
        duration = timeStart - date
        _id = self.config.get('data','id')
        localizacao = self.config.get('data','localizacao')
                   
        log = {'id':_id,
                'socket':str(client_info),
                'property':'Calibracao',
                'localizacao':localizacao,
                'date':date,
                'info':'Validation Authenticated',
                'duration': duration
                #'signature': assinatura               
                }
            
        assinatura = self.signature.sign(log)
        assinatura = str(assinatura)
        log['signature'] = assinatura
        self.register(log)
        print(log)

    def bluetooth_log_refuse(self):
                    
        date = datetime.now().timestamp()
        _id = self.config.get('data','id')
        localizacao = self.config.get('data','localizacao')
                   
        log = {'id':_id,
                'socket':str(client_info),
                'property':'Calibracao',
                'localizacao':localizacao,
                'date':date,
                'info':'Validation Failed'
                #'signature': assinatura               
                }
            
        assinatura = self.signature.sign(log)
        assinatura = str(assinatura)
        log['signature'] = assinatura
        self.register(log)
        print(log)

    def bluetooth_register(self, log):
            
        log_json = json.dumps(log)
        caminho_do_arquivo = "registro/" + log["property"] + "/" + str(log["date"]) + ".json"
        with open(caminho_do_arquivo, "a+") as f:
            f.write(log_json)
    
bluetooth_start()
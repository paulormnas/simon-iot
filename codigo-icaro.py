#-*- coding: UTF-8 -*-

import subprocess
import random
from bluetooth import *
from security.Sign import Signature
from utils.Log import *

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
    challenge = random.seed()
    print(challenge)
    assinatura = signature.sign(challenge)
    print(assinatura)
    
    data = client_sock.recv(1024)
    data = data.decode('utf-8')            
    data = data[:len(data)-2]
    if data == assinatura:
            print('Assinatura é válida')
            print("Autenticado")
            print('Iniciando processo de calibração')
            """
            timeStart = datetime.now().timestamp()
            self.bluetooth_log_connection(is_valid="valid", addr=device_addr)
            self.bluetooth_register(log)
               """ 
    else:
            print('Assinatura é inválida')
            print("Resultado incorreto")
            """
            self.bluetooth_log_connection(is_valid="invalid", addr=device_addr)
            self.bluetooth_register(log)
            """
            print("Closing sockets")
            client_sock.close()
            server_sock.close()
            break

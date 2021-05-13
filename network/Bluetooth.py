# -*- coding: UTF-8 -*-
import random
import subprocess
import bluetooth
from utils.Log import LogManager
from network.Http import HttpManager
from security.Sign import Signature

START_CONNECTION = '1000'
ACK = '1001'
CHALLENGE = '1002'


class BluetoothManager(object):
    def __init__(self):
        self.log = LogManager()
        self.sock = None
        self.is_connected = False
        self.enable_device_scan()

    @staticmethod
    def enable_device_scan():
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
        
    def accept_connection():
        client_sock, client_info = server_sock.accept()

    def send_data(self, data):
        # self.server_sock.settimeout(5.0)
        self.sock.send(data)            
    
    def receive_data(self):
        return self.sock.recv(1024)

    def close_connections(self):
        self.client_sock.close()
        self.sock.close()
        self.disable_device_scan()
        self.is_connected = False

    @staticmethod
    def disable_device_scan():
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'noscan'])

    @property
    def is_connected(self):
        return self.is_connected


class BluetoothManagerStandard(BluetoothManager):
    def __init__(self):
        super().__init__()
        self.enable_calibration_service()

    def enable_calibration_service(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.bind(("", bluetooth.PORT_ANY))
        self.sock.listen(1)
        print('Criando serviço de calibração...')
        bluetooth.advertise_service(self.sock,
                                    "SiMon Meter Calibration",
                                    service_classes=[bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Aguardando conexão.")
    
    def receive_challenge(self):
        self.accept_connection()
        data = self.receive_data()
        if data == 'challenge'
            self.sign_challenge()
        else
            self.receive_challenge()
        
    def sign_challenge(self):
        challenge = self.receive_data()
        signed_challenge = Signature.sign(challenge)
        self.send_data(signed_challenge)


class BluetoothManagerMeter(BluetoothManager):
    def __init__(self):
        super().__init__()
        self.find_and_authenticate_standard()

    def find_and_authenticate_standard(self):
        standard_addrs = self.find_standards()
        self.connect_to_standard(standard_addrs)
        self.authenticate()

    def find_standards(self):
        print("Dispositivos encontrados:")
        print("Nome \t\t Endereço")
        nearby_devices = []
        standard_addrs = []
        trials = 0
        while trials < 3 and len(nearby_devices) == 0:
            nearby_devices = bluetooth.find_devices()
            standard_addrs = self.get_nearby_devices_address(nearby_devices)
            trials += 1
        return standard_addrs

    @staticmethod
    def get_nearby_devices_address(nearby_devices):
        devices_addrs = []
        for address in nearby_devices:
            name = bluetooth.lookup_name(address)
            print(name, "\t", address)
            if name == 'SiMon-standard':
                devices_addrs.append(address)
        return devices_addrs

    def connect_to_standard(self, standard_addrs):
        for addr in standard_addrs:
            services = bluetooth.find_service(address=addr,
                                              name='SiMon Meter Calibration',
                                              uuid=bluetooth.SERIAL_PORT_CLASS)
            if len(services) > 0:
                service = services[0]
                self.connect_socket(service, addr)
                self.authenticate()
                if self.is_connected:
                    break
            else:
                print(f'Serviço de calibração não encontrado para o endereço: {addr}')

    def connect_socket(self, service, addr):
        self.log.generate_bluetooth_new_connection_attempt_log(addr=self.client_info)
        port = service["port"]
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr, port))
        self.send_data(START_CONNECTION)

    def authenticate(self):
        self.send_data(CHALLENGE)
        challenge_value = random.random()
        self.send_data(challenge_value)
            #if self.server_sock.settimeout == 0
                #response = 'timeout'
                #self.check_server_response(response)
            #else:
        data = self.receive_data()
        http = HttpManager()
        response = http.conferir_assinatura(data)
        self.check_server_response(response)

    def check_server_response(self, response):
        if response == 'valid':
            print('Padrao autenticado pelo servidor')
            self.log.generate_bluetooth_new_valid_connection_log(is_valid=True, addr=self.client_info)
            self.is_connected = True
        else:
            print('Padrao nao autenticado pelo servidor')
            self.log.generate_bluetooth_new_failed_connection_log(is_valid=False, addr=self.client_info, response)


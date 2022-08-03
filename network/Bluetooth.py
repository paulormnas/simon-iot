# -*- coding: UTF-8 -*-
import sys
import random
import subprocess
import bluetooth
import time
import json
from utils.Log import LogManager
from network.Http import HttpManager
from security.Sign import Signature
from utils.Config import ConfigDeviceInfo

START_CONNECTION = "1000"
START_AUTH = "1001"
ACK = "1002"
CHALLENGE = "1003"
TIMEOUT = "1004"
SEND_MEASURE = "1005"
MEASURE = "1006"
ERROR_JSON = "1010"



class BluetoothManager(object):
    def __init__(self):
        self.log = LogManager()
        self.config = ConfigDeviceInfo()
        self.sock = None
        self.client_sock = None
        self.connected = False
        self.enable_device_scan()

    @staticmethod
    def enable_device_scan():
        subprocess.call(["sudo", "hciconfig", "hci0", "piscan"])
        subprocess.call(["sudo", "hciconfig", "hci0", "sspmode", "1"])

    def send_data_to_meter(self, cmd, data=""):
        payload = self.compose_payload(cmd, data)
        self.client_sock.send(payload)

    def send_data_to_standard(self, cmd, data=""):
        payload = self.compose_payload(cmd, data)
        self.sock.send(payload)

    def send_measure_to_standard(self, property_, value=""):
        payload = self.compose_measure(property_, value)
        self.sock.send(payload)

    @staticmethod
    def compose_measure (property_, value):
        menssage = {"property": property_, "value": value, "cmd": MEASURE}
        payload = json.dumps(menssage)
        return payload

    @staticmethod
    def compose_payload(cmd, data):
        payload = {"cmd": cmd, "data": data}
        return json.dumps(payload)

    def receive_data(self, socket):
        incoming = {}
        try:
            payload = socket.recv(2048)
            incoming = json.loads(payload)
        except bluetooth.BluetoothError as err:
            incoming = {"cmd": TIMEOUT}
            if hasattr(err, "message"):
                print(err.message)
        except json.decoder.JSONDecodeError as err:
            incoming = {'cmd': ERROR_JSON}
            if hasattr(err, 'message'):
                print(err.message)
        return incoming
        
    def receive_measure(self):
        incoming = {'cmd': '', 'property': '', 'value': ''}
        try:
            payload = self.client_sock.recv(2048)
            incoming = json.loads(payload)
        except bluetooth.BluetoothError as err:
            incoming = {'cmd': TIMEOUT}
            if hasattr(err, 'message'):
                print(err.message)
        except json.decoder.JSONDecodeError as err:
            incoming = {'cmd': ERROR_JSON}
            if hasattr(err, 'message'):
                print(err.message)
                
        return incoming

    def close_connections(self):
        if self.client_sock != None:
            self.client_sock.close()

        if self.sock != None:
            self.sock.close()

        #TODO: Tratar busca por dispositivo de calibração
        #self.disable_device_scan()
        self.connected = False
        

    @staticmethod
    def disable_device_scan():
        subprocess.call(["sudo", "hciconfig", "hci0", "noscan"])
        subprocess.call(["sudo", "hciconfig", "hci0", "sspmode", "0"])

    def is_connected(self):
        return self.connected


class BluetoothManagerStandard(BluetoothManager):
    def __init__(self):
        super().__init__()
        self.enable_calibration_service()

    def enable_calibration_service(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.bind(("", bluetooth.PORT_ANY))
        self.sock.listen(1)
        self.sock.settimeout(10.0)
        print("[BLUETOOTH-STANTDARD]: Criando serviço de calibração...")
        bluetooth.advertise_service(
            self.sock,
            "SiMon Meter Calibration",
            service_classes=[bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
        )
        print("[BLUETOOTH-STANTDARD]: Aguardando conexão.")
        self.verify_connection()

    def handle_requests(self):
        while True:
            if not self.is_connected():
                self.verify_connection()
            else:
                data = self.receive_data(self.client_sock)
                print(f"[BLUETOOTH-STANTDARD]: Data received: {data}")
                if data["cmd"] == TIMEOUT or data["cmd"] == ACK:
                    self.close_connections()
                    break
                if data["cmd"] == START_AUTH:
                    config = ConfigDeviceInfo()
                    self.send_data_to_meter(ACK, config.id)
                if data["cmd"] == CHALLENGE:
                    signed_challenge = self.sign_challenge(data["data"])
                    self.send_data_to_meter(ACK, signed_challenge)

    def verify_connection(self):
        try:
            self.client_sock, addr = self.sock.accept()
            self.client_sock.settimeout(10.0)
            name = bluetooth.lookup_name(addr[0])
            print(
                f"[BLUETOOTH-STANTDARD]: Conectado ao dispositivo com endereço {addr} e nome {name}"
            )
            self.connected = True
            data = self.receive_data(self.client_sock)
            if data["cmd"] == START_CONNECTION:
                self.send_data_to_meter(ACK, self.config.id)
            else:
                print("[BLUETOOTH-STANTDARD]: Timeout na recepção de dados")
        except bluetooth.BluetoothError:
            print(
                "[BLUETOOTH-STANTDARD]: Timeout na identificação de novos dispositivos"
            )
            print("[BLUETOOTH-STANTDARD]: Aguardando conexão.")

    def sign_challenge(self, challenge):
        print(f"[BLUETOOTH-STANTDARD]: Challenge recebido: {challenge}")
        s = Signature()
        return s.sign(challenge)


class BluetoothManagerMeter(BluetoothManager):
    def __init__(self):
        super().__init__()
        self.device_connected_addr = ""
        self.find_and_connect_to_standard()
        if self.is_connected():
            self.authenticate()

    def find_and_connect_to_standard(self):
        standard_addrs = self.find_standards()
        if len(standard_addrs) == 0:
            print("[BLUETOOTH-METER]: Nenhum dispositivo encontrado")
        else:
            self.connect_to_standard(standard_addrs)

    def find_standards(self):
        nearby_devices = []
        standard_addrs = []
        trials = 0
        while trials < 3 and len(nearby_devices) == 0:
            nearby_devices = bluetooth.discover_devices()
            if len(nearby_devices) > 0:
                standard_addrs = self.get_standard_devices_address(nearby_devices)
            trials += 1
        return standard_addrs

    @staticmethod
    def get_standard_devices_address(nearby_devices):
        print("[BLUETOOTH-METER]: Dispositivos encontrados:")
        print("Nome \t\t Endereço")
        devices_addrs = []
        for address in nearby_devices:
            name = bluetooth.lookup_name(address)
            print(name, "\t", address)
            if name == "SiMon-standard":
                devices_addrs.append(address)
        return devices_addrs

    def connect_to_standard(self, standard_addrs):
        for addr in standard_addrs:
            services = bluetooth.find_service(
                address=addr,
                name="SiMon Meter Calibration",
                uuid=bluetooth.SERIAL_PORT_CLASS,
            )
            if len(services) > 0:
                print("[BLUETOOTH-METER]: Padrão encontrado")
                service = services[0]
                self.connect_socket(service, addr)
                if self.is_connected():
                    break
            else:
                print(
                    f"[BLUETOOTH-METER]: Serviço de calibração não encontrado para o endereço: {addr}"
                )

    def connect_socket(self, service, addr):
        print("[BLUETOOTH-METER]: Tentando conectar ao serviço de calibração")
        port = service["port"]
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr, port))
        self.sock.settimeout(10.0)
        if self.sock is not None:
            print("[BLUETOOTH-METER]: Conectado ao serviço")
            self.send_data_to_standard(START_CONNECTION)
            response = self.receive_data(self.sock)
            print(f"[BLUETOOTH-METER]: {response}")
            if response["cmd"] == ACK:
                self.connected = True
                self.device_connected_addr = addr

    def authenticate(self):
        self.send_data_to_standard(START_AUTH)
        response = self.receive_data(self.sock)
        if response["cmd"] == ACK:
            standard_id = response["data"].decode()
            print("[BLUETOOTH-METER]: Iniciando autenticação do padrão.")
            print("[BLUETOOTH-METER]: Device ID = ", standard_id)
            challenge_value = str(random.random())
            print("[BLUETOOTH-METER]: Enviando desafio...")
            self.send_data_to_standard(CHALLENGE, challenge_value)
            print("[BLUETOOTH-METER]: Aguardando resposta...")
            response = self.receive_data(self.sock)
            if response["cmd"] == ACK:
                http = HttpManager()
                print("[BLUETOOTH-METER]: Enviando resposta para o servidor...")

                response = http.conferir_assinatura(
                    standard_id, challenge_value, response["data"]
                )
                self.check_server_response(response)
        else:
            self.close_connections()

    def check_server_response(self, response):
        if response == "valid":
            self.send_data_to_standard(ACK)
            print("[BLUETOOTH-METER]: Padrão autenticado pelo servidor")
            self.log.generate_bluetooth_new_valid_connection_log(
                addr=self.device_connected_addr
            )
        else:
            print("[BLUETOOTH-METER]: Padrão não autenticado pelo servidor")
            self.log.generate_bluetooth_new_failed_connection_log(
                addr=self.device_connected_addr,
                reason = "Padrão não autenticado pelo servidor"
            )
            self.connected = False
            self.close_connections()
            self.disable_device_scan()

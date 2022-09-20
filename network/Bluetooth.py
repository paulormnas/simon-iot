# -*- coding: UTF-8 -*-
import sys
import random
import subprocess
import bluetooth
import time
import json
import os
from datetime import datetime
from utils.Log import LogManager
from network.Http import HttpManager
from security.Sign import Signature
from utils.Config import ConfigDeviceInfo
from peripherals.Sensors import DHT22

counter = {}
START_CONNECTION = "1000"
START_AUTH = "1001"
ACK = "1002"
CHALLENGE = "1003"
TIMEOUT = "1004"
SEND_MEASURE = "1005"
MEASURE = "1006"
ERROR_JSON = "1010"
AUTHENTICATED = "1011"
PING = "1012"
PONG = "1013" 


class BluetoothManager(object):
    def __init__(self):
        self.log = LogManager()
        self.config = ConfigDeviceInfo()
        self.sock = None
        self.client_sock = None
        self.connected = False
        self.is_authenticated = False
        self.is_calibrating = False
        self.enable_device_scan()
        
    @staticmethod
    def enable_device_scan():
        subprocess.call(["sudo", "hciconfig", "hci0", "piscan"])
        subprocess.call(["sudo", "hciconfig", "hci0", "sspmode", "1"])

    def send_data_to_meter(self, cmd, data=""):
        payload = self.compose_payload(cmd, data)
        try:
            self.client_sock.send(payload)
        except bluetooth.BluetoothError as err:
            print("[BLUETOOTH-STANDARD]: ERRO DE COMUNICAçãO COM O MEDIDOR ")
            self.close_connections()

    def send_data_to_standard(self, cmd, data=""):
        payload = self.compose_payload(cmd, data)
        try:
            self.sock.send(payload)
        except bluetooth.BluetoothError as err:
            print("[BLUETOOTH-METER]: ERRO DE COMUNICAçãO COM O PADRÃO ")
            self.close_connections()

    def send_measure_to_standard(self, property_, value=""):
        payload = self.compose_measure(property_, value)
        try:
            self.sock.send(payload)
        except bluetooth.BluetoothError as err:
            print("[BLUETOOTH-METER]: ERRO DE COMUNICAçãO COM O PADRÃO ")
            self.close_connections()

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
        self.is_authenticated = False
        self.is_calibrating = False
        

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
        self.handle_requests()

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
                
            if self.is_connected() and not self.is_authenticated:
                data = self.receive_data(self.client_sock)
                print(f"[BLUETOOTH-STANTDARD]: Data received: {data}")
                if data["cmd"] == TIMEOUT:
                    self.close_connections()
                    break
                if data["cmd"] == START_AUTH:
                    config = ConfigDeviceInfo()
                    self.send_data_to_meter(ACK, config.id)
                if data["cmd"] == CHALLENGE:
                    signed_challenge = self.sign_challenge(data["data"].encode("utf8"))
                    self.send_data_to_meter(ACK)
                    self.client_sock.send(signed_challenge)
                if data["cmd"] == AUTHENTICATED:
                    self.is_authenticated = True
                if data["cmd"] == PING:
                    self.send_data_to_meter (cmd = PONG)
            if self.is_connected() and self.is_authenticated:
                self.manager_calibration()
                
    def manager_calibration(self):
        global counter
        
        counter = {"TEMPERATURA": 0, "UMIDADE": 0}
        os.environ['NUMBER_OF_PROPERTIES'] = "2"
        ultima_medicao = 0
        message_counter = 0
        total_measures = 0
        print("[BLUETOOTH-STANTDARD]: Aguardando inicío da calibração.")
        
        while self.is_connected():
            n_readings = int(os.environ['N_READINGS'])
            intervalo = int(os.environ['INTERVALO'])
            start_readings = os.environ['START_READINGS'] == "True"
            pause = os.environ['PAUSE'] == "True"
            is_timing_to_measure = (datetime.now().timestamp() - ultima_medicao) >= intervalo
            if start_readings and not pause and is_timing_to_measure:
                
                if counter["TEMPERATURA"] < n_readings:
                    self.manager_measures(n_readings, "TEMPERATURA")
                    total_measures += 1
                if counter["UMIDADE"] < n_readings:
                    self.manager_measures(n_readings, "UMIDADE")
                    total_measures += 1
                ultima_medicao = datetime.now().timestamp()
                message_counter = 0
                os.environ['TOTAL_MEASURES_COUNTER'] = str(total_measures)
            
            if not is_timing_to_measure:
                if message_counter < 1:
                    print("not timing to measure")
                    message_counter += 1
            
            if n_readings == 0 and not start_readings and not pause:
                n_readings = -1
                print("[BLUETOOTH]: Ending calibration")
                message_counter = 0
                
            if self.is_counter_complete(n_readings) and n_readings > 0:
                for key in counter:
                    counter[key] = 0
                n_readings = 0
                start_readings = False
                
            os.environ['N_READINGS'] = str(n_readings)
            os.environ['START_READINGS'] = str(start_readings)
            time.sleep(1)

    @staticmethod
    def is_counter_complete(n_readings):
        global counter

        results = [counter[key] == n_readings for key in counter]
        return all(results)
        
    def manager_measures(self,n_readings, property_):
        global counter

        dht = DHT22()
        self.send_data_to_meter(cmd=SEND_MEASURE, data=property_)
        incoming_msg = self.receive_measure()
        if incoming_msg["cmd"] == MEASURE:
            self.send_data_to_meter(cmd=ACK, data="")
            if incoming_msg["value"] is not None:
                standard_temperature, standard_humidity = dht.read_temperature_and_humidity()
                client_property = incoming_msg["property"]
                client_measure = float(incoming_msg["value"])
                if client_property == "TEMPERATURA" and client_measure is not None:
                    counter["TEMPERATURA"] += 1
                    dht.register_measures(n_readings, client_property, standard_temperature, client_measure)
                elif client_property == "UMIDADE" and client_measure is not None:
                    counter["UMIDADE"] += 1
                    dht.register_measures(n_readings, client_property, standard_humidity, client_measure)

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
        print(f"[BLUETOOTH-STANTDARD]: Challenge recebido")
        s = Signature()
        return s.sign(challenge)


class BluetoothManagerMeter(BluetoothManager):
    def __init__(self):
        super().__init__()
        self.device_connected_addr = ""
        self.handle_calibration()

    
    def handle_calibration(self):
        dht = DHT22()
        contador_timeout = 0
        
        while True:
            if not self.is_connected():
                self.find_and_connect_to_standard()
                
            if self.is_connected() and not self.is_authenticated:
                self.authenticate()
                
            if self.is_connected() and self.is_authenticated and self.is_calibrating:
                incoming_msg = self.receive_data(self.sock)
                cmd = incoming_msg["cmd"]
                if cmd == SEND_MEASURE:
                    temperatura, umidade = dht.read_temperature_and_humidity()
                    if incoming_msg['data'] == "TEMPERATURA":
                        self.send_measure_to_standard(property_="TEMPERATURA", value=temperatura)
                    elif incoming_msg['data'] == "UMIDADE":
                        self.send_measure_to_standard(property_="UMIDADE", value=umidade)
                    contador_timeout = 0
                if incoming_msg["cmd"] == TIMEOUT:
                    contador_timeout = self.check_connection_to_standard(contador_timeout)
                else:
                    contador_timeout = 0

    def check_connection_to_standard(self, contador_timeout):
        self.send_data_to_standard(cmd = PING)
        is_alive = self.receive_data(self.sock)
        if is_alive["cmd"] == TIMEOUT:
            contador_timeout += 1
        if contador_timeout == 4:
            print("FECHANDO CONEXÃO COM O DISPOSITIVO PADRÃO POR TIMEOUT")
            self.close_connections()
            contador_timeout = 0 
        return contador_timeout
             
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
                    self.standard_address = addr
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
            standard_id = response["data"]
            print("[BLUETOOTH-METER]: Iniciando autenticação do padrão.")
            print("[BLUETOOTH-METER]: Device ID = ", standard_id)
            challenge_value = str(random.randint(1000000,100000000))
            print("[BLUETOOTH-METER]: Enviando desafio...")
            self.send_data_to_standard(CHALLENGE, challenge_value)
            print("[BLUETOOTH-METER]: Aguardando resposta...")
            response = self.receive_data(self.sock)
            if response["cmd"] == ACK:
                signature = self.sock.recv(2048)
                http = HttpManager()
                print("[BLUETOOTH-METER]: Enviando resposta para o servidor...")

                response = http.conferir_assinatura(
                    standard_id, challenge_value, signature
                )
                self.check_server_response(response)
        else:
            self.close_connections()


    def check_server_response(self, response):
        if response == "valid":
            self.is_authenticated = True
            self.is_calibrating = True
            self.send_data_to_standard(AUTHENTICATED)

            print("[BLUETOOTH-METER]: Padrão autenticado pelo servidor")
        else:
            print("[BLUETOOTH-METER]: Padrão não autenticado pelo servidor")
            self.connected = False
            self.close_connections()
            self.disable_device_scan()


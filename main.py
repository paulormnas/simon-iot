# -*- coding: utf-8 -*-
import threading, json, asyncio
from peripherals.Sensors import DHT22, PIR
from network import Bluetooth, Http, websocket
from utils.Log import LogManager
from utils.Config import ConfigDeviceInfo
from datetime import datetime

MODE = "meter"
counter = {}
is_websocket_connected = False


def main():
    log = LogManager()
    log.generate_boot_log()

    config = ConfigDeviceInfo()
    if config.type == "meter":
        run_meter_mode()
    if config.type == "standard":
        run_standard_mode()

def run_meter_mode():    
    threading.Thread(
        target=bluetooth_meter_handler,
    ).start()

    http = Http.HttpManager()
    sensors = config_sensors()
    while True:
        data_to_send = [sensor.read for sensor in sensors]
        for data in data_to_send:
            if data is not None:
                http.enviar_dados(data)


def bluetooth_meter_handler():
    blue = Bluetooth.BluetoothManagerMeter()


def config_sensors():
    dht = DHT22()
    #pir = PIR()
    return [dht]


def run_standard_mode():
    ws = websocket.Client(
         host="192.168.0.24",
     )
    ws.start()
    
    bt = Bluetooth.BluetoothManagerStandard()

if __name__ == "__main__":
    main()

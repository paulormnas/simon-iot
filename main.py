# -*- coding: utf-8 -*-
from peripherals.Sensors import DHT22, PIR
from network import Bluetooth, Http
from utils.Log import LogManager
from utils.Config import ConfigDeviceInfo


def main():
    log = LogManager()
    log.generate_boot_log()

    config = ConfigDeviceInfo()
    if config.type == 'meter':
        run_meter_mode()
    if config.type == 'standard':
        run_standard_mode()


def run_meter_mode():
    threading.Thread(target=bluetooth_meter_handler, ).start()
    http = Http.HttpManager()
    sensors = config_sensors()
    while True:
        # TODO: check for calibration event
        data_to_send = [sensor.read for sensor in sensors]
        for data in data_to_send:
            if data is not None:
                http.enviar_dados(data)

def bluetooth_meter_handler()
    blue = Bluetooth.BluetoothManagerMeter()

def config_sensors():
    dht = DHT22()
    pir = PIR()
    return [dht, pir]


def run_standard_mode():
    blue = Bluetooth.BluetoothManagerStandard()
    while True:
        handle_requests(blue)


def handle_requests(std_bluetooth):
    data = std_bluetooth.receive_data()
    if data == Bluetooth.CHALLENGE:
        challenge = std_bluetooth.receive_data()
        std_bluetooth.sign_challenge(challenge)


if __name__ == "__main__":
    main()
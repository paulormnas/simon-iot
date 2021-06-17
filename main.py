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

    http = Http.HttpManager()
    sensors = config_sensors()
    calibration = True
    while True:
        # TODO: check for calibration event
        if calibration:
            bt = Bluetooth.BluetoothManagerMeter()

        data_to_send = [sensor.read for sensor in sensors]
        for data in data_to_send:
            if data is not None:
                http.enviar_dados(data)


def config_sensors():
    dht = DHT22()
    pir = PIR()
    return [dht]


def run_standard_mode():
    bt = Bluetooth.BluetoothManagerStandard()
    bt.handle_requests()


if __name__ == "__main__":
    main()

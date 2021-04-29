# -*- coding: utf-8 -*-
from peripherals.Sensors import DHT22, PIR
from network.Http import HttpManager
from utils.Log import LogManager


def main():
    log = LogManager()
    log.generate_boot_log()
    http = HttpManager()
    sensors_list = config_sensors()
    while True:
        data_to_send = [sensor.read for sensor in sensors_list]
        for data in data_to_send:
            http.enviar_dados(data)


def config_sensors():
    dht = DHT22()
    pir = PIR()
    return [dht, pir]


if __name__ == "__main__":
    main()

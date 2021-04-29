# -*- coding: utf-8 -*-
from peripherals.Sensors import DHT22, PIR
from network.Http import HttpManager
from utils.Log import LogManager
from utils.Config import ConfigSensors


def main():
    log = LogManager()
    log.generate_boot_log()
    http = HttpManager()
    sensors_list = config_sensors()
    while True:
        data_to_send = [sensor.ler_dados for sensor in sensors_list]
        for data in data_to_send:
            http.enviar_dados(data)


def config_sensors():
    config = ConfigSensors()
    dht = DHT22(pino=config.DHT_pin,
                quantidade_leituras=config.DHT_number_of_readings,
                intervalo_medicao=config.DHT_interval)
    pir = PIR(pino=config.PIR_pin,
              intervalo_medicao=config.PIR_interval)
    return [dht, pir]


if __name__ == "__main__":
    main()

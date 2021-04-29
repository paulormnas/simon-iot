# -*- coding: utf-8 -*-
import subprocess
import json
from os import environ

from datetime import datetime
from security.Sign import Signature
from .Config import ConfigDeviceInfo


class LogManager(object):
    
    def __init__(self):
        self.config = ConfigDeviceInfo()
        self._id = self.config.id
        self._location = self.config.location
        self.signature = Signature()

    def generate_boot_log(self):
        boot_date = self.get_last_boot_date()
        timestamp = datetime.now().timestamp()
        log = {'id': self._id,
               'property': 'boot_log',
               'location': self._location,
               'date': timestamp,
               'info': boot_date
               }
        self.sign(log)

    @staticmethod
    def get_last_boot_date():
        result = subprocess.check_output(['who', '-b'], text=True)
        date_text = result.split()[-2]
        hour_text = result.split()[-1]
        hour, minute = hour_text.split(':')
        hour = int(hour)
        minute = int(minute)
        boot_date = datetime.fromisoformat(date_text)
        boot_date = boot_date.replace(hour=hour, minute=minute)
        boot_date = str(boot_date)
        return boot_date

    def generate_bluetooth_new_connection_log(self, is_valid, addr):
        timestamp = datetime.now().timestamp()
        log = {'id': self._id,
               'property': 'new_bluetooth_connection',
               'location': self._location,
               'date': timestamp,
               'device-addr': addr
               }
        
        if is_valid == "valid":
            log['info'] = 'Device Authenticated'
                        
        else:
            log['info'] = 'Authentication Failed'

        self.sign(log)
                
    def generate_calibration_start_log(self):
        timestamp = datetime.now().timestamp()

        log = {'id': self._id,
               'property': 'calibration_started',
               'location': self._location,
               'date': timestamp,
               }
        self.sign(log)

    def sign(self, dados):
        assinatura = self.signature.sign(dados)
        assinatura = str(assinatura)
        dados['signature'] = assinatura
        self.register(dados)

    @staticmethod
    def register(self, log):
        path_start = 'registros/'
        if environ['SIMON_IOT_MODE'] == 'test':
            path_start = '../registros/'
        log_date = str(log["date"])
        caminho_do_arquivo = f'{path_start}Log/{log_date}.json'
        with open(caminho_do_arquivo, "a+") as f:
            log_json = json.dumps(log)
            f.write(log_json)

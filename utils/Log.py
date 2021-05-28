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
        self.log = {'id': self._id,
                   'property': '',
                   'location': self._location,
                   'date': 0,
                   'info': ''
                   }

    def generate_boot_log(self):
        log = self.log
        boot_date = self.get_last_boot_date()
        timestamp = datetime.now().timestamp()
        log['property'] = 'boot_log'
        log['date'] = timestamp
        log['info'] = boot_date
        self.sign(log)
        self.register(dados)

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

    def generate_bluetooth_new_valid_connection_log(self, addr):
        log = self.log
        timestamp = datetime.now().timestamp()
        log['property'] = 'new_bluetooth_connection'
        log['date'] = timestamp
        log['device-addr'] = addr
        log['info'] = 'Device Authenticated'
        self.sign(log)
        self.register(dados)
    
    def generate_bluetooth_failed_connection_log(self, addr, reason):
        log = self.log
        timestamp = datetime.now().timestamp()
        log['property'] = 'new_bluetooth_connection'
        log['date'] = timestamp
        log['device-addr'] = addr
        log['info'] = reason
        self.sign(log)
        self.register(dados)
        
    def generate_bluetooth_new_connection_attempt_log(self, addr):
        log = self.log
        timestamp = datetime.now().timestamp()
        log['property'] = 'new_bluetooth_connection_attempt'
        log['date'] = timestamp
        log['device-addr'] = addr
        self.sign(log)
        self.register(dados)
                
    def generate_calibration_start_log(self):
        log = self.log
        timestamp = datetime.now().timestamp()
        log['property'] = 'calibration_started'
        log['date'] = timestamp
        self.sign(log)
        self.register(dados)

    def sign(self, dados):
        assinatura = self.signature.sign(dados)
        assinatura = str(assinatura)
        dados['signature'] = assinatura

    @staticmethod
    def register(log):
        path_start = 'registros/'
        path_start = '../registros/'
        log_date = str(log["date"])
        caminho_do_arquivo = f'{path_start}Log/{log_date}.json'
        with open(caminho_do_arquivo, "a+") as f:
            log_json = json.dumps(log)
            f.write(log_json)

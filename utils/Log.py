# -*- coding: utf-8 -*-
import subprocess
import json
import configparser
import time
from datetime import datetime
from peripherals.Sensors import Sensor
from security.Sign import Signature

class log():
    
    def boot_log(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        signature = Signature()
        
        result = subprocess.check_output(['who', '-b'], text=True)
        print(result.split())
        date_text = result.split()[2]
        hour_text = result.split()[3]
        hour = int(hour_text.split(':')[0])
        minute = int(hour_text.split(':')[1])
        boot_date = datetime.fromisoformat(date_text)
        boot_date = boot_date.replace(hour=hour, minute=minute)
        boot_date = boot_date.timestamp()
        date = datetime.now().timestamp()        
        ID = config.get('data','id')
        localizacao = config.get('data','localizacao')
        data = time.time()
        
        log = {'id':ID,
                'property':'Log',
                'localizacao':localizacao,
                'date':data,
                'info':boot_date
                #'signature': assinatura               
                }
        
        assinatura = signature.sign(log)
        assinatura = str(assinatura)
        log['signature'] = assinatura
        self.registrar_log(log)
        print(log)
        
    def registrar_log(self, log):
        
        log_json = json.dumps(log)
        caminho_do_arquivo = "registro/" + log["property"] + "/" + str(log["date"]) + ".json"
        with open(caminho_do_arquivo, "a+") as f:
            f.write(log_json)
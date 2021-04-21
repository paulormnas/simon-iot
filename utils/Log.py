# -*- coding: utf-8 -*-
import subprocess
import json
import configparser
import time
from datetime import datetime
from security.Sign import Signature

class LogManager():
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.signature = Signature()

    def generate_boot_log(self):
                
        result = subprocess.check_output(['who', '-b'], text=True)
        print(result.split())
        date_text = result.split()[2]
        hour_text = result.split()[3]
        hour = int(hour_text.split(':')[0])
        minute = int(hour_text.split(':')[1])
        boot_date = datetime.fromisoformat(date_text)
        boot_date = boot_date.replace(hour=hour, minute=minute)
        boot_date = str(boot_date)
        date = datetime.now().timestamp()
        _id = self.config.get('data','id')
        localizacao = self.config.get('data','localizacao')
               
        log = {'id':_id,
                'property':'Log',
                'location':localizacao,
                'date':date,
                'info':boot_date
                #'signature': assinatura               
                }
        self.sign()
        
    def bluetooth_log_connection(self, is_valid, addr):
        
        date = datetime.now().timestamp()
        _id = self.config.get('data','id')
        localizacao = self.config.get('data','localizacao')
        
        log = {'id':_id,
                'device':addr,
                'property':'Bluetooth',
                'location':localizacao,
                'date':date,
                }
        
        if is_valid == "valid":
            log['info'] = 'Validation Authenticated'
                        
        else:
            log['info'] = 'Validation Failed'        

        self.sign()
                
    def bluetooth_log_calibre(self):
        
        date = datetime.now().timestamp()
        _id = self.config.get('data','id')
        localizacao = self.config.get('data','localizacao')
               
        log = {'id':_id,
                'property':'Calibration',
                'location':localizacao,
                'date':date,
                'signal':''
                #'signature': assinatura               
                }
        self.sign()
    
    def sign(self):
    
        assinatura = self.signature.sign(log)
        assinatura = str(assinatura)
        log['signature'] = assinatura
        self.register(log)
        print(log)
    
    def register(self, log):
        
        log_json = json.dumps(log)
        caminho_do_arquivo = "registro/" + log["property"] + "/" + str(log["date"]) + ".json"
        with open(caminho_do_arquivo, "a+") as f:
            f.write(log_json)
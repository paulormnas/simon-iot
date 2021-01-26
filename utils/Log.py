import subprocess
import json

from datetime import datetime
from peripherals import Sensor
from security import Signature

class log():
    def __init__(self)
        self.signature = Signature()
        self.register = Sensor()
        
    def boot_log(self):    
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

        dados = {'id':'id',
                'property':'Log',
                'date': date,
                'info':boot_date
                #'signature': assinatura                
                }
        
        assinatura = self.signature.sign(dados)
        dados["signature"] = assinatura
        
        self.register.registrar_dados(dados)
        
        
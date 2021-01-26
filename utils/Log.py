import subprocess
import json
from datetime import datetime

class log():    
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

        dados_json = json.dumps(dados)
        caminho_do_arquivo = "registro/" + dados["property"] + "/" + str(dados["date"]) + ".json"
        with open(caminho_do_arquivo, "a+") as f:
            f.write(dados_json)
                    
        print(dados)

# -*- coding: UTF-8 -*-
import requests
import json
from security.Sign import Signature

signature = Signature()
device_id = 'SiMon-standard'

### Dados a serem assinados ###

dados = {"id": "dispositivo_001",
        "location": [-22.597412, -43.289396],
        "property": "TEMPERATURA",
        "date": 1604520278.332991,
        "value": 22.3}

### Conversão para a extensão json ###
dados_json = json.dumps(dados)

### Assinatura dos dados ###
#assinatura = signature.sign(dados_json)

### Assinatura dos dados via http ###
assinatura = requests.post('http://192.168.1.6:8080/sign', dados_json)


### Verificação da assinatura ###
#verificacao_dispositivo = signature.verify_signature(dados_json, device_id, assinatura)
verificacao_dispositivo = requests.get('http://192.168.1.6:8080//verifica_dispositivo?device_id={}&data={}'.format(device_id, dados_json),data=assinatura)


print(assinatura)

print(verificacao_dispositivo)

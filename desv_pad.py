# Implementando o cálculo do desvio padrão no código do registro.

import json
import time
import random
import numpy
#from leitura import DHT22

def registrar_dados(dados):
    dados_json = json.dumps(dados)
    caminho_do_arquivo = "registro/" + dados["property"] + "/" + str(dados["date"]) + ".json"

    with open(caminho_do_arquivo, "a+") as f:
        f.write(dados_json)

def gerar_dados(propriedade, valor):
    id = "dispositivo_001"
    localizacao = ["-22.597412, -43.289396"]
    data = time.time()

    dados = {'id': id,
         'location': localizacao,
         'property': propriedade,
         'date': data,
         'value': valor
            }
    registrar_dados(dados)
    #print(registrar_dados(dados))

contador = 0

while(contador < 10):
    umidade = random.randint(20,80)
    temperatura = random.randint(15,40)
    gerar_dados("UMIDADE", umidade)
    gerar_dados("TEMPERATURA", temperatura)
    print('{0},{1},{2:0.1f}*C,{3:0.1f}%rn'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperatura, umidade))

    contador = contador + 1

else:
    print("Falha ao receber os dados do sensor.")
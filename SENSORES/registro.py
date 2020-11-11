import json
import time
import numpy as np
from leitura import DHT22
from Fila import Fila

dht = DHT22(pino=4)
TOTAL_DE_LEITURAS = 10

### Funções para registro dos dados em um arquivo e manuseio dos dados ###

def registrar_dados(dados):
    """
    Converte dicionario com informaçoes de mediçao em formato JSON e registra em um arquivo com extensão .json.

        :dados - dict
        :return - None

    """
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
    
def verificar_desv_pad (leituras):
    """
    Verifica o desvio padrao de um conjunto de leituras em lista.
    
    :leituras - list
    :return - boolean
    
    """
    
    desv_pad = np.std(leituras)
    #print("Desvio Padrão: {:.4f}".format(desv_pad))
    
    if (desv_pad < 10):
        return True
    else:
        return False
        
### Script para leitura dos dados

fila_umidade = Fila(tamanho = TOTAL_DE_LEITURAS)
fila_temperatura = Fila(tamanho = TOTAL_DE_LEITURAS)

tamanho_temperatura = 0
tamanho_umidade = 0

#while (tamanho_temperatura < TOTAL_DE_LEITURAS and tamanho_umidade < TOTAL_DE_LEITURAS):
while (True):
    umidade, temperatura = dht.ler_dados()
    if umidade is not None and temperatura is not None:
        print('{0},{1},{2:0.1f}*C,{3:0.1f}%rn'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperatura, umidade))
        
        lista_temporaria = []
        lista_temporaria.extend(fila_umidade.ler_itens())
        lista_temporaria.append(umidade)
        if verificar_desv_pad(lista_temporaria):
            fila_umidade.adicionar_item(umidade)
            gerar_dados("UMIDADE", umidade)


        lista_temporaria = []
        lista_temporaria.extend(fila_temperatura.ler_itens())
        lista_temporaria.append(temperatura)
        if verificar_desv_pad(lista_temporaria):
            fila_temperatura.adicionar_item(temperatura)
            gerar_dados("TEMPERATURA", temperatura)

    else:
        print("Falha ao receber os dados do sensor.")

    tamanho_temperatura = len(fila_temperatura.ler_itens())
    tamanho_umidade = len(fila_umidade.ler_itens())


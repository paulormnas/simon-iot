# coding: utf-8

leitura = [1,2,3,4,5,6,7,8,9,10]

# dados = {
#       "id": "id do dispositivo",
#       "modelo": "modelo do dispositivo",
#       "data_e_hora": "O que achar melhor"
#     }


def main():
  print("Desvio padrao das leituras: ", desvpad(leitura))


def media(lista):
    soma = 0
    n = len(lista)
    for i in lista:
        soma += i
    ma = (soma/n)
    return ma


def var(lista):
    med = media(lista)
    soma = 0
    for i in lista:
        soma = soma + (i-med)**2
    return soma


def desvpad(lista):
    n = len(lista)
    somaquad = var(lista)
    variancia = (somaquad/n-1)
    desvpadA = (variancia)**(1/2)
    return desvpadA

# #  return dsev_pad
#   pass
#
# def assinarRSA(dados_pra_assinar):
#   ''' Esta função faz a assinatura dos dados utilizando o algoritmo RSA. '''
#
# #  return assinatura
#   pass
#


if __name__ == "__main__":
  main()

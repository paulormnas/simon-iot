#Testando listas e o cálculo do desvio padrão delas
import numpy

lista_umidade = []
lista_temperatura = []

lista_umidade.extend([40,40,40,40])
lista_temperatura.extend([20,20,20,20])

desv_pad_umidade = float(numpy.std(lista_umidade, ddof = 1))
desv_pad_temperatura = float(numpy.std(lista_temperatura, ddof = 1))

print(desv_pad_umidade)
print(desv_pad_temperatura)

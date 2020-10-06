#Cálculo do desvio padrão
import numpy

unit_of_measurement = input("Enter the unit of measurement of the data: ")
data = [1, 1, 1, 1]

standard_deviation = float(numpy.std(data, ddof = 1))

print("The sample standard deviation is: %.2f " % standard_deviation,unit_of_measurement)
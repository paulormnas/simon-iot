# -*- coding: utf-8 -*-

class Fila():
    def __init__(self, tamanho=10):
        self.lista = []
        self.tamanho_da_fila = tamanho

    def adicionar_item(self, item):
        if len(self.lista) < self.tamanho_da_fila:
            self.lista.append(item)
        else:
            self.lista = self.lista[1:]
            self.lista.append(item)

    def ler_itens(self):
        return self.lista

    def remove_itens(self):
        pass
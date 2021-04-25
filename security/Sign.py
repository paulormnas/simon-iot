# -*- coding: utf-8 -*-
from utils.Config import ConfigSecurity
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class Signature(object):
    def __init__(self):
        self.config = ConfigSecurity()
        
    def sign(self, dados):
        convert = str(dados)   #Converte o dicionario em uma string para poder ser em seguida convertido em bytes.
        byte_mensage = convert.encode()   #Converte a string em bytes para poder gerar o Hash.
        h = SHA256.new(byte_mensage)   #Gera o Hash da mensagem
        print(h.hexdigest())
        key_path = self.config.private_key_path
        key = RSA.import_key(open(key_path).read())
        assinatura = pkcs1_15.new(key).sign(h)
        print(assinatura)
        return assinatura

    def generate_key_pair(self):
        """
        Gera chaves criptograficas publica e privada, utilizando o algoritmo RSA, com tamanho fixo de 2048,
        escreve em arquivos e retorna as informaçoes.

        :return: um dicionario com chaves publica e privada e informaçoes das chaves para armazenamento em banco de dados
        """
        key_size = 2048
        priv_key = RSA.generate(key_size)
        priv_key_pem = priv_key.export_key('PEM')
        self.write_key_to_pem_file(file_name='private_key', key_stream=priv_key_pem)

        pub_key = priv_key.publickey()
        pub_key_pem = pub_key.export_key('PEM')
        self.write_key_to_pem_file(file_name='public_key', key_stream=pub_key_pem)

    def write_key_to_pem_file(self, file_name, key_stream):
        file_path = f'../generated_keys/{file_name}.pem'
        with open(file_path, 'wb') as f:
            f.write(key_stream)

    def verify_signature(self, dados, signature):
        copia = dados   #Copia o dicionario original para fazer as operacoes de comparacao sem alterar o original
        convert = str(copia)   #Converte o dicionario copiado em uma string para poder ser em seguida convertido em bytes.
        byte_mensage = convert.encode()   #Converte a string em bytes para poder gerar o Hash.
        h = SHA256.new(byte_mensage)   #Gera o Hash da mesagem
        key_path = self.config.public_key_path
        key = RSA.import_key(open(key_path).read())  # Le a informaçao da chave publica
        try:
            pkcs1_15.new(key).verify(h, signature)  # Verifica assinatura a partir do Hash e da chave informados
        except ValueError:
            print("Assinatura invalida")  # Caso ocorra uma exceçao, a assinatura nao e valida
            return False
        else:
            print("A assinatura e valida")
            return True


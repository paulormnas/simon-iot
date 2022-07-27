# -*- coding: utf-8 -*-
from utils.Config import ConfigSecurity
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class Signature(object):
    def __init__(self):
        self.config = ConfigSecurity()

    def sign(self, dados):
        h = SHA256.new(dados)
        key_path = self.config.private_key_path
        key = RSA.import_key(open(key_path).read())
        assinatura = pkcs1_15.new(key).sign(h)
        return assinatura

    def generate_key_pair(self):
        """
        Gera chaves criptograficas publica e privada, utilizando o algoritmo RSA, com tamanho fixo de 2048, e escreve em arquivos.
        """
        key_size = 2048
        priv_key = RSA.generate(key_size)
        priv_key_pem = priv_key.export_key("PEM")
        self.write_key_to_pem_file(file_name="private_key", key_stream=priv_key_pem)

        pub_key = priv_key.publickey()
        pub_key_pem = pub_key.export_key("PEM")
        self.write_key_to_pem_file(file_name="public_key", key_stream=pub_key_pem)

    def write_key_to_pem_file(self, file_name, key_stream):
        file_path = f"../generated_keys/{file_name}.pem"
        with open(file_path, "wb") as f:
            f.write(key_stream)

    def verify_signature(self, dados, signature):
        copy = dados
        convert = str(copy)
        byte_message = convert.encode()
        h = SHA256.new(byte_message)
        key_path = self.config.public_key_path
        key = RSA.import_key(open(key_path).read())
        try:
            pkcs1_15.new(key).verify(h, signature)
        except ValueError:
            print("invalid")  # Caso ocorra uma exceçao, a assinatura nao e valida
            return False
        else:
            print("valid")
            return True

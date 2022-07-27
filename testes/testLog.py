import os
import json

from unittest import TestCase
from utils.Log import LogManager


class TestSign(TestCase):
    def setUp(self):
        self.log = LogManager()
        self.register_path = "../registros/Log"
        self.test_device_addr = "70:6B:9F:2D:5B:0F"

    def test_boot_log(self):
        lista_de_arquivos = os.listdir(path=self.register_path)
        quantidade_inicial_de_arquivos = len(lista_de_arquivos)
        self.log.generate_boot_log()
        lista_de_arquivos = os.listdir(path=self.register_path)
        quantidade_final_de_arquivos = len(lista_de_arquivos)
        self.assertGreater(quantidade_final_de_arquivos, quantidade_inicial_de_arquivos)

    def test_log_new_valid_bluetooth_connection(self):
        arquivos_iniciais = set(os.listdir(path=self.register_path))
        self.log.generate_bluetooth_new_connection_log(
            is_valid="valid", addr=self.test_device_addr
        )
        arquivos_finais = set(os.listdir(path=self.register_path))
        arquivo_mais_recente = (arquivos_finais - arquivos_iniciais).pop()
        caminho_do_arquivo = f"{self.register_path}/{arquivo_mais_recente}"
        print(caminho_do_arquivo)
        with open(caminho_do_arquivo, "r") as f:
            dados = json.loads(f.read())
            if "info" in dados:
                self.assertEqual("Device Authenticated", dados["info"])

    def test_log_new_invalid_bluetooth_connection(self):
        arquivos_iniciais = set(os.listdir(path=self.register_path))
        self.log.generate_bluetooth_new_connection_log(
            is_valid="invalid", addr=self.test_device_addr
        )
        arquivos_finais = set(os.listdir(path=self.register_path))
        arquivo_mais_recente = (arquivos_finais - arquivos_iniciais).pop()
        caminho_do_arquivo = f"{self.register_path}/{arquivo_mais_recente}"
        print(caminho_do_arquivo)
        with open(caminho_do_arquivo, "r") as f:
            dados = json.loads(f.read())
            if "info" in dados:
                self.assertEqual("Authentication Failed", dados["info"])

    def test_new_start_calibration_log(self):
        arquivos_iniciais = set(os.listdir(path=self.register_path))
        self.log.generate_calibration_start_log()
        arquivos_finais = set(os.listdir(path=self.register_path))
        arquivo_mais_recente = (arquivos_finais - arquivos_iniciais).pop()
        caminho_do_arquivo = f"{self.register_path}/{arquivo_mais_recente}"
        print(caminho_do_arquivo)
        with open(caminho_do_arquivo, "r") as f:
            dados = json.loads(f.read())
            if "property" in dados:
                self.assertEqual("calibration_started", dados["property"])

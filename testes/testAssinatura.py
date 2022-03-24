import os

from utils.Config import ConfigSecurity
from unittest import TestCase
from security.Sign import Signature


class TestSign(TestCase):
    def setUp(self):
        self.signature = Signature()
        self.config = ConfigSecurity()
        self.dados_de_teste = {
            "id": "dispositivo_001",
            "location": [-22.597412, -43.289396],
            "property": "TEMPERATURA",
            "date": 1604520278.332991,
            "value": 22.3,
        }

    def test_gerar_par_de_chaves(self):
        self.signature.generate_key_pair()
        lista_de_arquivos = os.listdir(path="../generated_keys")
        contador_cahves = 0
        for item in lista_de_arquivos:
            if "pem" in item:
                contador_cahves += 1
        self.assertLessEqual(2, contador_cahves)

    def test_verifica_assinatura_valida(self):
        assinatura = self.signature.sign(self.dados_de_teste)
        self.assertTrue(
            self.signature.verify_signature(self.dados_de_teste, assinatura)
        )

    def test_verifica_assinatura_invalida(self):
        with open("assinatura_invalida.txt", "rb") as f:
            assinatura = f.read()
            self.assertFalse(
                self.signature.verify_signature(self.dados_de_teste, assinatura)
            )

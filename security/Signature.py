from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

class Signature():
    
    def sign(self, dados):
        convert = str(dados)   #Converte o dicionario em uma string para poder ser em seguida convertido em bytes.
        bite_mensage = convert.encode()   #Converte a string em bytes para poder gerar o Hash.
        h = SHA256.new(bite_mensage)   #Gera o Hash da mesagem
        print (h.hexdigest())
        key = RSA.import_key(open('private.pem').read())
        assinatura = pkcs1_15.new(key).sign(h)
        print(assinatura)
        return assinatura
    
    def verify_signature(self, dados):
        
        copia = dados   #Copia o dicionario original para fazer as operacoes de comparacao sem alterar o original
        original = dados.get("signature")   #Armazena o valor do campo signature para ser usada na comparacao de chaves
        key = RSA.import_key(open('public.pem').read())
        copia.pop("signature")   #Remove o campo de assinatura da copia para poder gerar um novo hash para comparacao
        convert = str(copia)   #Converte o dicionario copiado em uma string para poder ser em seguida convertido em bytes.
        bite_mensage = convert.encode()   #Converte a string em bytes para poder gerar o Hash.
        h = SHA256.new(bite_mensage)   #Gera o Hash da mesagem
        key = RSA.import_key(open('private.pem').read())
        assinatura = pkcs1_15.new(key).sign(h)
        assinatura = str(assinatura)
        if (assinatura == original):
            print ("A assinatura e valida")
            return True
        else:
            print ("Assinatura invalida")
            return False
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

def sign(dados):
    convert = str(dados)   #Converte o dicionario em uma string para poder ser em seguida convertido em bites.
    bite_mensage = convert.encode()   #Converte a string em bites para poder gerar o Hash.
    h = SHA256.new(bite_mensage)   #Gera o Hash da mesagem
    print (h.hexdigest())
    key = RSA.import_key(open('private.pem').read())
    assinatura = pkcs1_15.new(key).sign(h)
    print(assinatura)
    return assinatura

dados = {'id': id,
         'location': "localizacao",
         'property': "propriedade",
         'date': "data",
         'value': "valor"
         }

assinatura = sign(dados)

#Append signature
dados["signature"] = assinatura
print(dados)

##Verify Signature
#key = RSA.import_key(open('public.pem').read())
#try:
#    pkcs1_15.new(key).verify(h, assinatura)
#    print ("A assinatura e valida")
#except (ValueError, TypeError):
#    print ("Assinatura invalida")
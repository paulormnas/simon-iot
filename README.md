# Exercicio Python
Repositório para projeto de IoT desenvolvido utilizando um Raspberry Pi 3B+ conectado aos sensores de temperatura e umidade (DHT22) e sensore de movimento (PIR).

O código foi desenvolvido utilizando a versao 3.9 do Python e pode ser adaptado para receber novos sensores. O software foi desenvolvido de maneira a registrar logs de inicializaçao do dispositivo e as mediçoes de cada sensor em arquivos com estrutura JSON.

## Configuraçao Inicial

Inicialmente e necessario ter o Python 3.9 instalado no computador par que possa ser criado o ambiente virtual atraves do virtualenv. Em seguida sao criados diretorios necessarios para o armazenamento dos registros gerados pelo software. Para configurar o projeto em ambiente Linux utilize os seguintes comandos:

```bash
git clone https://github.com/paulormnas/exercicio-python.git
cd exercicio-python
pip install virtualenv
virtualenv -p python3.9 venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p registros/Log
touch config.ini
```

Para usuários do Windows recomenda-se utilizar o terminal do [Git para Windows](https://git-scm.com/download/win) que permite executar grande parte dos comandos do ambiente Linux. Com as devidas correções, o ambiente será preparado com os seguintes comandos: 

```bash
git clone https://github.com/paulormnas/exercicio-python.git
cd exercicio-python
pip install virtualenv
virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt
mkdir -p registros/Log
touch config.ini
```
Um arquivo de configuraçao ```config.ini``` tambem devera ser criado com informaçoes sobre o servidor ao qual o dispositvio precisara se conectar, identificaçao do dispositivos, localizaçao das chaves criptograficas e configuraçoes dos sensores conectados ao raspberry. A seguir esta um exemplo de arquivo de confiuraçao:

```txt
[signature]

public_key = /path/to/public.pem
private_key = /path/to/private.pem

[data]

id = dispositivo_001
localizacao = [-22.597412,-43.289396]

[server]

url = 192.168.1.8
porta = 8080

[DHT]

pino = 4
leituras = 10
intervalo = 300

[PIR]

pino = 11
intervalo = 60
```
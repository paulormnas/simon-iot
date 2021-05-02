# SiMon IoT
Repositório para projeto de IoT, do Sistema de Monitoramento (SiMon) do Inmetro, desenvolvido utilizando um Raspberry Pi 3B+ conectado aos sensores de temperatura e umidade (DHT22) e sensore de movimento (PIR).

O código foi desenvolvido utilizando a versão 3.9 do Python e pode ser adaptado para receber novos sensores. O software foi desenvolvido de maneira a registrar logs de inicialização do dispositivo e as medições de cada sensor em arquivos com estrutura JSON.

## Configuração Inicial

Inicialmente e necessario ter o Python 3.9 instalado no computador par que possa ser criado o ambiente virtual atraves do virtualenv. Em seguida são criados diretórios necessarios para o armazenamento dos registros gerados pelo software. Para configurar o projeto em ambiente Linux utilize os seguintes comandos:

```bash
git clone https://github.com/paulormnas/exercicio-python.git
cd exercicio-python
pip install virtualenv
virtualenv -p python3.9 venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p registros/Log
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
```
Um arquivo de configuração ```config.ini``` tambem deverá ser criado com informações sobre o servidor ao qual o dispositvio precisara se conectar, identificação do dispositivos, localização das chaves criptográficas e configurações dos sensores conectados ao raspberry. Este arquivo deverá se encontrar em um diretorio configurado de acordo com o modo de excução do software (test, development, production, etc). O software identifica o modo de operação a partir da variável de ambiente ```SIMON_IOT_MODE```. Por exemplo, para configurar o software para executar em modo teste configure ```SIMON_IOT_MODE=test```. Desta forma o software buscará pelo arquivo config.ini no diretório ```instance_test```. Caso essa variável não esteja configurada o software buscará automaticamente o config.ini no diretório ```instance_development```. A seguir estão os comandos para criar o diretorio e o arquivo a partir do terminal, utilizando o editor nano.

```bash
mkdir instance_development
nano instance_development/config.ini
```

Este é um exemplo de arquivo de configuração:
```txt
[security]
public_key = ../instance_test/public_key.pem
private_key = ../instance_test/private_key.pem

[device]
id = dispositivo_test_001
location = [-22.597412,-43.289396]
type = meter

[server]
url = 192.168.0.5
port = 8080

[DHT]
pin = 4
number_of_readings = 10
interval = 300

[PIR]
pin = 11
interval = 60
```

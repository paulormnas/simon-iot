# IoT com Raspberry Pi
Repositório para software do dispositivo de IoT para medição e controle de ambientes laboratoriais. O dispositivo é constituído de um Raspberry Pi 3 B+ e sensores como DHT22, PIR e MQ2.

Este projeto é desenvolvido utilizando Python a partir da versão 3.8. Caso o interpretador instalado em sua máquina esteja abaixo da versão 3.8 será necessário atualizar o interpretador do Python.

Para iniciar o projeto e necessário configurar o ambiente virtual do Python com as dependências do projeto e criar a pasta onde serão armazenados os registros de medições dos sensores:

```bash
git clone https://github.com/paulormnas/exercicio-python.git
cd exercicio-python
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
mkdir registros
```

Caso exista mais de um interpetrador Python 3 instalado na máquina será necessário especificar a versão desejada no momento da configuração do ambiente virtual, por exemplo, `virtualenv -p python3.9 venv`.

Após a configuração inicial do ambiente será necessário adicionar ao projeto um arquivo de configuração com informações sobre o dispositivo de IoT e sobre o servidor que receberá os dados do dispositivo:

```json
{
  "id": "id://identificacao/unica/do/dispositivo_001",
  "location": ["lat, lon"],
  "server_ip": "X.X.X.X",
  "server_port": "8080",
  "device_private_key": "/opt/keys/private.pem",
  "device_public_key": "/opt/keys/public.pem"
}
```

Para executar o programa utilize `python main.py` com o ambiente virtual habilitado.
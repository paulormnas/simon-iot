#!/bin/bash
SIMON_IOT_MODE="production"

# A variavel DIRETORIO foi criada para adequar o caminho onde o arquivo se encontra armazenado no sistema.
DIRETORIO="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir -p $DIRETORIO/registros/Log
mkdir -p $DIRETORIO/registros/UMIDADE
mkdir -p $DIRETORIO/registros/TEMPERATURA
mkdir $DIRETORIO/instance_$SIMON_IOT_MODE

pip3 install -r requirements.txt
export SIMON_IOT_MODE=$SIMON_IOT_MODE

sudo -E python3 $DIRETORIO/main.py

#Seguindo as instruções conforme o link: https://www.filipeflop.com/blog/inicializacao-durante-o-boot-com-systemd-na-raspberry-pi/

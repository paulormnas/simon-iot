#!/bin/bash

# A variavel DIRETORIO foi criada para adequar o caminho onde o arquivo se encontra armazenado no sistema.
DIRETORIO="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 $DIRETORIO/main.py

#Seguindo as instruções conforme o link: https://www.filipeflop.com/blog/inicializacao-durante-o-boot-com-systemd-na-raspberry-pi/

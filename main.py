#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# cliente.py

import os, socket, time, sys
import struct, re

from datetime import datetime
from threading import Thread

# Confere argumentos:
if len(sys.argv) != 2:
    print "Uso:\n"+sys.argv[0]+" <arquivo de configuracao>"
    exit(1)

# Abre arquivo com os hosts:
hostFP = open(sys.argv[1],'r')

# Log - Cliente & Servidor
logFP = open('log.txt', 'a')

# Colocando os dados do arquivo texto em uma lista:
l_host_port = [ i.strip() for i in hostFP.readlines() ]

# Fechando arquivo e eliminando da memoria, pois nao sera mais usado.
hostFP.close()
del hostFP

# Criando lista de hosts
l_hosts = [ i.split()[0] for i in l_host_port ]

# Criando lista de portas
l_ports = [ i.split()[1] for i in l_host_port ]

# Criando a tupla que acredito que simplificara nossas vidas:
# l_t_ -> lista de tuplas
l_t_HOST_PORT = [ ( i.split()[0], i.split()[1] ) for i in hostFP.readlines() ]


# OBS: cada servidor tem q fazer o log no mesmo arquivo.

# Identificando maquina local: (gethostname retorna uma string)
ME = socket.gethostname()

# Se for um dos hosts da lista, entao roda o servidor, caso contrario, roda em
# modo cliente com interface para usuario humano.
if ME in l_hosts:

    # Encontrando a porta desta maquina
    MINHA_PORTA = l_ports[l_hosts.index(ME)]

    # Iniciando o servidor
    import servidor
    servidor = Servidor(ME,MINHA_PORTA,l_hosts,l_ports,logFP)
    servidor.start()

else:
    # Inicia o cliente:
    import cliente
    cliente = Cliente(ME,l_hosts,l_ports,logFP)
    cliente.start()

# Fechando arquivo
logFP.close()


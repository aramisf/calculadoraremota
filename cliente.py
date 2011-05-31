#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# cliente.py

import os, socket, time, sys
import struct, re

from datetime import datetime
from threading import Thread

class Cliente(object):

    def __init__(self,ME,l_hosts,l_ports,logFP):

        self.HOST = l_host[0]
        self.PORT = l_ports[0]


    def log(self,msg,data):

        ''' diferentes niveis de log:
            1 - inicio
            2 - recebimento de mensagem
            3 - envio de mensagem
        '''
        if msg == 1:
            # Inicia o log com a marcacao de tempo
            logFP.write("%s iniciando, hora local:"+datetime.now().ctime()+"\n" % ME)

        elif msg == 2:
            # Recebimento de dados:
            logFP.write("%s(cliente) enviando %s, hora local:"+datetime.now().ctime()+"\n" % (ME,str(data)) )

        elif msg == 3:
            # Envio de dados:
            logFP.write("%s(cliente) recebendo %s, hora local:"+datetime.now().ctime()+"\n" % (ME,str(data)) )

        else:


    def start(self):

        self.log(1)

        # Abrindo um socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

        while True:

            # Recebendo dados do usuario:
            data = raw_input("Digite a expressao matematica: ")

            # Enviando dados e armazenando no log:
            self.sock.send(data)
            self.log(3,data)

            # Recebendo dados do servidor e atualizando o log
            # TIMEOUT AQUI
            data = self.sock.recv(1024)
            self.log(2,data)



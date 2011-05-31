#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# cliente.py

import socket, time
from datetime import datetime

class Cliente(object):

    def __init__(self,ME,l_hosts,l_ports,logFP):

        self.HOST = l_hosts[0]
        self.PORT = int(l_ports[0])
        self.logFile = logFP
        self.ME = ME


    def log(self,msg,data=None):

        ''' diferentes niveis de log:
            1 - inicio
            2 - recebimento de mensagem
            3 - envio de mensagem
        '''
        text1 = self.ME+"(em modo cliente) iniciando em: "+datetime.now().ctime()+"\n"
        text2 = self.ME+"(cliente) enviando "+str(data)+" em: "+datetime.now().ctime()+"\n"
        if msg == 1:
            # Inicia o log com a marcacao de tempo
            self.logFile.write(text1)

        elif msg == 2:
            # Recebimento de dados:
            self.logFile.write(text2)

        elif msg == 3:
            # Envio de dados:
            self.logFile.write(text2)

        #else:
        #    pass


    def start(self):

        self.log(1)

        # Abrindo um socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Criando conexao:
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



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, socket, time, sys
import struct, re

from datetime import datetime
from threading import Thread

class Servidor(object)


    def __init__(self,ME,MINHA_PORTA,l_hosts,l_ports,logFP):

        self.ME = ME
        self.HOST = ME
        self.PORT = MINHA_PORTA
        self.INDICE = l_hosts.index(ME)
        self.MAX_HOSTS = len(l_hosts)

        if self.INDICE == 0:
            self.caso_1()

        elif self.INDICE == (self.MAX_HOSTS - 1):
            self.caso_3()

        else:
            self.caso_2()


    def log(self,msg,data):

        ''' diferentes niveis de log:
            1 - inicio
            2 - recebimento de mensagem
            3 - envio de mensagem
        '''
        if msg == 1:
            # Inicia o log com a marcacao de tempo
            clientFP.write("%s iniciando, hora local:"+datetime.now().ctime()+"\n" % ME)

        elif msg == 2:
            # Recebimento de dados:
            clientFP.write("%s(cliente) enviando %s, hora local:"+datetime.now().ctime()+"\n" % (ME,str(data)) )

        elif msg == 3:
            # Envio de dados:
            clientFP.write("%s(cliente) recebendo %s, hora local:"+datetime.now().ctime()+"\n" % (ME,str(data)) )

        else:


    def fala(self,DATA):


        while True:

            # Enviando dados e armazenando no log:
            self.sock.send(DATA)
            self.log(3,DATA)

            # Recebendo confirmacao de recebimento pelo servidor e atualizando o
            # log
            data = s.recv(1024)
            self.log(2,DATA)


    def escuta(self,DATA):

        self.sock_escuta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_escuta.bind((HOST, PORT))
        self.sock_escuta.listen(3)
        conn, addr = s.accept()


    def start(self):

        self.log(1)

        # Abrindo um socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

        while True:



    def caso_1(self):

        HOST = ''
        PORT = self.l_ports[0]

        # Conecta com o cliente:
        self.sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_cliente.bind((HOST, PORT))
        self.sock_cliente.listen(3)
        self.clientConn = self.sock_cliente.accept()

        # Conecta com o Servidor:
        MEU_SERVIDOR = self.l_hosts[self.l_hosts.index(self.ME)+1]
        PORTA_DELE = self.l_ports[self.l_hosts.index(self.ME)+1]

        self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_servidor.connect((MEU_SERVIDOR, PORTA_DELE))


    def caso_2(self):

        # Informacoes para conectar com o cliente:
        MEU_CLIENTE = self.l_hosts[self.l_hosts.index(self.ME)-1]
        PORTA_ESCUTA = self.l_ports[self.l_hosts.index(self.ME)]

        # Informacoes para conectar com o servidor
        MEU_SERVIDOR = self.l_hosts[self.l_hosts.index(self.ME)+1]
        PORTA_FALA = self.l_ports[self.l_hosts.index(self.ME)+1]

        # Conecta com o cliente:
        self.sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_cliente.bind((MEU_CLIENTE, PORTA_ESCUTA))
        self.sock_cliente.listen(3)
        self.clientConn = self.sock_cliente.accept()

        # Conecta com o Servidor:
        MEU_SERVIDOR = self.l_hosts[self.l_hosts.index(self.ME)+1]
        PORTA_DELE = self.l_ports[self.l_hosts.index(self.ME)+1]

        self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_servidor.connect((MEU_SERVIDOR, PORTA_FALA))


    def caso_3(self):

        HOST = self.l_hosts[-2]
        PORT = self.l_ports[-1]

        # Conecta com o cliente:
        self.sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_cliente.bind((HOST, PORT))
        self.sock_cliente.listen(3)
        self.clientConn = self.sock_cliente.accept()

        while 1:
            # Recebe os dados;
            DATA = self.clientConn.recv(1024)
            if not DATA: break
            self.log(2,DATA)

            # Faz o calculo:
            DATA = eval(DATA)

            # Devolve o resultado
            self.clientConn.send(DATA)
            self.log(3,DATA)



###########################################
# Log - Client File Pointer
servFP = open('servidor.log', 'w')

# Inicia o log com a marcacao de tempo
servFP.write("Servidor, hora local: "+datetime.now().ctime()+"\n")

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    print "Recebi: %s" % str(data)
    data = "Ok\n"
    conn.send(data)
conn.close()
#-*- encoding: utf-8 -*-


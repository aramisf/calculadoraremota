#!/usr/bin/env python
# -*- coding: utf-8 -*-

# servidor.py

import socket, time
from datetime import datetime

class Servidor(object):

    def __init__(self,ME,MINHA_PORTA,l_hosts,l_ports,logFP):

        self.ME = ME
        #self.HOST = ME
        self.DATA = ''
        self.PORT = MINHA_PORTA
        self.INDICE = l_hosts.index(self.ME)
        self.MAX_HOSTS = len(l_hosts)
        self.logFile = logFP
        self.l_hosts = l_hosts
        self.l_ports = l_ports


    def log(self,msg):

        ''' diferentes niveis de log:
            1 - inicio
            2 - recebimento de mensagem
            3 - envio de mensagem
        '''
        text1 = "Iniciando "+self.ME+" em modo servidor, hora local:"+datetime.now().ctime()+"\n"
        text2 = self.ME+" diz: Enviando "+str(self.DATA)+", hora local:"+datetime.now().ctime()+"\n"
        text3 = self.ME+" diz: Recebendo "+str(self.DATA)+", hora local:"+datetime.now().ctime()+"\n"
        if msg == 1:
            # Inicia o log com a marcacao de tempo:
            self.logFile.write(text1)

        elif msg == 2:
            # Recebimento de dados:
            self.logFile.write(text2)

        elif msg == 3:
            # Envio de dados:
            self.logFile.write(text3)


    def fala(self,para_onde): # para_onde eh um socket

        # Enviando dados e armazenando no log:
        para_onde.send(self.DATA)
        self.log(3)


    def escuta(self, de_onde): # de_onde eh um socket

        # Recebe os dados.
        self.DATA = de_onde.recv(1024)

        # Esse if pode tirar, pq nao ta dentro de loop nenhum:
        #if not self.DATA: break
        self.log(2)

        #self.sock_escuta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock_escuta.bind((HOST, PORT))
        #self.sock_escuta.listen(3)
        #conn, addr = s.accept()


    def start(self):

        self.log(1)

        # Abrindo um socket ### Tira isso daqui, abre as conexoes apenas com os
        # caras certos, depois de ter identificado qual o tipo do servidor.
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect((self.HOST, self.PORT))

        if self.INDICE == 0:
            self.conecta_caso_1()

        elif self.INDICE == (self.MAX_HOSTS - 1):
            self.conecta_caso_3()

        else:
            self.conecta_caso_2()

        while True:

            # Caso 3 possui uma unica conexao (1 cliente, 0 servidor):
            if self.INDICE == (self.MAX_HOSTS - 1):

                self.escuta(self.clientConn[0])
                self.DATA = str(eval(self.DATA))
                self.fala(self.clientConn[0])

            else:

                self.escuta(self.clientConn[0])
                if not self.DATA: break
                self.fala(self.sock_servidor)
                self.escuta(self.sock_servidor)
                self.fala(self.clientConn[0])


    def conecta_caso_1(self):
        ''' Caso 1 eh quando o servidor eh o 1o da lista, ou seja, ele deve
        esperar uma conexao vinda de uma maquina qualquer, portanto, ele nao
        define um cliente, apenas um servidor ao qual se conectar.
        '''

        # Definindo caracteristicas da conexao do servidor:
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

        print "Meu host %s" % MEU_SERVIDOR
        print "Porta de fala: %d" % PORTA_DELE
        self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_servidor.connect((MEU_SERVIDOR, PORTA_DELE))


    def conecta_caso_2(self):
        ''' Caso 2 eh quando uma maquina nao eh a 1a da lista, mas uma maquina
        entre a segunda e a penultima da lista. Entao sao necessarias duas
        conexoes, uma com o cliente e outra com o servidor da maquina onde o
        programa esta em execucao.
        '''

        # Informacoes para conectar com o cliente:
        MEU_CLIENTE = self.l_hosts[self.l_hosts.index(self.ME)-1]
        PORTA_ESCUTA = self.l_ports[self.l_hosts.index(self.ME)]

        # Informacoes para conectar com o servidor
        MEU_SERVIDOR = self.l_hosts[self.l_hosts.index(self.ME)+1]
        PORTA_FALA = self.l_ports[self.l_hosts.index(self.ME)+1]

        print "Meu cliente %s" % MEU_CLIENTE
        print "Porta de escuta: %d" % PORTA_ESCUTA
        print "Meu host %s" % MEU_SERVIDOR
        print "Porta de fala: %d" % PORTA_FALA
        # Conecta com o cliente:
        self.sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock_cliente.bind((MEU_CLIENTE, PORTA_ESCUTA))
        self.sock_cliente.bind(('', PORTA_ESCUTA))
        self.sock_cliente.listen(3)
        self.clientConn = self.sock_cliente.accept()
        print "ClienConn",self.clientConn[1]

        # Conecta com o Servidor:
        MEU_SERVIDOR = self.l_hosts[self.l_hosts.index(self.ME)+1]
        PORTA_DELE = self.l_ports[self.l_hosts.index(self.ME)+1]

        self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_servidor.connect((MEU_SERVIDOR, PORTA_FALA))


    def conecta_caso_3(self):
        ''' Caso 3 eh quando o servidor eh o ultimo, ele vai apenas ouvir na
        porta dele, efetuar a operacao matematica e devolver o resultado.
        '''

        HOST = self.l_hosts[-2]
        PORT = self.l_ports[-1]

        print "Meu host %s" % HOST
        print "Porta de escuta: %d" % PORT
        # Conecta com o cliente:
        self.sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock_cliente.bind((HOST, PORT))
        self.sock_cliente.bind(('', PORT))
        self.sock_cliente.listen(3)
        self.clientConn = self.sock_cliente.accept()



###########################################
#
#   HOST = ''                 # Symbolic name meaning the local host
#   PORT = 50007              # Arbitrary non-privileged port
#   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   s.bind((HOST, PORT))
#   s.listen(1)
#   conn, addr = s.accept()
#   print 'Connected by', addr
#   while 1:
#       data = conn.recv(1024)
#       if not data: break
#       print "Recebi: %s" % str(data)
#       data = "Ok\n"
#       conn.send(data)
#   conn.close()
#

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
            1 - Inicio da execucao do cliente
            2 - Tentativa de conexao
            3 - Envio de dados
            4 - Recebimento de dados
            5 - Estouro de timeout na conexao
            6 - Estouro de timeout no envio
            7 - Estouro de timeout no recebimento
            8 - Conexao efetuada
            9 - Desligando cliente
        '''
        text1 = "\nIniciando "+self.ME+" em modo cliente: "+datetime.now().ctime()+"\n"
        text2 = self.ME+" tentando conexao com "+self.HOST+": "+datetime.now().ctime()+"\n"
        text3 = self.ME+" diz: recebi "+str(data)+" de "+self.HOST+" em: "+datetime.now().ctime()+"\n"
        text4 = self.ME+" diz: enviei "+str(data)+" para "+self.HOST+" em: "+datetime.now().ctime()+"\n"
        text5 = self.ME+" diz: estouro de timeout ao conectar-se com "+self.HOST+": "+datetime.now().ctime()+"\n"
        text6 = self.ME+" diz: estouro de timeout ao enviar "+str(data)+" para "+self.HOST+": "+datetime.now().ctime()+"\n"
        text7 = self.ME+" diz: estouro de timeout ao enviar "+str(data)+" para "+self.HOST+": "+datetime.now().ctime()+"\n"
        text8 = self.ME+" diz: conectei-me a "+self.HOST+" em: "+datetime.now().ctime()+"\n"
        text9 = self.ME+" diz: desligando em: "+datetime.now().ctime()+" flws \o\n"

        if msg == 1:
            # Inicia o log com a marcacao de tempo
            self.logFile.write(text1)

        elif msg == 2:
            # Recebimento de dados:
            self.logFile.write(text2)

        elif msg == 3:
            # Recebimento de dados:
            self.logFile.write(text3)

        elif msg == 4:
            # Envio de dados:
            self.logFile.write(text4)

        elif msg == 5:
            # Envio de dados:
            self.logFile.write(text5)

        elif msg == 6:
            # Envio de dados:
            self.logFile.write(text6)

        elif msg == 7:
            # Recebimento de dados:
            self.logFile.write(text7)

        elif msg == 8:
            # Recebimento de dados:
            self.logFile.write(text8)

        elif msg == 9:
            # Recebimento de dados:
            self.logFile.write(text9)


    def start(self):

        # Registra o inicio do cliente:
        self.log(1)

        # Abrindo um socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Definindo um timeout para conectar:
        self.sock.settimeout(5.0)

        # Tenta se conectar 3x:
#        for i in range(3):
        try:
            # Criando conexao:
            print "Tentando conectar ao servidor..."
            self.log(2)
            self.sock.connect((self.HOST, self.PORT))
            print "Conectado"
            self.log(8)

        except socket.timeout:
            print "Estouro do timeout"
            self.log(5)

        # Reajustando o timeout, para falar com o servidor:
        self.sock.settimeout(1.5)


        # Conexao feita, eh hora de aguardar a entrada do usuario.
        while True:

            # Recebendo dados do usuario:
            data = raw_input("Digite a expressao matematica: ")


            # Tenta enviar no maximo 5 vezes
            for i in range(5):

                # Trata timeout
                try:
                    # Enviando dados e armazenando no log:
                    self.sock.send(data)
                    print "Enviei %s" % str(data)
                    self.log(4,data)

                except socket.timeout:
                    print "Estouro de timeout no envio"
                    self.log(6,data)

                except:
                    print "Nao conectado, desligando..."
                    self.log(9)
                    exit(1)

            # Recebendo dados do servidor e atualizando o log
            # Tenta receber no maximo 5 vezes
            for i in range(5):

                # Trata timeout
                try:
                    # Enviando dados e armazenando no log:
                    data = self.sock.recv(1024)
                    print "Recebi %s" % str(data)
                    self.log(3,data)

                except socket.timeout:
                    print "Estouro de timeout no recebimento"
                    self.log(7,data)



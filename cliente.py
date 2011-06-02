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
            6 - Conexao efetuada
            7 - Desligando cliente
            8 - Servidor aparenta estar desconectado
        '''
        text1 = "\nIniciando "+self.ME+" em modo cliente: "+datetime.now().ctime()+"\n"
        text2 = self.ME+" tentando conexao com "+self.HOST+": "+datetime.now().ctime()+"\n"
        text3 = self.ME+" diz: recebi "+str(data)+" de "+self.HOST+" em: "+datetime.now().ctime()+"\n"
        text4 = self.ME+" diz: enviei "+str(data)+" para "+self.HOST+" em: "+datetime.now().ctime()+"\n"
        text5 = self.ME+" diz: estouro de timeout ao conectar-se com "+self.HOST+": "+datetime.now().ctime()+"\n"
        text6 = self.ME+" diz: conectei-me a outra ponta em: "+datetime.now().ctime()+"\n"
        text7 = self.ME+" diz: desligando em: "+datetime.now().ctime()+" flws \o\n"
        text8 = self.ME+" diz: servidor aparenta estar desconectado: "+datetime.now().ctime()+"\n"
        text9 = self.ME+" enviando mensagem de teste para o servidor final.\n"

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
            # Envio de dados:
            self.logFile.write(text8)

        elif msg == 9:
            # Envio de dados:
            self.logFile.write(text9)


    def start(self):

        # Registra o inicio do cliente:
        self.log(1)

        # Abrindo um socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Criando conexao:
            print "Tentando conectar ao servidor..."
            self.log(2)
            self.sock.connect((self.HOST, self.PORT))

        except socket.error:
            print "Servidor indisponivel =("
            self.log(8)
            exit(2)

        # Reajustando o timeout, para falar com o servidor:
        self.sock.settimeout(5.)


        # Enviando uma mensagem teste para a outra ponta da conexao, se vier
        # uma resposta, funcionou a conexao.
        data = 'Iae vei? Firmeza?'

        # Tenta enviar a mensagem de teste da outra ponta no maximo 3 vezes
        for i in range(3):

            # Trata timeout
            try:
                # Enviando dados e armazenando no log:
                self.sock.send(data)
                print "Enviei msg teste para a outra ponta"
                self.log(9)

                # Validando a resposta:
            except socket.timeout:
                print "%do estouro de timeout no envio da mensagem teste" % i+1
                self.log(6)

            except socket.error:
                print "Meu servidor caiu 3"
                self.log(8)
                exit(1)

            # Se rolou de enviar, agora recebe os dados e analiza
            try:
                data = self.sock.recv(1024)

            except socket.error:
                print "Conexao perdida"
                self.log(8)
                exit(1)

            if data == 'Opa, eh nois!':
                print "Conexao efetuada com sucesso"
                self.log(6)
                break

            elif data == '':
                print "Meu servidor caiu 2"
                self.log(8)
                exit(1)



        # Conexao feita, eh hora de aguardar a entrada do usuario.
        while True:

            # Recebendo dados do usuario:
            data = raw_input("Digite a expressao aritmetica: ")

            # Enviando dados e armazenando no log:
            try:
                self.sock.send(data)
                self.log(4,data)

            except socket.error:
                print "Meu servidor caiu 4"
                self.log(8)
                exit(1)

            # Recebendo dados do servidor e atualizando o log
#            try:
            data = self.sock.recv(1024)
            print "R: %s" % str(data)
            self.log(3,data)

#            except socket.error:
#                print "Meu servidor caiu 5"
#                self.log(8)
#                exit(1)
# 



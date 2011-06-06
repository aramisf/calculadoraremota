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
           00 - Inicio da execucao do cliente
           01 - Tentativa de conexao
           02 - Envio de dados para conexao com a outra ponta
           03 - Envio de dados
           04 - Recebimento de dados
           05 - Estouro de timeout na conexao
           06 - Conexao efetuada
           07 - Desligando cliente
           08 - Servidor aparenta estar desconectado
           09 - Tentativa de conexao usando IPv6
           10 - Largando IPv6, tentando IPv4
        '''
        textmsg = [ "\nIniciando "+self.ME+" em modo cliente: "+datetime.now().ctime()+"\n",
                    self.ME+" tentando conexao com "+self.HOST+": "+datetime.now().ctime()+"\n",
                    self.ME+" enviando mensagem de teste para o servidor final.\n",
                    self.ME+" diz: enviei "+str(data)+" para "+self.HOST+" em: "+datetime.now().ctime()+"\n",
                    self.ME+" diz: recebi "+str(data)+" de "+self.HOST+" em: "+datetime.now().ctime()+"\n",
                    self.ME+" diz: estouro de timeout ao conectar-se com "+self.HOST+": "+datetime.now().ctime()+"\n",
                    self.ME+" diz: conectei-me a outra ponta em: "+datetime.now().ctime()+"\n",
                    self.ME+" diz: desligando em: "+datetime.now().ctime()+" flws \o\n",
                    self.ME+" diz: servidor aparenta estar desconectado: "+datetime.now().ctime()+"\n",
                    self.ME+" tentando conectar-se usando IPv6: "+datetime.now().ctime()+"\n",
                    self.ME+" diz: nao foi possivel conectar via IPv6, usando IPv4.\n"
                  ]

        self.logFile.write(textmsg[msg])


    def conecta(self):

        # Abrindo um socket IPv6
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        try:
            # Criando conexao:
            print "Tentando conectar ao servidor...(IPv6)"
            self.log(9)
            self.sock.connect((self.HOST, self.PORT))

        except socket.error:
            print "Nao foi possivel conectar usando IPv6"
            self.log(10)

            # Abrindo um socket IPv4
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                # Criando conexao:
                print "Tentando conectar ao servidor...(IPv4)"
                self.log(1)
                self.sock.connect((self.HOST, self.PORT))

            except socket.error:
                print "Servidor indisponivel =("
                self.log(7)
                exit(1)


    def start(self):

        # Registra o inicio do cliente:
        self.log(0)

        # Criando a conexao:
        self.conecta()

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
                self.log(2)

            except socket.timeout:
                print "%do estouro de timeout no envio da mensagem teste" % i+1
                self.log(5)

            except socket.error:
                print "Meu servidor caiu 3"
                self.log(7)
                exit(1)

            # Se rolou de enviar, agora recebe os dados e analiza
            try:
                data = self.sock.recv(1024)

            except socket.error:
                print "Conexao perdida"
                self.log(7)
                exit(1)

            # Validando a resposta:
            if data == 'Opa, eh nois!':
                print "Conexao efetuada com sucesso"
                self.log(6)
                break

            elif data == '':
                print "Meu servidor caiu 2"
                self.log(7)
                exit(1)



        # Conexao feita, eh hora de aguardar a entrada do usuario.
        while True:

            # Recebendo dados do usuario:
            data = raw_input("Digite a expressao aritmetica: ")

            # Enviando dados e armazenando no log:
            try:
                self.sock.send(data)
                self.log(3,data)

            except socket.error:
                print "Meu servidor caiu 4"
                self.log(7)
                exit(1)

            # Recebendo dados do servidor e atualizando o log
#            try:
            data = self.sock.recv(1024)
            print "R: %s" % str(data)
            self.log(4,data)

#            except socket.error:
#                print "Meu servidor caiu 5"
#                self.log(8)
#                exit(1)
# 



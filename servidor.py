#!/usr/bin/env python
# -*- coding: utf-8 -*-

# servidor.py

import socket, time
from datetime import datetime

class Servidor(object):

    def __init__(self,ME,MINHA_PORTA,l_hosts,l_ports,logFP):

        self.ME = ME
        self.DATA = ''
        self.PORT = MINHA_PORTA
        self.INDICE = l_hosts.index(self.ME)
        self.MAX_HOSTS = len(l_hosts)
        self.logFile = logFP
        self.l_hosts = l_hosts
        self.l_ports = l_ports


    def log(self,msg,maq=None):

        ''' diferentes niveis de log:
            0 - inicio
            1 - recebimento de mensagem
            2 - envio de mensagem
            3 - texto de confirmacao de conexao com o cliente
            4 - servidor desta maquina aparentemente desligado
            5 - desligamento do servidor
            6 - repassando mensagem de teste na ida
            7 - repassando mensagem de teste na volta
            8 - tentando conexao ipv6
            9 - conexao ipv6 indisponivel, mudando para ipv4
           10 - CONEXAO IPV6 HUHUHUHUH
           10 - CONEXAO IPV4
        '''
        textmsg = [ "\nIniciando "+self.ME+" em modo servidor: "+datetime.now().ctime()+"\n",
                    self.ME+" diz: Recebi "+str(self.DATA)+": "+datetime.now().ctime()+"\n",
                    self.ME+" diz: Enviei "+str(self.DATA)+": "+datetime.now().ctime()+"\n",
                    self.ME+" confirmando teste de conexao com o cliente: "+datetime.now().ctime()+"\n",
                    self.ME+" meu servidor (%s) parece estar desconectado. "%str(maq)+datetime.now().ctime()+"\n",
                    self.ME+" -> Desligando...\n",
                    self.ME+" repassando mensagem de teste (ida)\n",
                    self.ME+" repassando mensagem de teste (volta)\n",
                    self.ME+" diz: tentando conectar usando ipv6. "+datetime.now().ctime()+"\n",
                    self.ME+" diz: ipv6 falhou, usando ipv4. "+datetime.now().ctime()+"\n",
                    self.ME+" diz: conectei-me usando IPv6 "+datetime.now().ctime()+"\n",
                    self.ME+" diz: conectei-me usando IPv4 "+datetime.now().ctime()+"\n"
                  ]

        self.logFile.write(textmsg[msg])


    def fala(self,para_onde,cliente=0): # para_onde eh um socket

        # Enviando dados e armazenando no log:
        try:
            para_onde.send(self.DATA)

            # Testa aqui se self.DATA nao eh vazio, isso faz diferenca no log.
            if self.DATA:

                # Conforme a mensagem, registra um log diferente:
                # Para registrar sucesso na conexao:
                if cliente == 1:
                    self.log(3)

                # Para registrar mensagem de teste na ida:
                elif cliente == 2:
                    self.log(6)

                # Para registrar mensagem de teste na volta:
                elif cliente == 3:
                    self.log(7)

                else:
                    self.log(2)


        except socket.error:

            print self.MEU_SERVIDOR+" parece estar desconectado\n"

            # Registrando isso no log:
            self.log(4,self.MEU_SERVIDOR)

            # Registrando saida:
            self.log(5)
            exit(1)



    def escuta(self, de_onde): # de_onde eh um socket

        # Recebe os dados.
        try:
            self.DATA = de_onde.recv(1024)
            if self.DATA != 'Iae vei? Firmeza?' and self.DATA != 'Opa, eh nois!':
                self.log(1)

        except socket.error:
            print self.MEU_SERVIDOR+" parece estar desconectado\n"

            # Registrando isso no log:
            self.log(4,self.MEU_SERVIDOR)

            # Registrando saida:
            self.log(5)
            exit(1)



    def start(self):

        self.log(0)

        if self.INDICE == 0:
            self.conecta_caso_1()

        elif self.INDICE == (self.MAX_HOSTS - 1):
            self.MEU_SERVIDOR = self.l_hosts[self.INDICE - 1]
            self.conecta_caso_3()

        else:
            self.conecta_caso_2()

        while True:

            # Caso 3 possui uma unica conexao (1 cliente, 0 servidor):
            if self.INDICE == (self.MAX_HOSTS - 1):

                # Recebe os dados
                self.escuta(self.clientConn[0])

                # Verifica se eh mensagem de teste de conexao do cliente e
                # responde que ta on:
                if self.DATA == 'Iae vei? Firmeza?':
                    self.DATA = 'Opa, eh nois!'

                    # Um parametro a mais, para enviar para o log que a mensagem
                    # teste esta sendo enviada:
                    self.fala(self.clientConn[0],1)

                # Se nao for uma mensagem teste, avalia a expressao matematica:
                else:
                    print "Recebi expressao %s" % self.DATA

                    try:
                        self.DATA = str(eval(self.DATA))

                    except:
                        self.DATA = 'Qual parte do \'aritmetica\' vc nao entendeu?'

                    print "Enviando resposta..."
                    self.fala(self.clientConn[0])

            # Se nao for o caso 3, pode ser o caso 1 ou 2
            else:

                # Escuta da maquina anterior:
                self.escuta(self.clientConn[0])
                if not self.DATA: break

                # Fala para a proxima maquina:
                elif self.DATA == 'Iae vei? Firmeza?':
                    self.fala(self.sock_servidor,2)

                else:
                    self.fala(self.sock_servidor)


                # Aguarda resposta:
                self.escuta(self.sock_servidor)
                if not self.DATA: break

                # Responde para a proxima maquina:
                elif self.DATA == 'Opa, eh nois!':
                    self.fala(self.clientConn[0],3)

                else:
                    # Envia resposta
                    self.fala(self.clientConn[0])

    # Cria a conexao para o cliente:
    def conecta_cliente(self,PORT):
        ''' Cria a conexao, primeiro tenta fazer ipv6, se falhar faz ipv4
        '''

        # Abrindo socket IPv6:
        try:
            self.sock_cliente = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        except socket.error:
            print "Nao foi possivel abrir o socket"
            self.log(9)

        try:
            # Criando a conexao para escutar o cliente. Novamente, como na
            # implementacao o modelo eh deterministico, nao eh necessario
            # checar quem eh o cliente, apenas uma maquina tentara acessar esta
            # maquina por esta porta
            self.sock_cliente.bind(('', PORT))
            self.log(10)

        except socket.error:
            print "Conexao IPv6 falhou"
            self.log(9)

            # Usando IPv4, assumindo que vai dar sempre certo:
            self.sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_cliente.bind(('', PORT))

        self.sock_cliente.listen(3)
        self.clientConn = self.sock_cliente.accept()
        print "Meu cliente: ",self.clientConn[0].getsockname()


    # Cria uma conexao com o servidor;
    def conecta_meu_servidor(self,HOST,PORT):

        # Tenta fazer a conexao com IPv6:
        try:
            self.sock_servidor = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        except socket.error:
            self.log(9)

        # Tenta se conectar:
        try:
            self.log(8)
            self.sock_servidor.connect((HOST, PORT))
            self.log(10)

        except socket.error:

            try:
                # Tenta o IPv4:
                self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock_servidor.connect((HOST, PORT))
                self.log(11)

            except socket.error:
                print HOST+" parece estar desconectado\n"

                # Registrando isso no log:
                self.log(4,HOST)

                # Registrando saida:
                self.log(5)
                exit(1)

        print "Meu servidor: ",self.sock_servidor.getpeername()


    def conecta_caso_1(self):
        ''' Caso 1 eh quando o servidor eh o 1o da lista, ou seja, ele deve
        esperar uma conexao vinda de uma maquina qualquer, portanto, ele nao
        define um cliente, apenas um servidor ao qual se conectar.
        '''

        # Definindo caracteristicas da conexao do servidor:
        HOST = ''
        PORT = self.l_ports[0]

        # Conecta com o cliente:
        self.conecta_cliente(PORT)

        # Conecta com o Servidor:
        self.MEU_SERVIDOR = self.l_hosts[self.l_hosts.index(self.ME)+1]
        self.PORTA_FALA = self.l_ports[self.l_hosts.index(self.ME)+1]

        self.conecta_meu_servidor(self.MEU_SERVIDOR,self.PORTA_FALA)



    def conecta_caso_2(self):
        ''' Caso 2 eh quando uma maquina nao eh a 1a da lista, mas uma maquina
        entre a primeira e a ultima da lista. Entao sao necessarias duas
        conexoes, uma com o cliente e outra com o servidor da maquina onde essa
        parte do programa esta em execucao.
        '''

        # Informacoes para conectar com o cliente:
        self.MEU_CLIENTE = self.l_hosts[self.l_hosts.index(self.ME)-1]
        self.PORTA_ESCUTA = self.l_ports[self.l_hosts.index(self.ME)]

        # Informacoes para conectar com o servidor
        self.MEU_SERVIDOR = self.l_hosts[self.l_hosts.index(self.ME)+1]
        self.PORTA_FALA = self.l_ports[self.l_hosts.index(self.ME)+1]

        # Conecta com o cliente:
        self.conecta_cliente(self.PORTA_ESCUTA)

        # Como a implementacao cria uma conexao deterministica, eh desnecessario
        # testar se o cliente eh o esperado
        #self.sock_cliente.bind((MEU_CLIENTE, PORTA_ESCUTA))


        # Conecta com o Servidor:
        self.conecta_meu_servidor(self.MEU_SERVIDOR, self.PORTA_FALA)


    def conecta_caso_3(self):
        ''' Caso 3 eh quando o servidor eh o ultimo, ele vai apenas ouvir na
        porta dele, efetuar a operacao matematica e devolver o resultado.
        '''

        self.MEU_CLIENTE = self.l_hosts[-2]
        self.PORTA_ESCUTA = self.l_ports[-1]

        # Conecta com o cliente:
        self.conecta_cliente(self.PORTA_ESCUTA)

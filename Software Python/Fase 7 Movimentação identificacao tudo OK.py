# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:37:49 2016

@author: Darlan.Magnus
"""

class Image ():
    # Inicia a classe
    def __init__(self, colunas, linhas):
        self.coluna = colunas
        self.linha = linhas
        self.maxvalue = 255
        self.data = [[[0,0,0] for i in range(self.coluna)] for j in range(self.linha)]

    # determina a cor do pixel selecionado
    def set_pixel(self, y, x, color):
        m = max(color)
        if m > self.maxvalue:
            self.maxvalue = m
        self.data[y][x] = color

    # Salva arquivo com as configurações ppm
    def save(self, filename):
        with open(filename,'w') as f:
            f.write("P3\n%d %d\n%d\n"%(self.coluna, self.linha, self.maxvalue))
            for line in self.data:
                for (r,g,b) in line:
                    f.write("%d %d %d\n" % (r,g,b))
        

class Arquivo():
    def __init__(self):
        self.numLinhas = 0
        self.numColunas = 0
        self.matriz = None
        
    def obtemTamanhoMatriz(self):
        arquivo = open('mapa01.txt', 'r')
        linha = arquivo.readline()
        arquivo.close()
        arquivo = open('mapa01.txt', 'r')
        coluna = arquivo.readlines()
        arquivo.close()
        self.numColunas = len(linha)-1
        self.numLinhas = len(coluna)        
        #print 'Linhas: %d' %(self.numLinhas)
        #print 'Colunas: %d' %(self.numColunas)        
        arquivo = open('mapa01.txt', 'r')
        linha = arquivo.readline()
        
        #Cria um vetor de 0 com o numero de COLUNAS lidos
        self.matriz = [0]*self.numColunas
        # Cria uma matriz de zeros com o numero de LINHAS lidos
        for i in range(self.numLinhas):
            self.matriz[i] = [0]*self.numColunas
        
        for y in range(self.numLinhas):
            for x in range(self.numColunas):
                self.matriz[y][x] = linha[x]
            if(y <= self.numLinhas):
                linha = arquivo.readline()
            else:
                arquivo.close()
        
    
class Sensor():    
    def __init__(self):
        self.contaImg = 0                   #Contador para nomes de imagens .ppm
        self.listaPosicoes = []             #guarda todas as coordenadas por onde o robo passou
        self.listaEscaneada = []            #Guarda todas posições livres
        self.listaEscaneadoAnterior = []    #Guarda todas posições livres lidas anterirmente
        self.listaParedes = []              #Guarda todos as paredes descobertas
    
    def percorreAngulos(self, partida, orient):
        arq = Arquivo()
        arq.obtemTamanhoMatriz()
        img = Image(arq.numColunas, arq.numLinhas)
        angulo = [0, 45, 90, 135, 180]
        #Lista escaeado anterior recebe o backup dos pontos lidos anteriores
        self.listaEscaneadoAnterior.extend(self.listaEscaneada)
        #zera lista escaneada
        self.listaEscaneada = []
        
        if orient == 'norte':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha ------------------
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x - 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x - 1
                        y = y - 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y - 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y - 1
                        x = x + 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x + 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
            y,x = partida     # x = coluna  y= linha
#-----------------------------------------------------------------------------------------
        elif orient == 'leste':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y - 1                    # diminui linhas
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x + 1                    #soma linhas e colunas
                        y = y - 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x + 1                    #Soma colunas
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y + 1                    #Soma linhas e colunas
                        x = x + 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y + 1                    #Soma linhas
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
            y,x = partida     # x = coluna  y= linha
#------------------------------------------------------------------------------------
        elif orient == 'sul':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x + 1                    #aumento colunas
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x + 1                    #Soma linhas e colunas
                        y = y + 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y + 1                    #Aumenta linhas 
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y + 1                    #aumenta linha diminui coluna
                        x = x - 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x - 1                    #Diminui linhas e colunas
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
            y,x = partida     # x = coluna  y= linha
#----------------------------------------------------------------------------------
        elif orient == 'oeste':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y + 1                    #Aumento linhas
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x - 1                    #Aumento linhas diminui colunas
                        y = y + 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        x = x - 1                    #Diminui colunas
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y - 1                    #Diminui linhas e colunas
                        x = x - 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        #img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        self.listaEscaneada.append([y,x])
                        y = y - 1
                    #img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                    self.listaParedes.append([y,x])
            y,x = partida     # x = coluna  y= linha

        self.listaPosicoes.append(partida)
        """
        pontilhado = '-'*40
        print pontilhado
        print 'Lista onde o robo passou (AZUL):'
        print self.listaPosicoes
        print pontilhado
        print 'Lista Paredes encontradas (BRANCO):'
        print self.listaParedes
        print pontilhado
        print 'Lista Lugares descobertos (VERDE):'
        print self.listaEscaneada
        print pontilhado
        print 'Lista Lugares descobertos anteriormente (AMARELO):'
        print self.listaEscaneadoAnterior
        print pontilhado
        """
        
        for i in range(len(self.listaEscaneadoAnterior)):
            y,x = self.listaEscaneadoAnterior[i]
            img.set_pixel(y,x,[220,220,0])        #Amarelo (Lista onde o robo já escaneo)

        for i in range(len(self.listaEscaneada)):
            y,x = self.listaEscaneada[i]
            img.set_pixel(y,x,[0,220,0])          #Verde (Lista onde o sensor passou)
        
        for i in range(len(self.listaPosicoes)):
            y,x = self.listaPosicoes[i]
            img.set_pixel(y,x,[0,0,220])          #Azul (Localização do robô)

        for i in range(len(self.listaParedes)):
            y,x = self.listaParedes[i]
            img.set_pixel(y,x,[220,220,220])      #Branco (Lista onde o robo encontrou paredes)
        #Salva imagem ppm
        img.save('C:/Users/Darlan/Desktop/Imagens mapeamento/Mapa Walle %d.ppm' %(self.contaImg))
        self.contaImg = self.contaImg + 1         

#-------------------------------------------------------------------------------   

class Orientacao():
    def descobreOrientacao(self, orientac, direc):
        orientacao = orientac
        direcao = direc
        pos = orientac
        
        if orientacao == 'norte' and (direcao == 'D'):
            pos = 'leste'
            return pos
        if orientacao == 'norte' and (direcao == 'E'):
            pos = 'oeste'
            return pos
        if orientacao == 'leste' and (direcao == 'D'):
            pos = 'sul'
            return pos
        if orientacao == 'leste' and (direcao == 'E'):
            pos = 'norte'
            return pos
        if orientacao == 'sul' and (direcao == 'D'):
            pos = 'oeste'
            return pos
        if orientacao == 'sul' and (direcao == 'E'):
            pos = 'leste'
            return pos
        if orientacao == 'oeste' and (direcao == 'D'):
            pos = 'norte'
            return pos
        if orientacao == 'oeste' and (direcao == 'E'):
            pos = 'sul'
            return pos
        else:
            return pos








    
if __name__ == "__main__":
    partida = [4,4]     #(linha, coluna)
    y,x = partida      # y= linha  x = coluna
    destino = [0,0]
    sensor = Sensor()
    orientacao = Orientacao()
    frente = 'norte'
    listaComandos = []          #Grava todos os comando dados
    comando = None
    #Inicia arquivo do tamanho do mapa desenhado
    arq = Arquivo()
    arq.obtemTamanhoMatriz()
    img = Image(arq.numColunas, arq.numLinhas)
    #Salva previa do mapa vazio
    img.save('C:/Users/Darlan/Desktop/Imagens mapeamento/Mapa Walle %d.ppm' %(sensor.contaImg))
    sensor.contaImg = sensor.contaImg + 1    
    
    #verifica qual orientação
    frente = orientacao.descobreOrientacao(frente, comando)
    print frente
    # Escaneia e salva estado inicial com primeiro mapemento
    sensor.percorreAngulos(partida, frente)
    
    
    while comando != 'SAIR':
        comando = raw_input('Digite "F" frente, "D" 90º direita "E" 90º esquerda, "R" ré ou "sair": ')
        comando = comando.upper()
        if comando != 'SAIR':

            if comando == 'F':
                frente = orientacao.descobreOrientacao(frente, comando)
                print frente
                if frente == 'norte':
                    y = (y-1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        comando='@!'
                        y = (y+1)
                        destino = [y,x]
                        partida = destino
                    
                elif frente == 'leste':
                    x = (x+1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        x = (x-1)
                        destino = [y,x]
                        comando='@!'
                        partida = destino
                    
                elif frente == 'sul':
                    y = (y+1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        y = (y-1)
                        destino = [y,x]
                        comando='@!'
                        partida = destino
                    
                elif frente == 'oeste':
                    x = (x-1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        x = (x+1)
                        destino = [y,x]
                        comando='@!'
                        partida = destino
                    
                if comando != '@!':
                    # Escaneia a orientação e salva imagem ppm
                    print partida
                    sensor.percorreAngulos(partida, frente)
            
            elif comando == 'R':
                frente = orientacao.descobreOrientacao(frente, comando)
                print frente
                if frente == 'norte':
                    y = (y+1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneadoAnterior or destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        y = (y-1)
                        destino = [y,x]
                        comando='@!'
                        partida = destino
                    elif destino not in sensor.listaEscaneadoAnterior or destino not in sensor.listaEscaneada:
                        print 'Desculpe ainda não conhecemos esta área. Vire para escanear!'
                        comando = '@!'
                        y = (y-1)
                        destino = [y,x]
                        partida = destino
                    
                elif frente == 'leste':
                    x = (x-1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneadoAnterior or destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        x = (x+1)
                        destino = [y,x]
                        comando='@!'
                        partida = destino
                    elif destino not in sensor.listaEscaneadoAnterior or destino not in sensor.listaEscaneada:
                        print 'Desculpe ainda não conhecemos esta área. Vire para escanear!'
                        comando = '@!'
                        x = (x+1)
                        destino = [y,x]
                        partida = destino
                    
                elif frente == 'sul':
                    y = (y-1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneadoAnterior or destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        y = (y+1)
                        destino = [y,x]
                        comando='@!'
                        partida = destino
                    elif destino not in sensor.listaEscaneadoAnterior or destino not in sensor.listaEscaneada:
                        print 'Desculpe ainda não conhecemos esta área. Vire para escanear!'
                        comando = '@!'
                        y = (y+1)
                        destino = [y,x]
                        partida = destino
                    
                elif frente == 'oeste':
                    x = (x+1)
                    destino = [y,x]
                    if destino in sensor.listaEscaneadoAnterior or destino in sensor.listaEscaneada:
                        partida = destino
                    elif destino in sensor.listaParedes:
                        print 'Não é permitido avançar! Tem uma parede ai!'
                        x = (x-1)
                        destino = [y,x]
                        comando='@!'
                        partida = destino
                    elif destino not in sensor.listaEscaneadoAnterior or destino not in sensor.listaEscaneada:
                        print 'Desculpe ainda não conhecemos esta área. Vire para escanear!'
                        comando = '@!'
                        x = (x-1)
                        destino = [y,x]
                        partida = destino
                
                if comando != '@!':
                    # Escaneia a orientação e salva imagem ppm
                    print partida
                    sensor.percorreAngulos(partida, frente)
                
            elif comando == 'D':
                frente = orientacao.descobreOrientacao(frente, comando)
                print frente
                # Escaneia a orientação e salva imagem ppm
                sensor.percorreAngulos(partida, frente)
            elif comando == 'E':
                frente = orientacao.descobreOrientacao(frente, comando)
                print frente
                # Escaneia a orientação e salva imagem ppm
                sensor.percorreAngulos(partida, frente)
                
            else:
                print 'Comando não reconhecido! Utilize um válido!'
                comando='@!'
            
            if True and comando != '@!':
                #Salva uma lista com os comandos recebidos
                listaComandos.append([comando])            
    
    
    
    #printa todos os comando da lista
    for i in range(len(listaComandos)):
        print listaComandos[i]
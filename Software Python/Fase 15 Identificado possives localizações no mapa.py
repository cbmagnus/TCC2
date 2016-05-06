# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:37:49 2016

@author: Darlan.Magnus
"""
import os.path
import operator

class Image ():
    # Inicia a classe
    def __init__(self, colunas, linhas):
        self.coluna = colunas
        self.linha = linhas
        self.maxvalue = 240
        self.data = [[0 for i in range(self.coluna)] for j in range(self.linha)]
        self.listaEscaneado = []
        self.listaPosicoes = []
        self.lista_pos_localizacao = []

    # Salva matriz com valores do ultimo mapeamento feito e ultimo posicionamento
    def salvaMapeado(self, filename, matriz, ultimaPos):
        with open (filename, 'w') as f:
            f.write("%d%d\n" %(ultimaPos[0], ultimaPos[1]))
            for lin in matriz:
                for coluna in lin:
                    f.write("%d"%(coluna))
                f.write("\n")

    # Salva arquivo com as configurações ppm
    def save(self, filename):

        for i in range(len(self.lista_pos_localizacao)):
            y,x =  self.lista_pos_localizacao[i]
            self.data[y][x] = 5
        
        with open(filename,'w') as f:
            f.write("P3\n%d %d\n%d\n"%(self.coluna, self.linha, self.maxvalue))
            for lin in self.data:
                for coluna in lin:
                    if coluna == 0:
                        f.write("%d %d %d\n" % (20,20,20))      #Pinta de preto
                    elif coluna == 2:
                        f.write("%d %d %d\n" % (220,220,220))   #Pinta de Branco
                    elif coluna == 3:
                        f.write("%d %d %d\n" % (220,220,0))     #Pinta de Amarelo
                    elif coluna == 4:
                        f.write("%d %d %d\n" % (0,0,220))       #Pinta de Azul
                    elif coluna == 1:
                        f.write("%d %d %d\n" % (0,220,0))       #Pinta de Verde
                    elif coluna == 5:
                        f.write("%d %d %d\n" % (220,0,0))       #Pinta de Vermelho
                    else:
                        print 'numero desconhecido dentro do mapa'

        for i in range(len(self.listaEscaneado)):
            y,x =  self.listaEscaneado[i]
            self.data[y][x] = 3
        self.listaEscaneado = []
        
        for i in range(len(self.listaPosicoes)):
            y,x =  self.listaPosicoes[i]
            self.data[y][x] = 4
                
    # Salva valores em suas respectivas listas
    def salvaValor(self, y, x, valor):
        self.data[y][x] = valor
        
        if self.data[y][x] == 1:
            self.listaEscaneado.append([y,x])
        
        elif self.data[y][x] == 4:
            self.listaPosicoes.append([y,x])
        
        elif self.data[y][x] == 5:
            self.lista_pos_localizacao.append([y,x])

            

class Arquivo():
    def __init__(self):
        self.numLinhas = 0
        self.numColunas = 0
        self.matriz = None
        self.diretorioMapeado = 'mapeado/MapaMapeado.txt'
        self.diretorio_img_posicoes = 'mapeado/MapaMapeado.txt'
        self.mapaTerico = 'mapa01.txt'
        self.matrizMapeada = None
        self.ultimaPos = None
        self.cont = 0
        
    def obtemTamanhoMatriz(self):           #cria uma matriz com os valores lidos do txt
        arquivo = open(self.mapaTerico, 'r')
        linha = arquivo.readline()
        arquivo.close()
        arquivo = open(self.mapaTerico, 'r')
        coluna = arquivo.readlines()
        arquivo.close()
        self.numColunas = len(linha)-1
        self.numLinhas = len(coluna)
        arquivo = open(self.mapaTerico, 'r')
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
            
 
 
    def leArquivoMapeado(self):
        arquivo = open(self.diretorioMapeado, 'r')
        arquivo.readline()
        linha = arquivo.readline()
        arquivo.close()
        arquivo = open(self.diretorioMapeado, 'r')
        coluna = arquivo.readlines()
        arquivo.close()
        self.numColunas = len(linha)-1
        self.numLinhas = len(coluna)-1
        
        #Cria um vetor de 0 com o numero de COLUNAS lidos
        self.matrizMapeada = [0]*self.numColunas
        # Cria uma matriz de zeros com o numero de LINHAS lidos
        for i in range(self.numLinhas):
            self.matrizMapeada[i] = [0]*self.numColunas
            
        arquivo = open(self.diretorioMapeado, 'r')
        self.ultimaPos = arquivo.readline()
        linha = arquivo.readline()
        for y in range(self.numLinhas):
            for x in range(self.numColunas):
                self.matrizMapeada[y][x] = int(linha[x])
            if(y <= self.numLinhas):
                linha = arquivo.readline()
            else:
                arquivo.close()
        
   
class Sensor():
    def __init__(self):
        self.distanciasMapeadas = [0,0,0,0,0]
        self.distanciasOriginal = [0,0,0,0,0]
        
    def percorreAngulos(self, partida, orient, img, arq):
        self.dist0Graus = -1
        self.dist45Graus = -1
        self.dist90Graus = -1
        self.dist135Graus = -1
        self.dist180Graus = -1
        angulo = [0, 45, 90, 135, 180]
        if orient == 'norte':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha ------------------
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1
                        self.dist0Graus = self.dist0Graus + 1         #conta numero de casas livres à 0º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1
                        y = y - 1
                        self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1
                        self.dist90Graus = self.dist90Graus + 1       #conta numero de casas livres à 90º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1
                        x = x + 1
                        self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1
                        self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo

#-----------------------------------------------------------------------------------------
        elif orient == 'leste':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1                       # diminui linhas
                        self.dist0Graus =self.dist0Graus + 1          #conta numero de casas livres à 0º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #soma linhas e colunas
                        y = y - 1
                        self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #Soma colunas
                        self.dist90Graus = self.dist90Graus + 1        #conta numero de casas livres à 90º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Soma linhas e colunas
                        x = x + 1
                        self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Soma linhas
                        self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
#------------------------------------------------------------------------------------
        elif orient == 'sul':
            for i in range(len(angulo)):
                y,x = partida                           # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #aumento colunas
                        self.dist0Graus = self.dist0Graus + 1          #conta numero de casas livres à 0º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #Soma linhas e colunas
                        y = y + 1
                        self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Aumenta linhas 
                        self.dist90Graus = self.dist90Graus + 1        #conta numero de casas livres à 90º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #aumenta linha diminui coluna
                        x = x - 1
                        self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1                       #Diminui linhas e colunas
                        self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
#----------------------------------------------------------------------------------
        elif orient == 'oeste':
            for i in range(len(angulo)):
                y,x = partida                           # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Aumento linhas
                        self.dist0Graus = self.dist0Graus + 1          #conta numero de casas livres à 0º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1                       #Aumento linhas diminui colunas
                        y = y + 1
                        self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1                       #Diminui colunas
                        self.dist90Graus = self.dist90Graus + 1        #conta numero de casas livres à 90º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1                       #Diminui linhas e colunas
                        x = x - 1
                        self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1
                        self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                    self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
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


class Desloca():
    def __init__(self):
        self.diretorio = 'Imagens mapeamento/Mapa Walle'
        self.listaComandos = []
        self.destino = [0,0]
        self.contaImg = 0
        self.frente = 'norte'
        
    def anda(self, partid, frent, orientacao, img, comando):
        partida = partid
        print partida
        self.frente = frent
        y,x = partida      # y= linha  x = coluna
        if comando == 'F':
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            if self.frente == 'norte':
                y = (y-1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    comando='@!'
                    y = (y+1)
                    self.destino = [y,x]
                    partida = self.destino
                
            elif self.frente == 'leste':
                x = (x+1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    x = (x-1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                
            elif self.frente == 'sul':
                y = (y+1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    y = (y-1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                
            elif self.frente == 'oeste':
                x = (x-1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    x = (x+1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                
            if comando != '@!':
                # Escaneia a orientação e salva imagem ppm
                print partida
                arq.ultimaPos = partida
                sensor.percorreAngulos(partida, self.frente, img, arq)
                img.save('%s %d.ppm' %(self.diretorio, self.contaImg))
                self.contaImg = self.contaImg + 1 
        
        elif comando == 'R':
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            if self.frente == 'norte':
                y = (y+1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    y = (y-1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                elif img.data[y][x] == 0:
                    print 'Desculpe ainda nao conhecemos esta area. Vire para escanear!'
                    comando = '@!'
                    y = (y-1)
                    self.destino = [y,x]
                    partida = self.destino
                
            elif self.frente == 'leste':
                x = (x-1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    x = (x+1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                elif img.data[y][x] == 0:
                    print 'Desculpe ainda nao conhecemos esta area. Vire para escanear!'
                    comando = '@!'
                    x = (x+1)
                    self.destino = [y,x]
                    partida = self.destino
                
            elif self.frente == 'sul':
                y = (y-1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    y = (y+1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                elif img.data[y][x] == 0:
                    print 'Desculpe ainda nao conhecemos esta area. Vire para escanear!'
                    comando = '@!'
                    y = (y+1)
                    self.destino = [y,x]
                    partida = self.destino
                
            elif self.frente == 'oeste':
                x = (x+1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    x = (x-1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                elif img.data[y][x] == 0:
                    print 'Desculpe ainda nao conhecemos esta area. Vire para escanear!'
                    comando = '@!'
                    x = (x-1)
                    self.destino = [y,x]
                    partida = self.destino
            
            if comando != '@!':
                # Escaneia a orientação e salva imagem ppm
                print partida
                arq.ultimaPos = partida
                sensor.percorreAngulos(partida, self.frente, img, arq)
                img.save('%s %d.ppm' %(self.diretorio, self.contaImg))
                self.contaImg = self.contaImg + 1
            
        elif comando == 'D':
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            # Escaneia a orientação e salva imagem ppm
            sensor.percorreAngulos(partida, self.frente, img, arq)
            img.save('%s %d.ppm' %(self.diretorio, self.contaImg))
            self.contaImg = self.contaImg + 1
        
        elif comando == 'E':
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            # Escaneia a orientação e salva imagem ppm
            sensor.percorreAngulos(partida, self.frente, img, arq)
            img.save('%s %d.ppm' %(self.diretorio, self.contaImg))
            self.contaImg = self.contaImg + 1
            
        else:
            print 'Comando nao reconhecido! Utilize um valido!'
            comando='@!'
            return partida
        
        if True and comando != '@!':
            #Salva uma lista com os comandos recebidos
            self.listaComandos.append(comando)
            return partida
            
        else:
            print partida
            return partida

    def salvaPassos(self, nome):
        with open(nome, 'w') as f:
            for linha in self.listaComandos:
                f.write('%s\n'%(linha))


class Automatico():
    def auto(self, partid, orientacao, img, sensor, anda, arq):
        y,x = partid
        partida = partid     
        saida = 0
        
        while saida < 1:
            partida = anda.anda(partida, anda.frente, orientacao, img, 'F')
            print '-----------'
            y,x = partida
            if anda.frente == 'norte' and img.data[y-1][x] == 2:
                if img.data[y-1][x] == 2 and img.data[y][x+1] != 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida
                elif img.data[y-1][x] == 2 and img.data[y][x+1] == 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'E')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida
                    
                elif img.data[y+1][x] != 2 and img.data[y][x+1] == 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida

            elif anda.frente == 'leste':
                if img.data[y-1][x] != 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'E')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida
                elif img.data[y+1][x] != 2 and img.data[y][x+1] == 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida

            elif anda.frente == 'sul':
                if img.data[y][x+1] != 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'E')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida
                elif img.data[y][x-1] != 2 and img.data[y+1][x] == 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida

            elif anda.frente == 'oeste':
                if img.data[y+1][x] != 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'E')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida
                elif img.data[y-1][x] != 2 and img.data[y][x-1] == 2:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D')
                    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                    y,x = partida
            #Percorre a lista de posições para saber se ja esteve ali
            tam =len(img.listaPosicoes)-1
            for i in range(len(img.listaPosicoes)):
                if img.listaPosicoes[i] == partida and i != tam and i != (tam -1): #Se posição for iguar a já visitada e não é a ultima ou penultima
                    saida = saida + 1
                    arq.ultimaPos = partida
                    
        return 'SAIR'
   
   
if __name__ == "__main__":
    partida = [3,3]     #(linha, coluna)
    sensor = Sensor()
    direcoes = ['norte', 'leste', 'sul', 'oeste']
    orientacao = Orientacao()
    comando = None
    anda = Desloca()
    auto = Automatico()
    arq = Arquivo()
    img = Image(arq.numColunas, arq.numLinhas)
    
    while comando != 'SAIR':
        if os.path.exists(arq.diretorioMapeado) and len(open(arq.diretorioMapeado, 'r').readlines()) > 2:
            print 'Já existe um mapa cadastrado'
            arq.leArquivoMapeado()
            img = Image(arq.numColunas, arq.numLinhas)
            print 'Ultima posição: LINHA:'+ arq.ultimaPos[0], 'COLUNA:'+ arq.ultimaPos[1]
            print arq.matrizMapeada

            arq.matriz = arq.matrizMapeada
            sensor.percorreAngulos(partida, anda.frente, img, arq)
            
            sensor.distanciasOriginal[0] = sensor.distanciasMapeadas[0]
            sensor.distanciasOriginal[1] = sensor.distanciasMapeadas[1]
            sensor.distanciasOriginal[2] = sensor.distanciasMapeadas[2]
            sensor.distanciasOriginal[3] = sensor.distanciasMapeadas[3]
            sensor.distanciasOriginal[4] = sensor.distanciasMapeadas[4]
            print sensor.distanciasOriginal
            
            # 2 loops para percorrer todas posições que forem igual a 3 e 4
            for y in range(arq.numLinhas):
                for x in range(arq.numColunas):
                    print 'Valor da posição=', arq.matrizMapeada[y][x]
                    # Se a posição for igual 3 ou 4 mapeia em todas direções e compara com valores recebidos do robô
                    if arq.matrizMapeada[y][x] == 3 or arq.matrizMapeada[y][x] == 4:
                        for direcao in direcoes:
                            print direcao.upper()
                            sensor.percorreAngulos([y,x], direcao, img, arq)
                            print sensor.distanciasOriginal
                            print sensor.distanciasMapeadas
                            # Se valores de mapeamento forem igual a do robô é uma possivel posição identificada com numero 5
                            if all(map(operator.eq, sensor.distanciasOriginal, sensor.distanciasMapeadas)):
                                img.salvaValor(y,x,5)
                                img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
                                anda.contaImg = anda.contaImg + 1
                            else:
                                print 'Não são compativeis'
                    else:
                        print 'Não é possivel estar aqui. Possivel parede!'
            
            img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
            anda.contaImg = anda.contaImg + 1
            print img.lista_pos_localizacao
            
            
                
            
            comando = 'SAIR'
            
        else:
            print 'Arquivo não encontrado ou não atende aos parâmetros de mapa esperados!'
            print 'Deseja realizar o mapeamento?'
            comando = raw_input('Digite Sim [S] Não [N] ou SAIR:')
            comando = comando.upper()
            if comando == 'S':
                arq.obtemTamanhoMatriz()
                img = Image(arq.numColunas, arq.numLinhas)
                #Salva previa do mapa vazio
                img.save('%s %d.ppm' %(anda.diretorio, anda.contaImg))
                anda.contaImg = anda.contaImg + 1
                #verifica qual orientação
                anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
                # Copia mapa teorico para matrizMapeada para não dar erro de verificação de matriz nula quando compara em percorre angulos
                arq.matrizMapeada = arq.matriz
                # Escaneia e salva estado inicial com primeiro mapemento
                sensor.percorreAngulos(partida, anda.frente, img, arq)
                img.save('%s %d.ppm' %(anda.diretorio, anda.contaImg))
                anda.contaImg = anda.contaImg + 1
                
                # Inicia mapeamento automatico
                comando = auto.auto(partida, orientacao, img, sensor, anda, arq)
                # Salava mapa com numeros de identificação
                img.salvaMapeado(arq.diretorioMapeado, img.data, arq.ultimaPos)
                
                print '\nMapeamento realizado com sucesso!\n'
                
            elif comando == 'N' or comando == 'SAIR':
                print 'OK Bye!'
                comando = 'SAIR'
            else:
                print 'Comando não conhecido!'

    #Salva os passos em um txt
    anda.salvaPassos('Comandos utilizados.txt')
    
    #printa todos os comando da lista
    for i in range(len(anda.listaComandos)):
        print anda.listaComandos[i]
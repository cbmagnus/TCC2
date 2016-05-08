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
        self.lista_direcoes = []
        self.lista_compara_distancias = []
        self.listaParticulasCriadas = []

    # Salva matriz com valores do ultimo mapeamento feito e ultimo posicionamento
    def salvaMapeado(self, filename, matriz, ultimaPos):
        with open (filename, 'w') as f:
            f.write("%d %d\n" %(ultimaPos[0], ultimaPos[1]))
            for lin in matriz:
                for coluna in lin:
                    f.write("%d"%(coluna))
                f.write("\n")

    # Salva arquivo com as configurações ppm
    def save(self, filename):

        #Força a sobreposição de cores da matriz 
        for i in range(len(self.lista_pos_localizacao)):
            y,x =  self.lista_pos_localizacao[i]
            self.data[y][x] = 5
        #Força a sobreposição de cores da matriz  
        for i in range(len(self.listaParticulasCriadas)):
            y,x =  self.listaParticulasCriadas[i]
            self.data[y][x] = 6
        
        with open(filename,'w') as f:
            f.write("P3\n%d %d\n%d\n"%(self.coluna, self.linha, self.maxvalue))
            for lin in self.data:
                for coluna in lin:
                    if coluna == 0:
                        f.write("%d %d %d\n" % (20,20,20))      #Pinta de preto     (Area desconhecida)
                    elif coluna == 2:
                        f.write("%d %d %d\n" % (220,220,220))   #Pinta de Branco    (Parede)
                    elif coluna == 3:
                        f.write("%d %d %d\n" % (220,220,0))     #Pinta de Amarelo   (Area já mapeada)
                    elif coluna == 4:
                        f.write("%d %d %d\n" % (0,0,220))       #Pinta de Azul      (Lugares onde robo passou)
                    elif coluna == 1:
                        f.write("%d %d %d\n" % (0,220,0))       #Pinta de Verde     (Lugares livres escaneados)
                    elif coluna == 5:
                        f.write("%d %d %d\n" % (220,0,0))       #Pinta de Vermelho  (Possiveis posições)
                    elif coluna == 6:
                        f.write("%d %d %d\n" % (200,115,60))       #Pinta de Laranja  (Posições das particulas)
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
        
        elif self.data[y][x] == 5 or self.data[y][x] == 6:
            self.lista_pos_localizacao.append([y,x])

            

class Arquivo():
    def __init__(self):
        self.numLinhas = 0
        self.numColunas = 0
        self.matriz = None
        self.diretorio = 'Imagens mapeamento/Mapa Walle'
        self.diretorio_img_posicoes = 'mapeado/MapaMapeado.txt'
        self.mapaTeorico = 'mapa01.txt'
        self.matrizMapeada = None
        self.ultimaPos = None
        self.cont = 0
        
    def obtemTamanhoMatriz(self):           #cria uma matriz com os valores lidos do txt
        arquivo = open(self.mapaTeorico, 'r')
        linha = arquivo.readline()
        arquivo.close()
        arquivo = open(self.mapaTeorico, 'r')
        coluna = arquivo.readlines()
        arquivo.close()
        self.numColunas = len(linha)-1
        self.numLinhas = len(coluna)
        arquivo = open(self.mapaTeorico, 'r')
        linha = arquivo.readline()
        
        if self.numLinhas > self.numColunas:
            #Cria um vetor de 0 com o numero de LINHAS lidos
            self.matriz = [0]*self.numLinhas
        else:
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
        arquivo = open(self.diretorio_img_posicoes, 'r')
        arquivo.readline()
        linha = arquivo.readline()
        arquivo.close()
        arquivo = open(self.diretorio_img_posicoes, 'r')
        coluna = arquivo.readlines()
        arquivo.close()
        self.numColunas = len(linha)-1
        self.numLinhas = len(coluna)-1
        
        if self.numLinhas > self.numColunas:
            #Cria um vetor de 0 com o numero de LINHAS lidos
            self.matrizMapeada = [0]*self.numLinhas
        else:
            #Cria um vetor de 0 com o numero de COLUNAS lidos
            self.matrizMapeada = [0]*self.numColunas
        
        # Cria uma matriz de zeros com o numero de LINHAS lidos
        for i in range(self.numLinhas):
            self.matrizMapeada[i] = [0]*self.numColunas
            
        arquivo = open(self.diretorio_img_posicoes, 'r')
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
        self.listaComandos = []
        self.destino = [0,0]
        self.contaImg = 0
        self.frente = 'norte'
        self.comando = None
        
    def anda(self, partid, frent, orientacao, img, comando, diretorio):
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
                img.save('%s %d.ppm' %(diretorio, self.contaImg))
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
                img.save('%s %d.ppm' %(diretorio, self.contaImg))
                self.contaImg = self.contaImg + 1
            
        elif comando == 'D':
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            # Escaneia a orientação e salva imagem ppm
            sensor.percorreAngulos(partida, self.frente, img, arq)
            img.save('%s %d.ppm' %(diretorio, self.contaImg))
            self.contaImg = self.contaImg + 1
        
        elif comando == 'E':
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            # Escaneia a orientação e salva imagem ppm
            sensor.percorreAngulos(partida, self.frente, img, arq)
            img.save('%s %d.ppm' %(diretorio, self.contaImg))
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
        chegada = []
        # Enquanto não chegar ao ponto da primeira curva segue percurso
        while chegada != partida:
            print sensor.distanciasMapeadas #[0, 45, 90, 135, 180]
            # Enquanto eu não encontrar parede vou para frente
            while sensor.distanciasMapeadas[2] != 0:               # 90º graus
                partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                y,x = partida
            if sensor.distanciasMapeadas[0] != 0:
                chegada = [y,x-1]
            else:
                chegada = partida
            partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
            
            # Segue o curso até encontrar uma posição conhecida e fexar programa
            while chegada != partida:
                while sensor.distanciasMapeadas[0] == 0 and chegada != partida:        #Enquanto tiver a parede a esquerda
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                    
                    if sensor.distanciasMapeadas[0] != 0:
                        partida = anda.anda(partida, anda.frente, orientacao, img, 'E', arq.diretorio)
                        partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                    
                    elif sensor.distanciasMapeadas[0] == 0 and sensor.distanciasMapeadas[2] == 0 and sensor.distanciasMapeadas[4] == 0:
                        partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
                        partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
                        
                    elif sensor.distanciasMapeadas[2] == 0:               # 90º graus
                        partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
        return 'SAIR'
   
   
   
class EncontraPossiveisPosicoes():
    def verificaTodasPosicoes(self, arq, direcoes, sensor, img, anda):
        # 2 loops para percorrer todas posições que forem igual a 3 e 4 e salva 
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
                            img.lista_direcoes.append(direcao)
                            img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
                            anda.contaImg = anda.contaImg + 1
                        else:
                            print 'Não são compativeis'
                else:
                    print 'Não é possivel estar aqui. Possivel parede!'
        img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
        print '\n',img.lista_pos_localizacao
        print img.lista_direcoes,'\n'
        
        
    def eliminaPosicoesDoVetor(self, arq, direcoes, sensor, img, anda):
        cont = 0    #Contador indicando as direções para o robo virar N, L, S, O
        nort = 0    
        while len(img.lista_pos_localizacao) > 1:
            # Gira 360º mapeando cada direção para tentar achar sua localização
            while cont < 4 and len(img.lista_pos_localizacao) > 1:
                # Limpa a lista de escaneamento
                img.lista_compara_distancias = []
                sensor.distanciasOriginal = [0,0,0,0,0] 
                
                print mapeamentoDoRobo
                print img.lista_pos_localizacao
                print '\n',direcoes[cont],'\n'
                
                #Gira todos para direita e compara com a leitura feita pelo robo
                contPos = 0     #Contador da posição dentro da lista de direções
                for posicao in img.lista_pos_localizacao:
                    print posicao
                    partida = anda.anda(posicao, img.lista_direcoes[contPos], orientacao, img, 'D', arq.diretorio)
                    contPos = contPos + 1
                    lista_direcoes_atualizada.append(anda.frente)
                    print img.lista_direcoes
                    print lista_direcoes_atualizada
                
                contPos = 0     #Contador da posição dentro da lista de direções ZERADO
                #Para cada posição realiza um loop de escanemento e comparação
                for posicao in img.lista_pos_localizacao:
                    y,x = posicao
                    sensor.percorreAngulos([y,x], lista_direcoes_atualizada[contPos], img, arq)
                    #Variavel recebe valores esaneados para não dar erro de receber o mesmo valor
                    sensor.distanciasOriginal[0] = sensor.distanciasMapeadas[0]
                    sensor.distanciasOriginal[1] = sensor.distanciasMapeadas[1]
                    sensor.distanciasOriginal[2] = sensor.distanciasMapeadas[2]
                    sensor.distanciasOriginal[3] = sensor.distanciasMapeadas[3]
                    sensor.distanciasOriginal[4] = sensor.distanciasMapeadas[4]
                    # Inclui na lista de escaneamentos as posições encontradas e logo depois zera a variavel para liberar para proxima
                    img.lista_compara_distancias.append(sensor.distanciasOriginal)
                    sensor.distanciasOriginal = [0,0,0,0,0]
                    # Salva imagem do escaneamento

                img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
                anda.contaImg = anda.contaImg + 1
                cont = cont + 1   # Muda a direção
                excluir = []
                print img.lista_compara_distancias
                for num in range(len(img.lista_compara_distancias)):
                    if all(map(operator.eq, img.lista_compara_distancias[0], img.lista_compara_distancias[num])) and len(img.lista_compara_distancias) > 1:
                        print 'continua'
                    else:
                        excluir.append(num)
                for i in reversed(excluir):
                    del img.lista_compara_distancias[i]
                    del img.lista_pos_localizacao[i]
                    del img.lista_direcoes[i]
                img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
                anda.contaImg = anda.contaImg + 1
                    
            cont = 0
            # Se Mesmo girando 360º Graus não sobrou apenas uma posição começa a andar e escanear
            # Anda para o norte até encontrar parede e escaneia posição por posição até a parede ao sul
            if sensor.distanciasMapeadas[4] != 0 and nort != 1 and len(img.lista_pos_localizacao) > 1:
                print img.lista_pos_localizacao
                for indice, pos in enumerate(img.lista_pos_localizacao):
                    partida = anda.anda(pos, 'norte', orientacao, img, 'F', arq.diretorio)
                    img.lista_pos_localizacao[indice] = partida
                print img.lista_pos_localizacao
            
            elif sensor.distanciasMapeadas[4] == 0 and len(img.lista_pos_localizacao) > 1:
                nort = 1
                print img.lista_pos_localizacao
                for indice, pos in enumerate(img.lista_pos_localizacao):
                    partida = anda.anda(pos, 'sul', orientacao, img, 'F', arq.diretorio)
                    img.lista_pos_localizacao[indice] = partida
                print img.lista_pos_localizacao
            
            elif sensor.distanciasMapeadas[0] != 0 and nort == 1 and len(img.lista_pos_localizacao) > 1:
                print img.lista_pos_localizacao
                for indice, pos in enumerate(img.lista_pos_localizacao):
                    partida = anda.anda(pos, 'sul', orientacao, img, 'F', arq.diretorio)
                    img.lista_pos_localizacao[indice] = partida
                print img.lista_pos_localizacao
                    
        
        print '\nSua posição é:', img.lista_pos_localizacao
        # Salva imagem do escaneamento
        #img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
        #anda.contaImg = anda.contaImg + 1
        anda.comando = 'SAIR'
   
   
class Mapeia():
    def realizaMapeamento(self, arq, img, anda, sensor, partida):
        arq.obtemTamanhoMatriz()
        img = Image(arq.numColunas, arq.numLinhas)
        #Salva previa do mapa vazio
        img.save('%s %d.ppm' %(arq.diretorio, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
        print anda.comando
        #verifica qual orientação
        anda.frente = orientacao.descobreOrientacao(anda.frente, anda.comando)
        # Copia mapa teorico para matrizMapeada para não dar erro de verificação de matriz nula quando compara em percorre angulos
        arq.matrizMapeada = arq.matriz
        # Escaneia e salva estado inicial com primeiro mapemento
        sensor.percorreAngulos(partida, anda.frente, img, arq)
        img.save('%s %d.ppm' %(arq.diretorio, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
        
        # Inicia mapeamento automatico
        anda.comando = auto.auto(partida, orientacao, img, sensor, anda, arq)
        # Salava mapa com numeros de identificação
        img.salvaMapeado(arq.diretorio_img_posicoes, img.data, arq.ultimaPos)
        print '\nMapeamento realizado com sucesso!\n'

            
    def criaParticulas(self, img, arq, anda):
        #Cria particulas em torno de cada posição encontrada
        for pos in img.lista_pos_localizacao:
            y,x = pos
            if img.data[y-1][x] != 2:
                var = [(y-1),x]
                img.listaParticulasCriadas.append(var)
            if img.data[y+1][x] != 2:
                var = [(y+1),x]
                img.listaParticulasCriadas.append(var)
            if img.data[y][x-1] != 2:
                var = [y,(x-1)]
                img.listaParticulasCriadas.append(var)
            if img.data[y][x+1] != 2:
                var = [y,(x+1)]
                img.listaParticulasCriadas.append(var)
            if img.data[y-1][x-1] != 2:
                var = [(y-1),(x-1)]
                img.listaParticulasCriadas.append(var)
            if img.data[y+1][x+1] != 2:
                var = [(y+1),(x+1)]
                img.listaParticulasCriadas.append(var)
            if img.data[y-1][x+1] != 2:
                var = [(y-1),(x+1)]
                img.listaParticulasCriadas.append(var)
            if img.data[y+1][x-1] != 2:
                var = [(y+1),(x-1)]
                img.listaParticulasCriadas.append(var)
                
        #Salva o valor 6 na matriz e já insere na lista de possiveis posições
        for pos in img.listaParticulasCriadas:
            y,x = pos
            img.salvaValor(y,x,6)                
        
        print img.data
        print arq.matrizMapeada
        print arq.matriz
        img.save('%s %d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
   
   
   
   
   
   
   
   
   
   
   
   
if __name__ == "__main__":
    partida = [11,15]     #(linha, coluna)
    sensor = Sensor()
    direcoes = ['norte', 'leste', 'sul', 'oeste']
    orientacao = Orientacao()
    mapeamentoDoRobo = []
    lista_direcoes_atualizada = []
    original = True
    posicaoRobo = []
    anda = Desloca()
    auto = Automatico()
    arq = Arquivo()
    img = Image(arq.numColunas, arq.numLinhas)
    encPosPos = EncontraPossiveisPosicoes()
    mapeia = Mapeia()

    #cria diretorios caso não existam
    if not os.path.exists('mapeado'):
        os.mkdir('mapeado')
    if not os.path.exists('Imagens mapeamento'):
        os.mkdir('Imagens mapeamento')
        
        
    while anda.comando != 'SAIR':
        # Esta parte é executada quando já existe um mapa do local
        if os.path.exists(arq.diretorio_img_posicoes) and len(open(arq.diretorio_img_posicoes, 'r').readlines()) > 2:
            print 'Já existe um mapa cadastrado'
            arq.leArquivoMapeado()
            img = Image(arq.numColunas, arq.numLinhas)
            #Variavel para guardar a ultima posição separando por ' ' a=1º Pos b=2ª Pos
            string = arq.ultimaPos
            a,b = string.split(' ')            
            print '\nUltima posição: LINHA:'+ a, 'COLUNA:'+ b ,'\n'
            print arq.matrizMapeada
            arq.matriz = arq.matrizMapeada
            
            sensor.percorreAngulos(partida, anda.frente, img, arq)
            
            sensor.distanciasOriginal[0] = sensor.distanciasMapeadas[0]
            sensor.distanciasOriginal[1] = sensor.distanciasMapeadas[1]
            sensor.distanciasOriginal[2] = sensor.distanciasMapeadas[2]
            sensor.distanciasOriginal[3] = sensor.distanciasMapeadas[3]
            sensor.distanciasOriginal[4] = sensor.distanciasMapeadas[4]
            #print sensor.distanciasOriginal
            
            #Guarda o escanemanto feito pelo robo e não as particulas simuladas
            if original is True:
                mapeamentoDoRobo = sensor.distanciasOriginal
                posicaoRobo = partida
                original = False
            print mapeamentoDoRobo
            print posicaoRobo
            #percorre todas posições que forem igual a 3 e 4 e compativel com as distancias obtidas depois salva 
            encPosPos.verificaTodasPosicoes(arq, direcoes, sensor, img, anda)
            #Cri particulas em torno de cada possivel possição encontrada
            mapeia.criaParticulas(img, arq, anda)
            # Esta parte é responsável por eliminar todas possiveis posições deixando apenas 1
            encPosPos.eliminaPosicoesDoVetor(arq, direcoes, sensor, img, anda)           
           
           
        # Caso não tenha mapeado o local ainda
        else:
            mapeia.realizaMapeamento(arq, img, anda, sensor, partida)

    #Salva os passos em um txt
    #anda.salvaPassos('Comandos utilizados.txt')
    
    #printa todos os comando da lista
    for i in range(len(anda.listaComandos)):
        print anda.listaComandos[i]
        
    anda.comando = 'SAIR'
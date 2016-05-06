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
        self.maxvalue = 240
        self.data = [[0 for i in range(self.coluna)] for j in range(self.linha)]
        self.listaEscaneado = []
        self.listaPosicoes = []

    # Salva arquivo com as configurações ppm
    def save(self, filename):
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
                    else:
                        print 'numero desconhecido dentro do mapa'
        self.contaPos = 0
        for i in range(len(self.listaEscaneado)):
            y,x =  self.listaEscaneado[i]
            self.data[y][x] = 3
        self.listaEscaneado = []
        
        for i in range(len(self.listaPosicoes)):
            y,x =  self.listaPosicoes[i]
            self.data[y][x] = 4
                
                
    def salvaValor(self, y, x, valor):
        self.data[y][x] = valor
        
        if self.data[y][x] == 1:
            self.listaEscaneado.append([y,x])
        
        elif self.data[y][x] == 4:
            self.listaPosicoes.append([y,x])

            

class Arquivo():
    def __init__(self):
        self.numLinhas = 0
        self.numColunas = 0
        self.matriz = None
        
    def obtemTamanhoMatriz(self):           #cria uma matriz com os valores lidos do txt
        arquivo = open('mapa01.txt', 'r')
        linha = arquivo.readline()
        arquivo.close()
        arquivo = open('mapa01.txt', 'r')
        coluna = arquivo.readlines()
        arquivo.close()
        self.numColunas = len(linha)-1
        self.numLinhas = len(coluna)        
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
    def percorreAngulos(self, partida, orient, img, arq):
        angulo = [0, 45, 90, 135, 180]
        
        if orient == 'norte':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha ------------------
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1
                        y = y - 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1
                        x = x + 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo

#-----------------------------------------------------------------------------------------
        elif orient == 'leste':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1                       # diminui linhas
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #soma linhas e colunas
                        y = y - 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #Soma colunas
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Soma linhas e colunas
                        x = x + 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Soma linhas
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
#------------------------------------------------------------------------------------
        elif orient == 'sul':
            for i in range(len(angulo)):
                y,x = partida                           # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #aumento colunas
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x + 1                       #Soma linhas e colunas
                        y = y + 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Aumenta linhas 
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #aumenta linha diminui coluna
                        x = x - 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1                       #Diminui linhas e colunas
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
#----------------------------------------------------------------------------------
        elif orient == 'oeste':
            for i in range(len(angulo)):
                y,x = partida                           # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y + 1                       #Aumento linhas
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1                       #Aumento linhas diminui colunas
                        y = y + 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        x = x - 1                       #Diminui colunas
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1                       #Diminui linhas e colunas
                        x = x - 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                        y = y - 1
                    img.salvaValor(y,x,2)               #Branco (Obstáculo)
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

   
   
   
   
if __name__ == "__main__":
    partida = [3,5]     #(linha, coluna)
    sensor = Sensor()
    orientacao = Orientacao()
    comando = None
    anda = Desloca()
    
    #Inicia arquivo do tamanho do mapa desenhado
    arq = Arquivo()
    arq.obtemTamanhoMatriz()
    img = Image(arq.numColunas, arq.numLinhas)
    #Salva previa do mapa vazio
    img.save('%s %d.ppm' %(anda.diretorio, anda.contaImg))
    anda.contaImg = anda.contaImg + 1    
    
    #verifica qual orientação
    anda.frente = orientacao.descobreOrientacao(anda.frente, comando)
    print anda.frente
    # Escaneia e salva estado inicial com primeiro mapemento
    sensor.percorreAngulos(partida, anda.frente, img, arq)
    img.save('%s %d.ppm' %(anda.diretorio, anda.contaImg))
    anda.contaImg = anda.contaImg + 1 
    
    print img.data                
    
    while comando != 'SAIR':        
        comando = raw_input('Digite "F" frente, "D" 90 direita "E" 90 esquerda, "R" re ou "sair": ')
        comando = comando.upper()
        if comando != 'SAIR':
            partida = anda.anda(partida, anda.frente, orientacao, img, comando)
            
    #Salva os passos em um txt
    anda.salvaPassos('Comandos utilizados.txt')
    
    #printa todos os comando da lista
    for i in range(len(anda.listaComandos)):
        print anda.listaComandos[i]
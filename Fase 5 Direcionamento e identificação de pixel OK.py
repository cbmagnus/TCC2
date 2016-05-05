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
        print 'Linhas: %d' %(self.numLinhas)
        print 'Colunas: %d' %(self.numColunas)        
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
        #Formatando a saida apresenta mapa lido
        for i in range(self.numLinhas):
            print (self.matriz[i][:])
    
    
class Sensor():       
    def percorreAngulos(self, partida, orient):
        contaImg = 0
        arq = Arquivo()
        arq.obtemTamanhoMatriz()
        img = Image(arq.numColunas, arq.numLinhas)
        angulo = [0, 45, 90, 135, 180]
        
        if orient == 'norte':
            for i in range(len(angulo)):
                x, y = partida      # x = coluna  y= linha ------------------
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x - 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x - 1
                        y = y - 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y - 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y - 1
                        x = x + 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x + 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
            x, y = partida     # x = coluna  y= linha
#-----------------------------------------------------------------------------------------
        elif orient == 'leste':
            for i in range(len(angulo)):
                x, y = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y - 1                    # diminui linhas
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x + 1                    #soma linhas e colunas
                        y = y - 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x + 1                    #Soma colunas
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y + 1                    #Soma linhas e colunas
                        x = x + 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y + 1                    #Soma linhas
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
            x, y = partida     # x = coluna  y= linha
#------------------------------------------------------------------------------------
        elif orient == 'sul':
            for i in range(len(angulo)):
                x, y = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x + 1                    #aumento colunas
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x + 1                    #Soma linhas e colunas
                        y = y + 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y + 1                    #Aumenta linhas 
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y + 1                    #aumenta linha diminui coluna
                        x = x - 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x - 1                    #Diminui linhas e colunas
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
            x, y = partida     # x = coluna  y= linha
#----------------------------------------------------------------------------------
        elif orient == 'oeste':
            for i in range(len(angulo)):
                x, y = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y + 1                    #Aumento linhas
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 45:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x - 1                    #Aumento linhas diminui colunas
                        y = y + 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 90:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        x = x - 1                    #Diminui colunas
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 135:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y - 1                    #Diminui linhas e colunas
                        x = x - 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
                elif angulo[i] == 180:
                    while arq.matriz[y][x] != '*':
                        img.set_pixel(y,x,[0,220,0]) #Verde (Caminho do raio)
                        y = y - 1
                    img.set_pixel(y,x,[220,220,220]) #Branco (Obstáculo)
            x, y = partida     # x = coluna  y= linha
#-----------------------------------------------------------------------------------
            
        posicoes = [partida]
        for i in range(len(posicoes)):
            img.set_pixel(y,x,[0,0,220])   #Azul (Localização do robô)
       
        img.save('Mapa Walle %d.ppm' %(contaImg))
        contaImg = contaImg + 1

class Orientacao():
    def descobreOrientacao(self, orientac, direc):
        orientacao = orientac
        direcao = direc
        pos = orientac
        
        if orientacao == 'norte' and (direcao == 'D' or direcao == 'd'):
            pos = 'leste'
            return pos
        if orientacao == 'norte' and (direcao == 'E' or direcao == 'e'):
            pos = 'oeste'
            return pos
        if orientacao == 'leste' and (direcao == 'D' or direcao == 'd'):
            pos = 'sul'
            return pos
        if orientacao == 'leste' and (direcao == 'E' or direcao == 'e'):
            pos = 'norte'
            return pos
        if orientacao == 'sul' and (direcao == 'D' or direcao == 'd'):
            pos = 'oeste'
            return pos
        if orientacao == 'sul' and (direcao == 'E' or direcao == 'e'):
            pos = 'leste'
            return pos
        if orientacao == 'oeste' and (direcao == 'D' or direcao == 'd'):
            pos = 'norte'
            return pos
        if orientacao == 'oeste' and (direcao == 'E' or direcao == 'e'):
            pos = 'sul'
            return pos
        
        else:
            return pos
    
if __name__ == "__main__":
    partida = (4,4)     #(coluna, linha)
    sensor = Sensor()
    orientacao = Orientacao()
    frente = 'norte'
    
    comando = raw_input('Digite "F" frente, "D" 90º direita "E" 90º esquerda, "R" ré: ')
    print comando
    frente = orientacao.descobreOrientacao(frente, comando)
    print frente
    
    # Escaneia
    sensor.percorreAngulos(partida, frente)
    
    
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:37:49 2016

@author: Darlan.Magnus
"""

class Image ():
    # Inicia a classe
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maxvalue = 255
        self.data = [[[0,0,0] for i in range(width)] for j in range(height)]

    # determina a cor do pixel selecionado
    def set_pixel(self, y, x, color):
        m = max(color)
        if m > self.maxvalue:
            self.maxvalue = m
        self.data[y][x] = color

    # Salva arquivo com as configurações ppm
    def save(self, filename):
        with open(filename,'w') as f:
            f.write("P3\n%d %d\n%d\n"%(self.width, self.height, self.maxvalue))
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
            

def bresenham(start, end):
    # condições iniciais
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1 
    # determina quanto a linha é inclinada
    is_steep = abs(dy) > abs(dx)
    # inverte linha
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # recalcula diferenças
    dx = x2 - x1
    dy = y2 - y1
 
    # calcula erro
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # cria caminho entre inicio e fim
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    
    # transforma cordenadas em pontos por onde passa a linha
    if swapped:
        points.reverse()    
    return points
    
    
if __name__ == "__main__":
    partida = (3,2)     #(coluna, linha)
    chegada = (17,16)   #(coluna, linha)
    arq = Arquivo()
    arq.obtemTamanhoMatriz()
    img = Image(arq.numColunas, arq.numLinhas)
    coordenadas = bresenham(partida, chegada)
    cont = 0
    #print coordenadas
    
    for y in range(arq.numLinhas):
        for x in range(arq.numColunas):
            if arq.matriz[y][x] == ' ':     # (linha, coluna)
                img.set_pixel(y,x,[0,0,0])
            if arq.matriz[y][x] == '*':
                img.set_pixel(y,x,[255,255,255])
            if cont < len(coordenadas) and (x, y) == coordenadas[cont] and arq.matriz[y][x] == '*':
                img.set_pixel(y,x,[255,255,255])
                cont = 0
            if cont < len(coordenadas) and (x, y) == coordenadas[cont] and arq.matriz[y][x] == ' ':
                img.set_pixel(y,x,[200,100,100])
                cont = cont + 1
    
    img.save('Mapa Walle.ppm')
    img.save('Mapa Walle.txt')
    
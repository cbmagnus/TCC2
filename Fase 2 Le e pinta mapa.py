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
        #print self.matriz
        # Cria uma matriz de zeros com o numero de LINHAS lidos
        for i in range(self.numLinhas):
            self.matriz[i] = [0]*self.numColunas
        #print (self.matriz)
        
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
            

# Se for verdade salva arquivo ppm e define o tamanho da imagem
if __name__ == "__main__":
    arq = Arquivo()
    arq.obtemTamanhoMatriz()
    
    img = Image(arq.numColunas, arq.numLinhas)
    for y in range(arq.numLinhas):
        for x in range(arq.numColunas):
            if arq.matriz[y][x] == '*':
                img.set_pixel(y,x,[255,255,255])
            else:
                img.set_pixel(y,x,[0,0,0])
    img.save('Mapa Walle.ppm')
    img.save('Mapa Walle.txt')
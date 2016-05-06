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
            

class Bresenham():
    def bresenham(self, start, end):
        # condições iniciais
        x1, y1 = start  #coluna, linha
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
    
    
class Sensor():       
    def percorreAngulos(self, partida):
        arq = Arquivo()
        arq.obtemTamanhoMatriz()
        img = Image(arq.numColunas, arq.numLinhas)
        angulo = [0, 45, 90, 135, 180]
        for i in range(len(angulo)):
            x, y = partida      # x = coluna  y= linha
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
        img.set_pixel(y,x,[0,0,220])   #Azul (Localização do robô)
        
        img.save('Mapa Walle.ppm')

    
if __name__ == "__main__":
    partida = (3,3)     #(coluna, linha)
    chegada = (17,7)   #(coluna, linha)
    arq = Arquivo()
    arq.obtemTamanhoMatriz()
    img = Image(arq.numColunas, arq.numLinhas)
    """bre = Bresenham()
    #coordenadas = bre.bresenham(partida, chegada)
    # auxiliar para parar em paredes    
    cont = 0
    
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
   """
   #Cria uma imagem .ppm e um .txt
    #img.save('Mapa Walle.ppm')
    img.save('Mapa Walle.txt')

    sensor = Sensor()
    sensor.percorreAngulos(partida) 
        
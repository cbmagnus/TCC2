# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:37:49 2016

@author: Darlan.Magnus
"""
class Image (object):

    # Inicia a classe
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maxvalue = 255
        self.data = [[[0,0,0] for i in range(width)] for j in range(height)]

    # determina a cor do pixel selecionado
    def set_pixel(self, x, y, color):
        m = max(color)
        if m > self.maxvalue:
            self.maxvalue = m
        self.data[y][x] = color

    # Modifica as cores
    #def draw_filled_rect(self, x, y, w, h, color):
     #   for j in range(y,y+w):
      #      line = self.data[j]
       #     for i in range(x,x+w):
        #        line[i] = color

    # Salva arquivo com as configurações ppm
    def save(self, filename):
        with open(filename,'w') as f:
            f.write("P3\n%d %d\n%d\n"%(self.width, self.height, self.maxvalue))
            for line in self.data:
                for (r,g,b) in line:
                    f.write("%d %d %d\n" % (r,g,b))





# Se for verdade salva arquivo ppm e define o tamanho da imagem
if __name__ == "__main__":
    tamX = 21
    tamY = 21
    img = Image(tamY,tamX)
    for y in range(tamY):
        for x in range(tamX):
            img.set_pixel(x,y,[0,0,0])
            if x == 0:
                img.set_pixel(x,y,[255,255,255])
            if y == 0:
                img.set_pixel(x,y,[255,255,255])
            if x == (tamX-1):
                img.set_pixel(x,y,[255,255,255])
            if y == (tamY-1):
                img.set_pixel(x,y,[255,255,255])
            if (x == tamX/2) and (y < tamY/2):
                img.set_pixel(x,y,[255,255,255])
    img.save('Mapa Walle.ppm')
    img.save('Mapa Walle.txt')

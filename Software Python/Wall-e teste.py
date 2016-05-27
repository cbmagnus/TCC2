# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:37:49 2016

@author: Darlan.Magnus
"""

"""
Lista de comandos com o arduino
ANGULO0             # Gira o servo para o angulo 0º
ANGULO45            # Gira o servo para o angulo 45º
ANGULO90            # Gira o servo para o angulo 90º
ANGULO135           # Gira o servo para o angulo 135º
ANGULO180           # Gira o servo para o angulo 180º
F                   # Anda para frente
D                   # Anda para direita
E                   # Anda para esquerda
R                   # Anda para tras

"""

import os.path
import operator
import serial
import time

porta = "COM5"
velocidade = 9600

try:
    print 'Conectando'
    arduino = serial.Serial(porta, velocidade)
    time.sleep(1.5)
except:
    print 'Aguarde, inicializando porta...'
    arduino.close()
    time.sleep(1.5)
    arduino.open()
    time.sleep(1.5)

print '\nPorta = ' + arduino.portstr + '\n'      # Mostra a porta em uso
time.sleep(0.5)

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
        self.sair = False
        self.listaParedes = []
        self.listaParedeTemporaria = []
        self.listaParedePermanente = []

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
        print self.listaParedes
        print self.listaParedeTemporaria
        for i in range(len(self.listaParedeTemporaria)):
            y,x = self.listaParedeTemporaria[i]
            if self.data[y][x] == 0 or self.data[y][x] == 3:
                self.data[y][x] = 2

        for i in self.listaParedes:
            if i in self.listaParedeTemporaria:
                self.listaParedePermanente.append(i)
        print self.listaParedePermanente

        for i in range(len(self.listaEscaneado)):
            y,x =  self.listaEscaneado[i]
            self.data[y][x] = 3
        self.listaEscaneado = []
        
        for i in range(len(self.listaPosicoes)):
            y,x =  self.listaPosicoes[i]
            self.data[y][x] = 4
            
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
                        f.write("%d %d %d\n" % (220,0,220))       #Pinta de Laranja  (Posições das particulas)
                    else:
                        print 'numero desconhecido dentro do mapa'
                        
        for i in range(len(self.listaParedeTemporaria)):
            y,x = self.listaParedeTemporaria[i]
            self.data[y][x] = 0

                
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
        self.diretorio = 'Imagens_mapeamento/Mapa'
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
        self.lista_direcoes_atualizada = []
        self.recebido = ''
        self.numQuadrados = 0
    
    def escreveNoArduino(self, comand, sensor):
        arduino.flush()
        arduino.flushInput()
        arduino.flushOutput()
        self.numQuadrados = 0
        self.recebido = ''
        # Manda pro arduino o comando
        arduino.write(comand)
        time.sleep(0.1)
        while len(self.recebido) != 6:          #Enquanto diferente de FIMM\n = 6 caracteres
            self.recebido = arduino.readline()
            if len(self.recebido) == 9:         #Se igual a PAREDEP\n = 9 caracteres espera 2 milesegundos
                print 'Parede...'
                time.sleep(0.1)
            elif len(self.recebido) == 8 or len(self.recebido) == 0:    #Se igual INICIO\n = 8 aguarda
                print 'aguardando resposta...'
                time.sleep(0.1)
            elif len(self.recebido) >= 3 and len(self.recebido) < 6:       # Se receber um numero = 42\n = 4 por exemplo 
                self.numQuadrados = round(float('%.1f' % ( float(self.recebido)/10)))
                
    
    def percorreAngulos(self, partida, orient, img, arq, sensor):
        self.dist0Graus = -1
        self.dist45Graus = -1
        self.dist90Graus = -1
        self.dist135Graus = -1
        self.dist180Graus = -1

        angulo = [0, 45, 90, 135, 180]
        arduino.flush()
        arduino.flushInput()
        arduino.flushOutput()
        if orient == 'norte':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha ------------------
                if angulo[i] == 0:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO0', sensor)
                        # Divide por 10 a distancia encontrada sendo que cada quadrado tem 10cm Arredonda pra mais ou pra menos o numero de quadrados a ser pintados
                        self.numQuadrados = self.numQuadrados - 1 # Pra cada lado o robo tem +- 10cm por isso diminuo 1 da leitura
                        print self.numQuadrados
                        if self.numQuadrados == 0:  #Se for 0 assume a posição ao lado para dizer que é um obstaculo
                            x = x - 1
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1
                            self.dist0Graus = self.dist0Graus + 1         #conta numero de casas livres à 0º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        img.listaParedes.append([y,x])
                        self.distanciasMapeadas[0] = self.dist0Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1
                            self.dist0Graus = self.dist0Graus + 1         #conta numero de casas livres à 0º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO45', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1
                            y = y - 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1
                            y = y - 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO90', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1
                            self.dist90Graus = self.dist90Graus + 1       #conta numero de casas livres à 90º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)
                        img.listaParedes.append([y,x])
                        self.distanciasMapeadas[2] = self.dist90Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1
                            self.dist90Graus = self.dist90Graus + 1       #conta numero de casas livres à 90º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO135', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1
                            x = x + 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1
                            x = x + 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO180', sensor)
                        print self.numQuadrados
                        if self.numQuadrados == 0:
                            x = x + 1
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)
                        img.listaParedes.append([y,x])
                        self.distanciasMapeadas[4] = self.dist180Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
            print self.distanciasMapeadas
            y,x = img.listaParedes[1]
            a,b = img.listaParedes[0]
            c,d = img.listaParedes[2]
            print img.listaParedes
            while x != b:
                img.listaParedeTemporaria.append([y,x])
                x = x -1
            y,x = img.listaParedes[1]
            while x != d:
                img.listaParedeTemporaria.append([y,x])
                x = x +1
            y,x = img.listaParedes[1]
            
            while a != y:
                img.listaParedeTemporaria.append([a,b])
                a = a -1
            while c != y:
                img.listaParedeTemporaria.append([c,d])
                c = c -1
            img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
            anda.contaImg = anda.contaImg + 1
            img.listaParedes = []
            print img.listaParedeTemporaria
            print img.listaParedePermanente

#-----------------------------------------------------------------------------------------
        elif orient == 'leste':
            for i in range(len(angulo)):
                y,x = partida      # x = coluna  y= linha
                if angulo[i] == 0:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO0', sensor)
                        self.numQuadrados = self.numQuadrados - 1 # Pra cada lado o robo tem +- 10cm por isso diminuo 1 da leitura
                        print self.numQuadrados
                        if self.numQuadrados == 0:
                            y = y - 1
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1                       # diminui linhas
                            self.dist0Graus = self.dist0Graus + 1
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[0] = self.dist0Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1                       # diminui linhas
                            self.dist0Graus = self.dist0Graus + 1          #conta numero de casas livres à 0º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO45', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #soma linhas e colunas
                            y = y - 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #soma linhas e colunas
                            y = y - 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO90', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #Soma colunas
                            self.dist90Graus = self.dist90Graus + 1       #conta numero de casas livres à 90º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[2] = self.dist90Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #Soma colunas
                            self.dist90Graus = self.dist90Graus + 1        #conta numero de casas livres à 90º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO135', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1
                            x = x + 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #Soma linhas e colunas
                            x = x + 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO180', sensor)
                        self.numQuadrados = self.numQuadrados - 1 # Pra cada lado o robo tem +- 10cm por isso diminuo 1 da leitura
                        print self.numQuadrados
                        if self.numQuadrados == 0:
                            y = y + 1
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #Soma linhas
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[4] = self.dist180Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #Soma linhas
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
            print self.distanciasMapeadas
#------------------------------------------------------------------------------------
        elif orient == 'sul':
            for i in range(len(angulo)):
                y,x = partida                           # x = coluna  y= linha
                if angulo[i] == 0:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO0', sensor)
                        self.numQuadrados = self.numQuadrados - 1 # Pra cada lado o robo tem +- 10cm por isso diminuo 1 da leitura
                        print self.numQuadrados
                        if self.numQuadrados == 0:
                            x = x + 1  
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #aumento colunas
                            self.dist0Graus = self.dist0Graus + 1
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[0] = self.dist0Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #aumento colunas
                            self.dist0Graus = self.dist0Graus + 1          #conta numero de casas livres à 0º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO45', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #Soma linhas e colunas
                            y = y + 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x + 1                       #Soma linhas e colunas
                            y = y + 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO90', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #Aumenta linhas 
                            self.dist90Graus = self.dist90Graus + 1       #conta numero de casas livres à 90º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[2] = self.dist90Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #Aumenta linhas 
                            self.dist90Graus = self.dist90Graus + 1        #conta numero de casas livres à 90º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO135', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #aumenta linha diminui coluna
                            x = x - 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #aumenta linha diminui coluna
                            x = x - 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO180', sensor)
                        self.numQuadrados = self.numQuadrados - 1 # Pra cada lado o robo tem +- 10cm por isso diminuo 1 da leitura
                        print self.numQuadrados
                        if self.numQuadrados == 0:
                            x = x - 1  
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1                       #Diminui linhas e colunas
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[4] = self.dist180Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1                       #Diminui linhas e colunas
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
            print self.distanciasMapeadas
#----------------------------------------------------------------------------------
        elif orient == 'oeste':
            for i in range(len(angulo)):
                y,x = partida                           # x = coluna  y= linha
                if angulo[i] == 0:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO0', sensor)
                        self.numQuadrados = self.numQuadrados - 1 # Pra cada lado o robo tem +- 10cm por isso diminuo 1 da leitura
                        print self.numQuadrados
                        if self.numQuadrados == 0:
                            y = y + 1
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #Aumento linhas
                            self.dist0Graus = self.dist0Graus + 1
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[0] = self.dist0Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y + 1                       #Aumento linhas
                            self.dist0Graus = self.dist0Graus + 1          #conta numero de casas livres à 0º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[0] = self.dist0Graus
                elif angulo[i] == 45:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO45', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1                       #Aumento linhas diminui colunas
                            y = y + 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1                       #Aumento linhas diminui colunas
                            y = y + 1
                            self.dist45Graus = self.dist45Graus + 1        #conta numero de casas livres à 45º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[1] = self.dist45Graus
                elif angulo[i] == 90:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO90', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1                       #Diminui colunas
                            self.dist90Graus = self.dist90Graus + 1       #conta numero de casas livres à 90º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[2] = self.dist90Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            x = x - 1                       #Diminui colunas
                            self.dist90Graus = self.dist90Graus + 1        #conta numero de casas livres à 90º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[2] = self.dist90Graus
                elif angulo[i] == 135:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO135', sensor)
                        print self.numQuadrados
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1                       #Diminui linhas e colunas
                            x = x - 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1                       #Diminui linhas e colunas
                            x = x - 1
                            self.dist135Graus = self.dist135Graus + 1        #conta numero de casas livres à 135º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[3] = self.dist135Graus
                elif angulo[i] == 180:
                    if anda.original == True:
                        sensor.escreveNoArduino('ANGULO180', sensor)
                        self.numQuadrados = self.numQuadrados - 1 # Pra cada lado o robo tem +- 10cm por isso diminuo 1 da leitura
                        print self.numQuadrados
                        if self.numQuadrados == 0:
                            y = y - 1
                        while self.numQuadrados >= 0:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                            self.numQuadrados = self.numQuadrados - 1
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[4] = self.dist180Graus
                        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
                        anda.contaImg = anda.contaImg + 1
                    else:
                        while arq.matriz[y][x] != '*' and arq.matrizMapeada[y][x] != 2:
                            img.salvaValor(y,x,1)           #Verde (Caminho do raio)
                            y = y - 1
                            self.dist180Graus = self.dist180Graus + 1        #conta numero de casas livres à 180º
                        img.salvaValor(y,x,2)               #Branco (Obstáculo)
                        self.distanciasMapeadas[4] = self.dist180Graus
            y,x = partida                               # x = coluna  y= linha
            img.salvaValor(y,x,4)                       # Azul posição do robo
            print self.distanciasMapeadas
            
        arduino.write('ANGULO90')
        time.sleep(0.6)
        arduino.flushInput
        arduino.flushOutput
        time.sleep(0.2)
        #anda.original = False
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
        self.original = True
        
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
                    arduino.write('F')
                    time.sleep(1)
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    comando='@!'
                    y = (y+1)
                    self.destino = [y,x]
                    partida = self.destino
                    sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
                
            elif self.frente == 'leste':
                x = (x+1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    arduino.write('F')
                    time.sleep(1)
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    x = (x-1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                    sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
                
            elif self.frente == 'sul':
                y = (y+1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    arduino.write('F')
                    time.sleep(1)
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    y = (y-1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                    sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
                
            elif self.frente == 'oeste':
                x = (x-1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    arduino.write('F')
                    time.sleep(1)
                    partida = self.destino
                elif img.data[y][x] == 2:
                    print 'Nao e permitido avancar! Tem uma parede ai!'
                    x = (x+1)
                    self.destino = [y,x]
                    comando='@!'
                    partida = self.destino
                    sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
                
            if comando != '@!':
                # Escaneia a orientação e salva imagem ppm
                print partida
                arq.ultimaPos = partida
                sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
                img.save('%s%d.ppm' %(diretorio, self.contaImg))
                self.contaImg = self.contaImg + 1 
        
        elif comando == 'R':
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            if self.frente == 'norte':
                y = (y+1)
                self.destino = [y,x]
                if img.data[y][x] != 2:
                    arduino.write('R')
                    time.sleep(1)
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
                    arduino.write('R')
                    time.sleep(1)
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
                    arduino.write('R')
                    time.sleep(1)
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
                    arduino.write('R')
                    time.sleep(1)
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
                sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
                img.save('%s%d.ppm' %(diretorio, self.contaImg))
                self.contaImg = self.contaImg + 1
            
        elif comando == 'D':
            arduino.write('D')
            time.sleep(1)
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            # Escaneia a orientação e salva imagem ppm
            sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
            img.save('%s%d.ppm' %(diretorio, self.contaImg))
            self.contaImg = self.contaImg + 1
        
        elif comando == 'E':
            arduino.write('E')
            time.sleep(1)
            self.frente = orientacao.descobreOrientacao(self.frente, comando)
            print self.frente
            # Escaneia a orientação e salva imagem ppm
            sensor.percorreAngulos(partida, self.frente, img, arq, sensor)
            img.save('%s%d.ppm' %(diretorio, self.contaImg))
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
        cont = 3
        # Enquanto eu não encontrar parede vou para frente
        while sensor.distanciasMapeadas[2] > 1:               # 90º graus
            partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
            img.listaParedeTemporaria = []
        partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
        chegada.append(partida)
        dirPartida = anda.frente
        y,x = partida
        while cont > 0:
            y = y - 1
            chegada.append([y,x])
            cont = cont - 1
        y,x = partida
        while cont < 3:
            y = y + 1
            chegada.append([y,x])
            cont = cont + 1
        partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
        
        print partida
        print chegada
        # Segue o curso até encontrar uma posição conhecida e mesma direção
        while not(partida in chegada) and anda.frente == dirPartida:
            #Enquanto angulo 0 for entre 1 e 3 e chegada != partida segue loop
            while sensor.distanciasMapeadas[0] > 0 and sensor.distanciasMapeadas[0] < 4 and not(partida in chegada):
                partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                
                if sensor.distanciasMapeadas[0] > 3:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'E', arq.diretorio)
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'F', arq.diretorio)
                
                elif sensor.distanciasMapeadas[0] < 3 and sensor.distanciasMapeadas[2] < 3 and sensor.distanciasMapeadas[4] < 3:
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
                    
                elif sensor.distanciasMapeadas[2] < 2:        # 90º graus
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
                    
                elif sensor.distanciasMapeadas[0] == 0:
                    sensor.escreveNoArduino('ACERTAPOS', sensor)
            
            sensor.percorreAngulos(partida, anda.frente, img, arq, sensor)
                
                    
        anda.original = True
        return 'SAIR'
        arduino.close()
        print 'Mapeamento realizado OK'
   
   
   
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
                        sensor.percorreAngulos([y,x], direcao, img, arq, sensor)
                        print sensor.distanciasOriginal
                        print sensor.distanciasMapeadas
                        
                        # Se valores de mapeamento forem igual a do robô é uma possivel posição identificada com numero 5
                        if all(map(operator.eq, sensor.distanciasOriginal, sensor.distanciasMapeadas)):
                            img.salvaValor(y,x,5)
                            img.lista_direcoes.append(direcao)
                            img.save('%s%d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
                            anda.contaImg = anda.contaImg + 1
                        else:
                            print 'Não são compativeis'
                else:
                    print 'Não é possivel estar aqui. Possivel parede!'
        img.save('%s%d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
        print '\n',img.lista_pos_localizacao
        print img.lista_direcoes,'\n'
        # Se não tiver uma outra possivel posição termina o programa
        if len(img.lista_pos_localizacao) == 1:
            anda.comando = 'SAIR'
            img.sair = True
            print '\nSua posição é' + str(img.lista_pos_localizacao[0]) + '\n'
        
        
    def eliminaPosicoesDoVetor(self, arq, direcoes, sensor, img, anda, partida, mapeamentoDoRobo):
        # Gira 360º mapeando cada direção para tentar achar sua localização
        # Limpa a lista de escaneamento
        img.lista_compara_distancias = []
        sensor.distanciasOriginal = [0,0,0,0,0] 
        img.lista_direcoes = []
        listaPosicoesTEMP = []
        
        print mapeamentoDoRobo
        print img.lista_pos_localizacao
        
        #Gira todos 360º e compara com a leitura feita pelo robo
        for posicao in img.lista_pos_localizacao:
            for direc in direcoes:
                print posicao
                print direc
                y,x = posicao
                sensor.percorreAngulos([y,x], direc, img, arq, sensor)
                print sensor.distanciasMapeadas
                #Se o mapeamento do robo for compativel com alguma particula em 360º salva se não volta a ser mapeada
                if all(map(operator.eq, mapeamentoDoRobo, sensor.distanciasMapeadas)):
                    print 'SÃO compativeis'
                    img.lista_direcoes.append(direc)
                    listaPosicoesTEMP.append(posicao)
                else:
                    print 'NÃO são compativeis'
            print 'Fim da posição -> ', posicao
            print listaPosicoesTEMP
            print img.lista_direcoes
            
        img.listaParticulasCriadas = []
        #Pinta mapa com as cores restantes no caso apenas possiveis posições
        for a in img.lista_pos_localizacao:
            y,x = a
            if a in listaPosicoesTEMP:
                img.data[y][x] = 5
            else:
                img.data[y][x] = 4

        #Zera lista de particulas criadas
        if len(listaPosicoesTEMP) == 1:
            anda.comando = 'SAIR'
            img.sair = True
            img.lista_pos_localizacao = listaPosicoesTEMP
            print '\nSua posição é' + str(listaPosicoesTEMP[0]) + '\n'
            img.save('%s%d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
            anda.contaImg = anda.contaImg + 1
        
        elif len(listaPosicoesTEMP) > 1:
            img.lista_pos_localizacao = listaPosicoesTEMP
        
        else:
            print 'Erro Não sobrou possições possíveis no mapa'
   
   
class Mapeia():
    def realizaMapeamento(self, arq, img, anda, sensor, partida):
        arq.obtemTamanhoMatriz()
        img = Image(arq.numColunas, arq.numLinhas)
        #Salva previa do mapa vazio
        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
        print anda.comando
        #verifica qual orientação
        anda.frente = orientacao.descobreOrientacao(anda.frente, anda.comando)
        # Copia mapa teorico para matrizMapeada para não dar erro de verificação de matriz nula quando compara em percorre angulos
        arq.matrizMapeada = arq.matriz
        # Escaneia e salva estado inicial com primeiro mapemento
        sensor.percorreAngulos(partida, anda.frente, img, arq, sensor)
        img.save('%s%d.ppm' %(arq.diretorio, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
        
        anda.original = True
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
       
        img.save('%s%d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
        anda.contaImg = anda.contaImg + 1
   
   
   
   
   
   
   
   
   
   
   
   
if __name__ == "__main__":
    partida = [30,30]     #(linha, coluna)
    direcaoRobo = 'norte'
    sensor = Sensor()
    direcoes = ['norte', 'leste', 'sul', 'oeste']
    orientacao = Orientacao()
    mapeamentoDoRobo = []
    anda = Desloca()
    auto = Automatico()
    arq = Arquivo()
    img = Image(arq.numColunas, arq.numLinhas)
    encPosPos = EncontraPossiveisPosicoes()
    mapeia = Mapeia()
    primVez = 0
    cont = 0

    #cria diretorios caso não existam
    if not os.path.exists('mapeado'):
        os.mkdir('mapeado')
    if not os.path.exists('Imagens_mapeamento'):
        os.mkdir('Imagens_mapeamento')
        
        
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

            while anda.comando != 'SAIR':
                #Inicia o escaneamento do robo real
                sensor.percorreAngulos(partida, direcaoRobo, img, arq, sensor)
                sensor.distanciasOriginal[0] = sensor.distanciasMapeadas[0]
                sensor.distanciasOriginal[1] = sensor.distanciasMapeadas[1]
                sensor.distanciasOriginal[2] = sensor.distanciasMapeadas[2]
                sensor.distanciasOriginal[3] = sensor.distanciasMapeadas[3]
                sensor.distanciasOriginal[4] = sensor.distanciasMapeadas[4]
                mapeamentoDoRobo = sensor.distanciasOriginal
                print mapeamentoDoRobo
                
                if primVez == 0:
                    #percorre todas posições e em todas as direções que forem igual a 3 e 4 e compativel com as distancias obtidas pelo robo depois salva 
                    encPosPos.verificaTodasPosicoes(arq, direcoes, sensor, img, anda)
                    primVez = primVez + 1
                else:
                    # Esta parte é responsável por eliminar todas possiveis posições deixando apenas 1
                    encPosPos.eliminaPosicoesDoVetor(arq, direcoes, sensor, img, anda, partida, mapeamentoDoRobo)
                    img.save('%s%d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
                    anda.contaImg = anda.contaImg + 1
                    if img.sair == True:
                        break
                    
                    print '------------------------------------------------------'
                    print cont
                    print direcaoRobo
                    print img.lista_pos_localizacao
                    print img.lista_direcoes
                    print mapeamentoDoRobo
                    
                    # Se já tiver virado 360º e ainda tiver mais de 1 possível posição
                    if cont >= 4 and primVez == 1:
                        listaLocalTemporaria = []
                        listaDirecaoTemporaria = []
                        if mapeamentoDoRobo[2] != 0:
                            #Anda robo para frente e na sequencia todas particulas tmbm
                            partida = anda.anda(partida, direcaoRobo, orientacao, img, 'F', arq.diretorio)
                            direcaoRobo = anda.frente
                            for indice, pos in enumerate(img.lista_pos_localizacao):
                                temp = anda.anda(pos, img.lista_direcoes[indice], orientacao, img, 'F', arq.diretorio)
                                print temp
                                listaLocalTemporaria.append(temp)
                            print img.lista_pos_localizacao
                            img.lista_pos_localizacao = listaLocalTemporaria
                            print img.lista_pos_localizacao
                            print img.lista_direcoes
                            img.save('%s%d.ppm' %(arq.diretorio_img_posicoes, anda.contaImg))
                            anda.contaImg = anda.contaImg + 1
                        
                        # Se tiver parede a frente vira para o lado contrário
                        elif mapeamentoDoRobo[2] == 0:
                            #Viro o robo para a direita e na sequencia todas particulas tmbm
                            partida = anda.anda(partida, direcaoRobo, orientacao, img, 'D', arq.diretorio)
                            direcaoRobo = anda.frente
                            for indice, pos in enumerate(img.lista_pos_localizacao):
                                temp = anda.anda(pos, img.lista_direcoes[indice], orientacao, img, 'D', arq.diretorio)
                                print temp
                                listaLocalTemporaria.append(temp)
                                listaDirecaoTemporaria.append(anda.frente)
                            img.lista_pos_localizacao = listaLocalTemporaria
                            img.lista_direcoes = listaDirecaoTemporaria
                            
                            
                    
                #Cri particulas em torno de cada possivel possição encontrada
                mapeia.criaParticulas(img, arq, anda)
                
                if cont < 4:
                    #Vira para direita para compatibilizar com particulas
                    partida = anda.anda(partida, anda.frente, orientacao, img, 'D', arq.diretorio)
                    direcaoRobo = anda.frente
                    cont = cont + 1
           
           
        # Caso não tenha mapeado o local ainda
        else:
            anda.original = True
            mapeia.realizaMapeamento(arq, img, anda, sensor, partida)

    #Salva os passos em um txt
    #anda.salvaPassos('Comandos utilizados.txt')
    
    #printa todos os comando da lista
    for i in range(len(anda.listaComandos)):
        print anda.listaComandos[i]
        
    anda.comando = 'SAIR'
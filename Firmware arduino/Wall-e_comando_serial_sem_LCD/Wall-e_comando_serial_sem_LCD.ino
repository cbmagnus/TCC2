// DECLARAÇÃO DAS FUNÇÕES DO TIPO VOID
void frente();
void direita();
void esquerda();
void re();
void pare();
void pensa();
void sonar();

// DECLARAÇÃO VARIÁVEL GLOBAL
int distancia;
int distSegura = 20;
char comando = '0';
int tempo = 1000;

// INFRA VERMELHO
int infraFrente = 0;        //analogico 0

// VELOCIDADE DOS MOTORES
int velMax = 255;      //entre 0 parado e 255 maximo
int velMin = 0;

// PINOS DOS MOTORES
int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;

// POSICIONAMENTO SERVO ENTRE 0 E 180
int servoCentro = 90;
int servoDireita = 0;
int servoEsquerda = 175;

// SENSOR ULTRASSONICO
int trig = 11;          // pino 11 digital
int echo = 12;          // pino 12 digital

#include <Wire.h>
#include <LCD.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

Servo servo1;         //Criando objeto servo da frente

// DECLARANDO PINOS I2C
LiquidCrystal_I2C lcd(0x3F,2,1,0,4,5,6,7,3, POSITIVE); // 3F (hexa) = 63 decimal

void setup() {
  Serial.begin(9600);
  Serial.flush();
  
  // PINOS DOS MOTORES SAIDA
  pinMode(IN1, OUTPUT);     // LADO DIREITO 
  pinMode(IN2, OUTPUT);     // LADO DIREITO
  pinMode(IN3, OUTPUT);     // LADO ESQUERDO
  pinMode(IN4, OUTPUT);     // LADO ESQUERDO
  
  // INICIA PINO SERVO 10 DIGITAL
  servo1.attach(10);      // definido pino 10 digital
  servo1.write(servoCentro);
  
  //INICIA PINO SONAR
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);

  // INICIANDO PINOS DO SENSOR INFRAVERMELHO
  pinMode(infraFrente, INPUT);
  
  //INICIA DISPLAY
  lcd.begin(16,2);    //16 colunas por 2 linhas
  lcd.setBacklight(HIGH);
  lcd.clear();                  // Limpa display 
  lcd.home();                   // Manda o cursor para a posição "zero" 
  lcd.print("     WALL-E     ");// Escreve
  lcd.setCursor(0,1);  // posiciona o cursor na linha de baixo.
  lcd.print("   TCC Darlan   ");
  delay(1000);
}



void loop() {

  if (Serial.available()) {
    comando = Serial.read();

    if(comando == 'F'){
      frente();
      delay(tempo);
    }

    else if(comando == 'R'){
      re();
      delay(tempo);
    }

    else if(comando == 'D'){
      direita();
      delay(tempo);
    }

    else if(comando == 'E'){
      esquerda();
      delay(tempo);
    }

    else if(comando == 'P'){
      pensa();
    }

    else{
      pare();
    }

    pare();
    delay(200);
  }
  else{
    pare();
  }
  
}

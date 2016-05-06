
#include <Wire.h>
#include <LCD.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>
#include <SoftwareSerial.h>

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
int distSegura = 25;

// INFRA VERMELHO
int infraDireito = 0;        //analogico 0
int infraEsquerdo = 1;       //analogico 1

// VELOCIDADE DOS MOTORES
int velMax = 255;      //entre 0 parado e 255 maximo
int velMin = 0;

// POSICIONAMENTO SERVO ENTRE 0 E 180
int servoCentro = 90;
int servoDireita = 10;
int servoEsquerda = 170;

// SENSOR ULTRASSONICO
int trig = 11;          // pino 11 digital
int echo = 12;          // pino 12 digital

// BLUETHOOT
char dados = '0';
const int rxpin = 2;
const int txpin = 4;
SoftwareSerial bluetooth(rxpin, txpin);


Servo servo1;         //Criando objeto servo da frente

// DECLARANDO PINOS I2C
LiquidCrystal_I2C lcd(0x3F,2,1,0,4,5,6,7,3, POSITIVE); // 3F (hexa) = 63 decimal

void setup() {
  bluetooth.begin(9600); // initialize the software serial port
  Serial.begin(9600);
  Serial.flush();
  
  // PINOS DOS MOTORES SAIDA
  pinMode(3, OUTPUT);     // LADO DIREITO 
  pinMode(5, OUTPUT);     // LADO DIREITO
  pinMode(6, OUTPUT);     // LADO ESQUERDO
  pinMode(9, OUTPUT);     // LADO ESQUERDO
  
  // INICIA PINO SERVO 10 DIGITAL
  servo1.attach(10);      // definido pino 10 digital
  servo1.write(servoCentro);
  
  //INICIA PINO SONAR
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);

  // INICIANDO PINOS DO SENSOR INFRAVERMELHO
  pinMode(infraDireito, INPUT);
  pinMode(infraEsquerdo, INPUT);
  
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

  if (bluetooth.available() > 0){
    dados = (char)bluetooth.read();
  }

  lcd.clear();                  // Limpa display 
  lcd.home();                   // Manda o cursor para a posição "zero" 
  lcd.print("     WALL-E     ");// Escreve
  sonar();
  lcd.setCursor(0,1);
  lcd.print("     ");
  lcd.print(distancia);
  lcd.print(" Cm     ");
  delay(100);

  if(analogRead(infraDireito) < 500){
    pare();
    pensa();
  }

  else if(analogRead(infraEsquerdo) < 500){
    pare();
    pensa();
  }

  else if(distancia >= distSegura){
    lcd.setCursor(0,1);
    lcd.print("     ");
    lcd.print(distancia);
    lcd.print(" Cm     ");
    frente();
  }

  else if(distancia < distSegura){
    pare();
    pensa();
  }

  else{
    pare();
    lcd.setCursor(0,1);
    lcd.print("  NENHUMA OP  ");
    delay(700);
    direita();
    delay(1000);
  }
  
}

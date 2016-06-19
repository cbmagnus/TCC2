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
int valor = 0;
int distSegura = 5;
String comando = "";

// INFRA VERMELHO
int infraFrente = 0;        //analogico 0

// VELOCIDADE DOS MOTORES
int velDir = 255;
int velEsq = 255;
int velMin = 0;

// PINOS DOS MOTORES
int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;

// POSICIONAMENTO SERVO ENTRE 0 E 180
int servo0 = 173;
int servo45 = 118;
int servo90 = 73;
int servo135 = 40;
int servo180 = 0;

// SENSOR ULTRASSONICO
int trig = 11;          // pino 11 digital
int echo = 12;          // pino 12 digital

//CONTADOR DE PULSOS E VARUAVEL DE VERIFICAÇÃO DE ESTADO
int pulsosDir = 0;
int pulsosEsq = 0;
int anteriorDir = 0;
int anteriorEsq = 0;
int saida = 0;
int e = 0;
int d = 0;

// CONTADOR DE PULSOS
int nrPulsosFrente = 7;
int nrPulsosRe = 3;
int nrPulsosAcertaPos = 4;
int nrPulsosLado = 15;

// NUMERO DE FUROS DO ENCODER
int nrFuros = 16;

//PINO LIGADO AO ENCODER
int encoderDir = 2;
int encoderEsq = 3;

#include <Servo.h>
Servo servo1;         //Criando objeto servo da frente

void setup() {
  Serial.begin(9600);
  //Serial.flush();
  
  // PINOS DOS MOTORES SAIDA
  pinMode(IN1, OUTPUT);     // LADO DIREITO 
  pinMode(IN2, OUTPUT);     // LADO DIREITO
  pinMode(IN3, OUTPUT);     // LADO ESQUERDO
  pinMode(IN4, OUTPUT);     // LADO ESQUERDO
  
  // INICIA PINO SERVO 10 DIGITAL
  servo1.attach(10);      // definido pino 10 digital
  servo1.write(servo90);
  
  //INICIA PINO SONAR
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);

  // INICIANDO PINOS DO SENSOR INFRAVERMELHO
  pinMode(infraFrente, INPUT);

  // PINO ENCODER
  pinMode(encoderDir, INPUT);
  pinMode(encoderEsq, INPUT);
}


void loop() {
  if (Serial.available() > 0){
    // Lê toda string recebida
    comando = leStringSerial();
    if(comando == "F"){
      Serial.println("INICIO");
      frente(nrPulsosFrente);
      Serial.println("FIMM");
    }
    else if(comando == "R"){
      Serial.println("INICIO");
      re(nrPulsosFrente);
      Serial.println("FIMM");
    }
    else if(comando == "D"){
      Serial.println("INICIO");
      direita(nrPulsosLado);
      Serial.println("FIMM");
    }
    else if(comando == "E"){
      Serial.println("INICIO");
      esquerda(nrPulsosLado);
      Serial.println("FIMM");
    }
    else if(comando == "TRAS"){ // pequena ré quando gira para direita
      Serial.println("INICIO");
      re(nrPulsosRe);
      Serial.println("FIMM");
    }
    else if(comando == "ACERTAPOS"){ // acerta a posição quando anda não linearmente em direção a uma parede
      Serial.println("INICIO");
      acertaPos(nrPulsosAcertaPos);
      Serial.println("FIMM");
    }
    else if(comando == "ANGULO0"){
      servo1.write(servo0);
      Serial.println("INICIO");
      delay(300);
      sonar();    // ja me retorna a distancia
      Serial.println("FIMM");
    }
    else if(comando == "ANGULO45"){
      servo1.write(servo45);
      Serial.println("INICIO");
      delay(300);
      sonar();
      Serial.println("FIMM");
    }
    else if(comando == "ANGULO90"){
      servo1.write(servo90);
      Serial.println("INICIO");
      delay(300);
      sonar();
      Serial.println("FIMM");
    }
    else if(comando == "ANGULO135"){
      servo1.write(servo135);
      Serial.println("INICIO");
      delay(300);
      sonar();
      Serial.println("FIMM");
    }
    else if(comando == "ANGULO180"){
      servo1.write(servo180);
      Serial.println("INICIO");
      delay(300);
      sonar();
      Serial.println("FIMM");
    }
    else{
      //Serial.println("Comando nao encntrado");
      pare();
      delay(100);
    }
    pare();
    delay(100);
  }
}

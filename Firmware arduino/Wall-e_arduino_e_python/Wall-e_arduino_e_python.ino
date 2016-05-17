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
int distSegura = 5;
String comando = "";

// INFRA VERMELHO
int infraFrente = 0;        //analogico 0

// VELOCIDADE DOS MOTORES
int velMax = 250;      //entre 0 parado e 255 maximo
int velMin = 0;

// PINOS DOS MOTORES
int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;

// POSICIONAMENTO SERVO ENTRE 0 E 180
int servo0 = 170;
int servo45 = 125;
int servo90 = 75;
int servo135 = 35;
int servo180 = 0;

// SENSOR ULTRASSONICO
int trig = 11;          // pino 11 digital
int echo = 12;          // pino 12 digital

//CONTADOR DE PULSOS E VARUAVEL DE VERIFICAÇÃO DE ESTADO
int pulsosDir = 0;
int pulsosEsq = 0;
int anteriorDir = 0;
int anteriorEsq = 0;
int nrPulsosFrente = 4;
int nrPulsosLado = 8;
// NUMERO DE FUROS DO ENCODER
int nrFuros = 8;
//PINO LIGADO AO ENCODER
int encoderDir = 2;
int encoderEsq = 3;

#include <Servo.h>
Servo servo1;         //Criando objeto servo da frente

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
    Serial.println(comando);

    if(analogRead(infraFrente) < 500){
      pare();
      Serial.println("Nao tem espaço a frente");
    }
    
    if(comando == "F"){
      frente(nrPulsosFrente);
      //delay(tempoFrente);
    }
  
    else if(comando == "R"){
      re(nrPulsosFrente);
      //delay(tempoFrente);
    }
  
    else if(comando == "D"){
      direita(nrPulsosLado);
      //delay(tempoLado);
    }
  
    else if(comando == "E"){
      esquerda(nrPulsosLado);
      //delay(tempoLado);
    }
  
    else if(comando == "ANGULO0"){
      servo1.write(servo0);
      delay(400);
      sonar();    // ja me retorna a distancia
      delay(100);
    }
  
    else if(comando == "ANGULO45"){
      servo1.write(servo45);
      delay(400);
      sonar();
      delay(100);
    }
  
    else if(comando == "ANGULO90"){
      servo1.write(servo90);
      delay(400);
      sonar();
      delay(100);
    }
  
    else if(comando == "ANGULO135"){
      servo1.write(servo135);
      delay(400);
      sonar();
      delay(100);
    }
  
    else if(comando == "ANGULO180"){
      servo1.write(servo180);
      delay(400);
      sonar();
      delay(100);
    }

    else{
      Serial.println("Comando nao encntrado");
      pare();
    }
    pare();
  }
}

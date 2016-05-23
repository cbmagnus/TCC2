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
int velDir = 240;
int velEsq = 250;
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
int nrPulsosFrente = 7;
int nrPulsosRe = 2;
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
      frente(nrPulsosFrente);
    }
    else if(comando == "R"){
      re(nrPulsosFrente);
    }
    else if(comando == "D"){
      direita(nrPulsosLado);
    }
    else if(comando == "E"){
      esquerda(nrPulsosLado);
    }
    else if(comando == "ANGULO0"){
      servo1.write(servo0);
      delay(300);
      sonar();    // ja me retorna a distancia
    }
    else if(comando == "ANGULO45"){
      servo1.write(servo45);
      delay(300);
      sonar();
    }
    else if(comando == "ANGULO90"){
      servo1.write(servo90);
      delay(300);
      sonar();
    }
    else if(comando == "ANGULO135"){
      servo1.write(servo135);
      delay(300);
      sonar();
    }
    else if(comando == "ANGULO180"){
      servo1.write(servo180);
      delay(300);
      sonar();
    }
    else{
      //Serial.println("Comando nao encntrado");
      pare();
    }
    pare();
  }
}

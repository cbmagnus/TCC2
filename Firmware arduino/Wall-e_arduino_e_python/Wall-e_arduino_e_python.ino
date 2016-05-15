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
int tempo = 1000;
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
int servo0 = 175;
int servo45 = 125;
int servo90 = 75;
int servo135 = 40;
int servo180 = 0;

// SENSOR ULTRASSONICO
int trig = 11;          // pino 11 digital
int echo = 12;          // pino 12 digital

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
}




void loop() {
  if (Serial.available() > 0){
    // Lê toda string recebida
    comando = leStringSerial();
    Serial.println(comando);
    
    if(comando == "F"){
      frente();
      delay(tempo);
    }
  
    else if(comando == "R"){
      re();
      delay(tempo);
    }
  
    else if(comando == "D"){
      direita();
      delay(tempo);
    }
  
    else if(comando == "E"){
      esquerda();
      delay(tempo);
    }
  
    else if(comando == "ANGULO0"){
      servo1.write(servo0);
      delay(300);
      sonar();    // ja me retorna a distancia
      delay(100);
    }
  
    else if(comando == "ANGULO45"){
      servo1.write(servo45);
      delay(300);
      sonar();
      delay(100);
    }
  
    else if(comando == "ANGULO90"){
      servo1.write(servo90);
      delay(300);
      sonar();
      delay(100);
    }
  
    else if(comando == "ANGULO135"){
      servo1.write(servo135);
      delay(300);
      sonar();
      delay(100);
    }
  
    else if(comando == "ANGULO180"){
      servo1.write(servo180);
      delay(300);
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

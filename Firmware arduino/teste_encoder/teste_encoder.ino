//Programa: Sensor de velocidade Arduino LM393
//Autor: Arduino e Cia

//Definicoes pinos Arduino ligados a entrada da Ponte H
int IN1 = 3;
int IN2 = 5;
int IN3 = 6;
int IN4 = 9;

//Pino ligado ao pino D0 do sensor
int rodaDireita = 8;
int rodaEsquerda = 7;
int rpm;
volatile byte pulsos;
unsigned long timeold;

//Altere o numero abaixo de acordo com o seu disco encoder
unsigned int pulsos_por_volta = 8;

void contador()
{
  //Incrementa contador
  pulsos++;
}

int velocMax = 200;
int velocMin = 0;

void setup()
{
  Serial.begin(9600);
  //Pino do sensor como entrada
  pinMode(rodaDireita, INPUT);
  pinMode(rodaEsquerda, INPUT);
  //Interrupcao 0 - pino digital 2
  //Aciona o contador a cada pulso
  attachInterrupt(0, contador, FALLING);
  pulsos = 0;
  rpm = 0;
  timeold = 0;
  //Define os pinos como saida
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop()
{
  digitalWrite(3, velocMax);
  digitalWrite(5, velocMin);
  //digitalWrite(6, velocMax);
  //digitalWrite(9, velocMin);

  //Atualiza contador a cada segundo
  if (millis() - timeold >= 1000){
    //Desabilita interrupcao durante o calculo
    detachInterrupt(0);
    rpm = (60 * 1000 / pulsos_por_volta ) / (millis() - timeold) * pulsos;
    timeold = millis();
    pulsos = 0;

    //Mostra o valor de RPM no serial monitor
    Serial.print("RPM DIR= ");
    Serial.println(rpm, DEC);
    //Habilita interrupcao
    attachInterrupt(0, contador, FALLING);
  }
}

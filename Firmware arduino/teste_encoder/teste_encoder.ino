int velMax = 255;
int velMin = 0;
int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;

//Pino ligado ao pino D0 do sensor
int motorDir = 2;
int motorEsq = 3;
int rpmDir;
int rpmEsq;
volatile byte pulsosDir;
volatile byte pulsosEsq;
unsigned long timeold;

//Altere o numero abaixo de acordo com o seu disco encoder
unsigned int pulsos_por_volta = 8;

void contadorDir(){
  pulsosDir++;
}
void contadorEsq(){
  pulsosEsq++;
}

void setup(){
  Serial.begin(9600);
  //Pino do sensor como entrada
  pinMode(motorDir, INPUT);
  pinMode(motorEsq, INPUT);
  //Interrupcao 0 - pino digital 2 Aciona o contador a cada pulso
  attachInterrupt(0, contadorDir, FALLING);
  attachInterrupt(1, contadorEsq, FALLING);
  pulsosDir = 0;
  pulsosEsq = 0;
  rpmDir = 0;
  rpmEsq = 0;
  timeold = 0;
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop(){
  analogWrite(IN1, velMin);
  analogWrite(IN2, velMax);
  analogWrite(IN3, velMax);
  analogWrite(IN4, velMin);
  //Atualiza contador a cada segundo
  if (millis() - timeold >= 1000){
    //Desabilita interrupcao durante o calculo
    detachInterrupt(0);
    detachInterrupt(1);
    rpmDir = (60 * 1000 / pulsos_por_volta ) / (millis() - timeold) * pulsosDir;
    rpmEsq = (60 * 1000 / pulsos_por_volta ) / (millis() - timeold) * pulsosEsq;
    timeold = millis();
    pulsosDir = 0;
    pulsosEsq = 0;

    //Mostra o valor de RPM no serial monitor
    Serial.print("RPMDir = ");
    Serial.println(rpmDir, DEC);
    Serial.print("RPMEsq = ");
    Serial.println(rpmEsq, DEC);
    Serial.println();
    //Habilita interrupcao
    attachInterrupt(0, contadorDir, FALLING);
    attachInterrupt(1, contadorEsq, FALLING);
  }
}

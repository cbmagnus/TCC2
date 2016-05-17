int velDir = 255;
int velEsq = 255;
int velMin = 0;
int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;

//Pino ligado ao pino D0 do sensor
int encoderDir = 2;
int encoderEsq = 3;

//Numero de furos do disco do encoder
int nrFuros = 8;

//Contador de pulsos e variavel de verificação de estado
int pulsosDir = 0;
int pulsosEsq = 0;
int anteriorDir = 0;
int anteriorEsq = 0;

int quantidade = 100;

void setup(){
  Serial.begin(9600);
  
  //Pino do sensor como entrada
  pinMode(encoderDir, INPUT);
  pinMode(encoderEsq, INPUT);
  
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop(){
  analogWrite(IN1, velMin);
  analogWrite(IN2, velDir);
  analogWrite(IN3, velEsq);
  analogWrite(IN4, velMin);

  // Encoder lado direito
  if(digitalRead(encoderDir) == LOW && anteriorDir == 0){
    anteriorDir = 1;
    delay(10);
  }
  // Encoder lado Esquerdo
  if(digitalRead(encoderEsq) == LOW && anteriorEsq == 0){
    anteriorEsq = 1;
    delay(10);
  }
  
  if(digitalRead(encoderDir) == HIGH && anteriorDir == 1){
    pulsosDir = pulsosDir + 1;
    Serial.println(pulsosDir);
    anteriorDir = 0;
    delay(10);
  }
  if(digitalRead(encoderEsq) == HIGH && anteriorEsq == 1){
    pulsosEsq = pulsosEsq + 1;
    Serial.println(pulsosEsq);
    anteriorEsq = 0;
    delay(10);
  }
  
  if(pulsosDir >= quantidade && pulsosEsq >= quantidade){
    analogWrite(IN1, velMin);
    analogWrite(IN2, velMin);
    analogWrite(IN3, velMin);
    analogWrite(IN4, velMin);
    pulsosDir = 0;
    pulsosEsq = 0;
    delay(8000);
  }
  
}

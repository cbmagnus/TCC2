int velMax = 255;
int velMin = 0;

int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;

int encoder_pin = 2;  // The pin the encoder is connected
int nrFuros = 8;
int pulsos = 0;
int anterior = 0;

void setup(){
  Serial.begin(9600);
  pinMode(encoder_pin, INPUT);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop(){
  analogWrite(IN1, velMin);
  analogWrite(IN2, velMax);
  analogWrite(IN3, velMin);
  analogWrite(IN4, velMin);

  if(digitalRead(encoder_pin) == LOW && anterior == 0){
    anterior = 1;
    delay(10);
  }

  if(digitalRead(encoder_pin) == HIGH && anterior == 1){
    pulsos = pulsos + 1;
    Serial.println(pulsos);
    anterior = 0;
    delay(10);
  }
  
  if(pulsos == nrFuros){
    analogWrite(IN1, velMin);
    analogWrite(IN2, velMin);
    analogWrite(IN3, velMin);
    analogWrite(IN4, velMin);
    pulsos = 0;
    delay(2000);
  }
}


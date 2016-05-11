int velMax = 255;
int velMin = 0;

int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;
  
void setup(){
  Serial.begin(9600);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  analogWrite(IN1, velMin);
  analogWrite(IN2, velMax);
  analogWrite(IN3, velMax);
  analogWrite(IN4, velMin);
}

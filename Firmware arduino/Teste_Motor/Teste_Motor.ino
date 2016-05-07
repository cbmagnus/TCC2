int velMax = 255;
int velMin = 0;

int IN1 = 3;
int IN2 = 5;
int IN3 = 6;
int IN4 = 9;
  
void setup(){
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  digitalWrite(IN1, velMax);
  digitalWrite(IN2, velMin);
  digitalWrite(IN3, velMax);
  digitalWrite(IN4, velMin);
}

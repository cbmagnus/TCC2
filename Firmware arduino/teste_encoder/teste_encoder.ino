int velMax = 255;
int velMin = 0;

int IN1 = 3;
int IN2 = 5;
int IN3 = 6;
int IN4 = 9;
  
#define PIN_DO 8
volatile unsigned int pulses;
float rpm;
unsigned long timeOld;
#define HOLES_DISC 8
 
void counter(){
  pulses++;
}
 
void setup(){
  Serial.begin(9600);
  pinMode(PIN_DO, INPUT);
  pulses = 0;
  timeOld = 0;
  attachInterrupt(digitalPinToInterrupt(PIN_DO), counter, FALLING);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}
 
void loop(){
  digitalWrite(IN1, velMax);
  digitalWrite(IN2, velMin);
  digitalWrite(IN3, velMax);
  digitalWrite(IN4, velMin);
  if (millis() - timeOld >= 1000){
    detachInterrupt(digitalPinToInterrupt(PIN_DO));
    rpm = (pulses * 60) / (HOLES_DISC);
    Serial.println(rpm);
    
    timeOld = millis();
    pulses = 0;
    attachInterrupt(digitalPinToInterrupt(PIN_DO), counter, FALLING);  
  }
}

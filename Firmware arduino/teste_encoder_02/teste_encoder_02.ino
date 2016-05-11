int velMax = 255;
int velMin = 0;

int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;

int encoder_pin = 8;  // The pin the encoder is connected           
unsigned int rpm;     // rpm reading
volatile byte pulses;  // number of pulses
unsigned long timeold; 
// The number of pulses per revolution
// depends on your index disc!!
unsigned int pulsesperturn = 8;

void counter(){
  //Update count
  pulses++;
}

void setup(){
  Serial.begin(9600);
  //Use statusPin to flash along with interrupts
  pinMode(encoder_pin, INPUT);
 
  //Interrupt 0 is digital pin 2, so that is where the IR detector is connected
  //Triggers on FALLING (change from HIGH to LOW)
  attachInterrupt(1, counter, FALLING);
  // Initialize
  pulses = 0;
  rpm = 0;
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
  if (millis() - timeold >= 1000){  /*Uptade every one second, this will be equal to reading frecuency (Hz).*/
    //Don't process interrupts during calculations
    detachInterrupt(1);
    //Note that this would be 60*1000/(millis() - timeold)*pulses if the interrupt
    //happened once per revolution
    rpm = (60 * 1000 / pulsesperturn )/ (millis() - timeold)* pulses;
    timeold = millis();
    pulses = 0;
    
    //Write it out to serial port
    Serial.print("RPM = ");
    Serial.println(rpm,DEC);
    //Restart the interrupt processing
    attachInterrupt(1, counter, FALLING);
    }
}


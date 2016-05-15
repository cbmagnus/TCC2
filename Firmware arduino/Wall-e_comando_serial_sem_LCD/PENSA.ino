void pensa(){
    int distanciaD = 0;
    int distanciaE = 0;
    int distanciaFrente = 0 ;
    
    delay(200);
    servo1.write(servoDireita);
    delay(400);
    sonar();
    distanciaD = distancia;

    Serial.print("Direita= ");
    Serial.println(distancia);
    
    delay(400);
     
    servo1.write(servoEsquerda);
    delay(600);
    sonar();
    distanciaE = distancia;

    Serial.print("Esquerda= ");
    Serial.println(distancia);
    
    delay(400);
    
    servo1.write(servoCentro);
    delay(400);
    sonar();
    distanciaFrente = distancia;
    
    Serial.print("Frente= ");
    Serial.println(distancia);
    
    delay(400);

}

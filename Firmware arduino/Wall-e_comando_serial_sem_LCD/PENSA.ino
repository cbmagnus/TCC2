void pensa(){
    lcd.setCursor(0,1);  // posiciona o cursor na linha de baixo.
    lcd.print("#   PENSANDO   #");
    int distanciaD = 0;
    int distanciaE = 0;
    int distanciaFrente = 0 ;
    
    delay(200);
    servo1.write(servoDireita);
    delay(400);
    sonar();
    distanciaD = distancia;
    lcd.setCursor(0,1);  // posiciona o cursor na linha de baixo.
    lcd.print("Direita ");
    lcd.print(distancia);
    lcd.print(" Cm  ");

    Serial.print("Direita= ");
    Serial.println(distancia);
    
    delay(400);
     
    servo1.write(servoEsquerda);
    delay(600);
    sonar();
    distanciaE = distancia;
    lcd.setCursor(0,1);  // posiciona o cursor na linha de baixo.
    lcd.print("Esquerda ");
    lcd.print(distancia);
    lcd.print(" Cm ");

    Serial.print("Esquerda= ");
    Serial.println(distancia);
    
    delay(400);
    
    servo1.write(servoCentro);
    delay(400);
    sonar();
    distanciaFrente = distancia;
    lcd.setCursor(0,1);  // posiciona o cursor na linha de baixo.
    lcd.print("Frente ");
    lcd.print(distancia);
    lcd.print(" Cm   ");

    Serial.print("Frente= ");
    Serial.println(distancia);
    
    delay(400);

}

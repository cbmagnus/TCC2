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
    delay(400);
     
    servo1.write(servoEsquerda);
    delay(600);
    sonar();
    distanciaE = distancia;
    lcd.setCursor(0,1);  // posiciona o cursor na linha de baixo.
    lcd.print("Esquerda ");
    lcd.print(distancia);
    lcd.print(" Cm ");
    delay(400);
    
    servo1.write(servoCentro);
    delay(400);
    sonar();
    distanciaFrente = distancia;
    lcd.setCursor(0,1);  // posiciona o cursor na linha de baixo.
    lcd.print("Frente ");
    lcd.print(distancia);
    lcd.print(" Cm   ");
    delay(400);




    
    
    if(distanciaD > distanciaE){
      lcd.clear();
      lcd.setCursor(0,1); 
      lcd.print("DESVIO DIREITA ");
      re();
      delay(400); 
      pare();
      delay(300); 
      direita();
      delay(400);
    }
    
    else if(distanciaD < distanciaE){
      lcd.clear();
      lcd.setCursor(0,1);
      lcd.print("DESVIO ESQUERDA");
      re();
      delay(400);
      pare();
      delay(300);
      esquerda();
      delay(400);
    }

    else if(distanciaFrente > distSegura){
      frente();
      delay(200);
    }

    else if(distanciaE < distSegura && distanciaD < distSegura){
      lcd.clear();
      lcd.setCursor(0,1);
      lcd.print("   SEM SAIDA!   ");
      re();
      delay(400);
      pensa();
    }

    else{
      pare();
      delay(1000);
      lcd.clear();
      lcd.print("     ERRO!!!    ");
      re();
      delay(500);
      pensa();
    }
}

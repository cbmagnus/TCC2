void encoder(int nrPulsos){
  while((saida != 2) and (analogRead(infraFrente) > 500)){  
    // Encoder lado direito
    if((digitalRead(encoderDir) == LOW) and (anteriorDir == 0)){
      anteriorDir = 1;
      delay(10);
    }
    // Encoder lado Esquerdo
    if((digitalRead(encoderEsq) == LOW) and (anteriorEsq == 0) and (nrPulsos >= pulsosEsq)){
      anteriorEsq = 1;
      delay(10);
    }

        
    if((digitalRead(encoderDir) == HIGH) and (anteriorDir == 1) and (nrPulsos >= pulsosDir)){
      pulsosDir = pulsosDir + 1;
      anteriorDir = 0;
      delay(10);
    }
    if((digitalRead(encoderEsq) == HIGH) and (anteriorEsq == 1) and (nrPulsos >= pulsosEsq)){
      pulsosEsq = pulsosEsq + 1;
      anteriorEsq = 0;
      delay(10);
    }



    //Quando atingido o nr de pulsos. Para o lado corespondente
    if(nrPulsos <= pulsosDir){
      analogWrite (IN1, velMin);
      analogWrite (IN2, velMin);
      delay(10);
      if(d <= 0){
        saida = saida + 1;
        d = d + 1;
      }
    }
    if(nrPulsos <= pulsosEsq){
      analogWrite (IN3, velMin);
      analogWrite (IN4, velMin);
      delay(10);
      if(e <= 0){
        saida = saida + 1;
        e = e + 1;
      }
    }
    delay(10);
  }


  if(analogRead(infraFrente) < 500){
    Serial.println("PAREDEP");
    re(nrPulsosRe);
    Serial.println("FIMM");
  }
  
  pulsosEsq = 0;
  pulsosDir = 0;
  saida = 0;
  e = 0;
  d = 0;
  delay(30);
}

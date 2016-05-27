void encoder(int nrPulsos){
  while(nrPulsos >= pulsosDir && nrPulsos >= pulsosEsq && analogRead(infraFrente) > 500){
    // Encoder lado direito
    if(digitalRead(encoderDir) == LOW && anteriorDir == 0){
      anteriorDir = 1;
      delay(5);
    }
    // Encoder lado Esquerdo
    if(digitalRead(encoderEsq) == LOW && anteriorEsq == 0){
      anteriorEsq = 1;
      delay(5);
    }
    
    if(digitalRead(encoderDir) == HIGH && anteriorDir == 1){
      pulsosDir = pulsosDir + 1;
      anteriorDir = 0;
      delay(5);
    }
    if(digitalRead(encoderEsq) == HIGH && anteriorEsq == 1){
      pulsosEsq = pulsosEsq + 1;
      anteriorEsq = 0;
      delay(5);
    }
  }

  if(analogRead(infraFrente) < 500){
    pare();
    delay(100);
    Serial.println("PAREDEP");
    re(nrPulsosRe);
    delay(100);
    Serial.println("FIMM");
  }
  
  pulsosEsq = 0;
  pulsosDir = 0;
  delay(20);
}

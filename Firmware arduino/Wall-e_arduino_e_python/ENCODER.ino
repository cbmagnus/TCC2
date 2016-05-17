void encoder(int nrPulsos){
  while(nrPulsos >= pulsosDir && nrPulsos >= pulsosEsq){
    // Encoder lado direito
    if(digitalRead(encoderDir) == LOW && anteriorDir == 0){
      anteriorDir = 1;
      delay(10);
    }
    // Encoder lado Esquerdo
    if(digitalRead(encoderEsq) == LOW && anteriorEsq == 0){
      anteriorEsq = 1;
      delay(10);
    }
    
    if(digitalRead(encoderDir) == HIGH && anteriorDir == 1){
      pulsosDir = pulsosDir + 1;
      Serial.println(pulsosDir);
      anteriorDir = 0;
      delay(10);
    }
    if(digitalRead(encoderEsq) == HIGH && anteriorEsq == 1){
      pulsosEsq = pulsosEsq + 1;
      Serial.println(pulsosEsq);
      anteriorEsq = 0;
      delay(10);
    }
  }
  pulsosEsq = 0;
  pulsosDir = 0;
  Serial.flush();
  delay(100);
}

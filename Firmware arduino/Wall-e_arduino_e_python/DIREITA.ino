void direita(int nrPulsos){
  analogWrite (IN1, velMax);
  analogWrite (IN2, velMin);
  analogWrite (IN3, velMax);
  analogWrite (IN4, velMin);
  encoder(nrPulsos);
}


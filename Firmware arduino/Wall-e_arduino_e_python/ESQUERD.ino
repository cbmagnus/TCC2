void esquerda(int nrPulsos){
  analogWrite (IN1, velMin);
  analogWrite (IN2, velMax);
  analogWrite (IN3, velMin);
  analogWrite (IN4, velMax);
  encoder(nrPulsos);
}


void esquerda(int nrPulsos){
  analogWrite (IN1, velMin);
  analogWrite (IN2, velDir);
  analogWrite (IN3, velMin);
  analogWrite (IN4, velEsq);
  encoder(nrPulsos);
}


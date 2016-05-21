void direita(int nrPulsos){
  analogWrite (IN1, velDir);
  analogWrite (IN2, velMin);
  analogWrite (IN3, velEsq);
  analogWrite (IN4, velMin);
  encoder(nrPulsos);
}


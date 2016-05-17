void frente(int nrPulsos){
  analogWrite (IN1, velMin);
  analogWrite (IN2, velMax);
  analogWrite (IN3, velMax);
  analogWrite (IN4, velMin);
  encoder(nrPulsos);
}


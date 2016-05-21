void frente(int nrPulsos){
  analogWrite (IN1, velMin);
  analogWrite (IN2, velDir);
  analogWrite (IN3, velEsq);
  analogWrite (IN4, velMin);
  encoder(nrPulsos);
}


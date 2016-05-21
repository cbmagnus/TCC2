void re(int nrPulsos){
  analogWrite (IN1, velDir);
  analogWrite (IN2, velMin);
  analogWrite (IN3, velMin);
  analogWrite (IN4, velEsq);
  encoder(nrPulsos);
}


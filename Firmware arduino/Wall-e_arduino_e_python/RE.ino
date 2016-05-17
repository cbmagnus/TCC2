void re(int nrPulsos){
  analogWrite (IN1, velMax);
  analogWrite (IN2, velMin);
  analogWrite (IN3, velMin);
  analogWrite (IN4, velMax);
  encoder(nrPulsos);
}


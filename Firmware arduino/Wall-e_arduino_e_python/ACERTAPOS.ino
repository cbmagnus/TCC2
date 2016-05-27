void acertaPos(int nrPulsos){
  analogWrite (IN1, velDir);
  analogWrite (IN2, velMin);
  analogWrite (IN3, velMin);
  analogWrite (IN4, velMin);
  encoder(nrPulsos);
}


void acertaPos(int nrPulsos){
  analogWrite (IN1, velDir);
  analogWrite (IN2, velMin);
  analogWrite (IN3, velMin);
  analogWrite (IN4, velMin);
  saida = saida + 1;
  e = e + 1;
  encoder(nrPulsos);
}


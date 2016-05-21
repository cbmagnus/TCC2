void verDist(){
  digitalWrite (trig,LOW);
  delayMicroseconds(2);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);
  distancia = pulseIn (echo,HIGH);
  distancia = distancia / 58;
  //Serial.println(distancia);
  delay(100);
}

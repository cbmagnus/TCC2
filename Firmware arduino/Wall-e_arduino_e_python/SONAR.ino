void sonar(){
  valor = 0;
  for(int i=0; i<3; i++){
    verDist();
    if(distancia > 1){
      valor = valor + distancia;
    }else{
      i--;
    }
  }
  distancia = 0;
  //Serial.println(valor);
  distancia = (valor / 3);
  Serial.println(distancia);
  delay(10);
}

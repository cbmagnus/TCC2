void sonar(){
  valor = 0;
  for(int i=0; i<5; i++){
    verDist();
    if(distancia > 1){
      valor = valor + distancia;
    }else{
      i--;
    }
  }
  //Serial.println(valor);
  distancia = (valor / 5);
  Serial.print(distancia);
}

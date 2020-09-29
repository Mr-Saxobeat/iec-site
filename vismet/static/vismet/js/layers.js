map.addLayer(xaviewrWeatherStation);

var divObservedData = document.getElementById("dados-observados");
var divSimulatedData = document.getElementById("dados-simulados");
var divByCity = document.getElementById("porMunicipio");
var divByPixel = document.getElementById("porPixel");
var selCamadaFuturos = document.getElementById("sel-camada-dados-futuros");

divObservedData.style.display = "block";
divSimulatedData.style.display = "none";


document.getElementById("estacoesxavier").addEventListener("click", displayXavier);
// document.getElementById("satelitereanalise").addEventListener("click", displaySatelite);
document.getElementById("cenariosfuturos").addEventListener("click", displayFuturo);

var XavierIsOn = true;
var PixelIsOn = false;

function displayXavier() {
  if(XavierIsOn){
    map.removeLayer(xaviewrWeatherStation);
    XavierIsOn = false;
  }
  else{
    map.addLayer(xaviewrWeatherStation);
    XavierIsOn = true;

    map.removeLayer(pixels_layer);
    map.removeLayer(cities_layer);
    PixelIsOn = false;

    divObservedData.style.display = "block";
    divSimulatedData.style.display = "none";
  }
}

function displayFuturo() {
  if(PixelIsOn){
    map.removeLayer(pixels_layer);
    PixelIsOn = false;
  }
  else{
    map.addLayer(pixels_layer);
    PixelIsOn = true;

    map.removeLayer(xaviewrWeatherStation);
    removeData(chart);
    chart.options.title.text = "";
    chart.update();
    XavierIsOn = false;

    divObservedData.style.display = "none";
    divSimulatedData.style.display = "block";
    // document.getElementById("porMunicipio").style.display = "none";
    // document.getElementById("porPixel").style.display = "block";
    // document.getElementById("cenarios-futuros-layer").style.display = "block";
    selCamadaFuturos.value = "pixel";
    divByPixel.style.display = "block";
    divByCity.style.display = "none";
  }
}

selCamadaFuturos.addEventListener("change", function(){
  var value = this.value;

  if(value == "city"){
    divByCity.style.display = "block";
    divByPixel.style.display = "none";

    map.removeLayer(pixels_layer);
    map.addLayer(cities_layer);
  }
  else if(value == "pixel"){
    divByCity.style.display = "none";
    divByPixel.style.display = "block";

    map.removeLayer(cities_layer);
    map.addLayer(pixels_layer);
  }
})

function displaySatelite() {
}



var event_change = new Event('change');
var sel_observados_fonte = document.getElementById("fonte-dados-observados");
var sel_variavel = document.getElementById("station_variable");
add_xavier_options();



function clear_sel(){
  var length = sel_variavel.options.length;
  for (i = length-1; i >= 0; i--) {
    sel_variavel.remove(i);
  }
}

function add_xavier_options(){
  var opt_maxTemp = document.createElement('option');
    opt_maxTemp.appendChild(document.createTextNode('Temperatura Máxima'));
    opt_maxTemp.value = "maxTemp";
    sel_variavel.appendChild(opt_maxTemp);

  var opt_minTemp = document.createElement('option');
    opt_minTemp.appendChild(document.createTextNode('Temperatura Mínima'));
    opt_minTemp.value = "minTemp";
    sel_variavel.appendChild(opt_minTemp);

  var opt_evapo = document.createElement('option');
    opt_evapo.appendChild(document.createTextNode('Evapotranspiração'));
    opt_evapo.value = "maxTemp";
    sel_variavel.appendChild(opt_evapo);

  var opt_relHum = document.createElement('option');
    opt_relHum.appendChild(document.createTextNode('Umidade Relativa'));
    opt_relHum.value = "relHum";
    sel_variavel.appendChild(opt_relHum);

  var opt_solarIns = document.createElement('option');
    opt_solarIns.appendChild(document.createTextNode('Radiação Solar'));
    opt_solarIns.value = "solarIns";
    sel_variavel.appendChild(opt_solarIns);

  var opt_windSpeed = document.createElement('option');
    opt_windSpeed.appendChild(document.createTextNode('Velocidade do Vento'));
    opt_windSpeed.value = "windSpeed";
    sel_variavel.appendChild(opt_windSpeed);

  sel_variavel.value = "maxTemp";
  sel_variavel.dispatchEvent(event_change);
}

function add_inmet_options(){
  var opt_maxTemp = document.createElement('option');
    opt_maxTemp.appendChild(document.createTextNode('Temperatura Máxima'));
    opt_maxTemp.value = "maxTemp";
    sel_variavel.appendChild(opt_maxTemp);

  var opt_minTemp = document.createElement('option');
    opt_minTemp.appendChild(document.createTextNode('Temperatura Mínima'));
    opt_minTemp.value = "minTemp";
    sel_variavel.appendChild(opt_minTemp);

  var opt_precip = document.createElement('option');
    opt_precip.appendChild(document.createTextNode('Precipitação'));
    opt_precip.value = "precip";
    sel_variavel.appendChild(opt_precip);

  var opt_relHum = document.createElement('option');
    opt_relHum.appendChild(document.createTextNode('Umidade Relativa'));
    opt_relHum.value = "relHum";
    sel_variavel.appendChild(opt_relHum);

  sel_variavel.value = "maxTemp";
  sel_variavel.dispatchEvent(event_change);
}


sel_observados_fonte.addEventListener("change", function(){
  var value = this.value;

  if(value == "xavier"){
    clear_sel();
    add_xavier_options();
  } else if(value == "inmet"){
    clear_sel();
    add_inmet_options();
  }
})

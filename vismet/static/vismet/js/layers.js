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

var XavierStations_Style = {
  fillColor: 'blue',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

function XavierStations_Layer_onEachFeature(feature, layer) {
  layer.bindPopup(feature.properties.popup_content);
  layer.on('click', function() {
    input_station_code.value = feature.properties.inmet_code;
    station_city = feature.properties.city;
    station_state = feature.properties.state;
    station_inmet = feature.properties.inmet_code;
    $( ".dateinput" ).datepicker( "option", "yearRange", "1980:2014");
    $( ".dateinput" ).datepicker( "option", "defaultDate", "01/01/1980");
    botoes = true;

    chart.options.title.text = "Estação nº " + station_inmet + ", " + station_city + " - " + station_state;
    chart.update();
  })
}

var XavierStations_Layer = L.geoJson([], {
    style: XavierStations_Style,
    pointToLayer: function(feature, latlng) {
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: XavierStations_Layer_onEachFeature,
});

function loadXavierLayer(){
  $.getJSON(url_stations + "json/xavier/0/", function (data) {
    XavierStations_Layer.addData(data);
  });
  // control.addOverlay(XavierStations_Layer, "xavier");

  layers_dic["xavier"] = XavierStations_Layer;
}

function Show_Xavier_Data(code, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  $.getJSON(url_stations + "json/xavier/" + code + "/" + startDate + "/" + finalDate, function(data) {
    var variable = 'evapo';
    switch (selBox_variable_display.value.toLowerCase()) {
      case 'evapotranspiração':
        variable = 'evapo';
        break;
      case 'umidade relativa':
        variable = 'relHum';
        break;
      case 'radiação solar':
        variable = 'solarIns';
        break;
      case 'temperatura máxima':
        variable = "maxTemp";
        break;
      case 'temperatura mínima':
        variable = "minTemp";
        break;
      case 'velocidade do vento':
        variable = 'windSpeed';
        break;
      default:
        variable = 'evapo';
        break;
    }
    chart_update(chart, data, variable);
  })
}

function Download_Xavier_Data(code, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  var url = url_stations + "csv/xavier/" + code + "/" + startDate + "/" + finalDate;
  window.location.href = url;
}

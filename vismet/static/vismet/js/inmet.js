var INMETStations_Style = {
  fillColor: 'red',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

function INMETStations_Layer_onEachFeature(feature, layer) {
  layer.bindPopup(feature.properties.popup_content);
  layer.on('click', function() {
    input_station_code.value = feature.properties.inmet_code;
    station_city = feature.properties.city;
    station_state = feature.properties.state;
    station_inmet = feature.properties.inmet_code;
    botoes = true;

    chart.options.title.text = "Estação nº " + station_inmet + ", " + station_city + " - " + station_state;
    chart.update();
  })
}

var INMETStations_Layer = L.geoJson([], {
  style: INMETStations_Style,
  pointToLayer: function(feature, latlng) {
    return new L.CircleMarker(latlng, {radius: 5});
  },
  onEachFeature: INMETStations_Layer_onEachFeature,
});

function loadINMETLayer(){
  $.getJSON(url_stations + "json/inmet/0/", function(data){
    INMETStations_Layer.addData(data);
  })
  control.addOverlay(INMETStations_Layer, "inmet");

  layers_dic["inmet"] = INMETStations_Layer;
}

function Show_INMET_Data(code, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  $.getJSON(url_stations + "json/inmet/" + code + "/" + startDate + "/" + finalDate, function(data) {
    var variable = 'maxTemp';
    switch (selBox_variable_display.value) {
      case 'temperatura máxima':
        variable = "maxTemp";
        break;
      case 'temperatura mínima':
        variable = "minTemp";
        break;
      case 'umidade relativa':
        variable = 'relHum';
        break;
      case 'precipitação':
        variable = 'precip';
        break;
      default:
        variable = 'maxTemp';
        break;
    }
    chart_update(chart, data, variable);
  })
}

var INMETStations_Style = {
  fillColor: 'red',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

function INMETStations_Layer_onEachFeature(feature, layer) {
  var popupContent = feature.properties.popup_content;
  layer.bindPopup(popupContent);
  layer.on('click', function() {
    input_station_code.value = feature.properties.inmet_code;
    station_city = feature.properties.city;
    station_state = feature.properties.state;
    station_inmet = feature.properties.inmet_code;

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
  $.getJSON(url_stations + "json/inmet/", function(data){
    data.forEach(station => {
      station_geojson = {
        "type": "Feature",
        "properties": {
          "inmet_code": station.fields.inmet_code,
          "state": station.fields.state,
          "city": station.fields.city,
          "type": station.fields.type,
          "latitude": station.fields.latitude,
          "longitude": station.fields.longitude,
          "altitude": station.fields.altitude,
          "startDate": station.fields.startDate,
          "finalDate": station.fields.finalDate,
          "status": station.fields.status,
        },
        "geometry": {
          "type": "Point",
          "coordinates": [station.fields.longitude, station.fields.latitude],
        }
      }

      INMETStations_Layer.addData(station_geojson);
    });
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

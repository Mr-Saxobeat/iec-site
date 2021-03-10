
function style(feature){
  return {
    fillColor: feature.properties.type.toLowerCase() == "automatica" ? "red" : "green",
    weight: 1,
    opacity: 1,
    color: 'black',
    fillOpacity: 1,
  }
}

function INMETStations_Layer_onEachFeature(feature, layer) {
  layer.bindPopup(feature.properties.popup_content);
  layer.on('click', function() {
    input_station_code.value = feature.properties.inmet_code;
    station_city = feature.properties.city;
    station_state = feature.properties.state;
    station_inmet = feature.properties.inmet_code;

    station_startDate = feature.properties.startDate;
    calendar_startDate = station_startDate.split("-").slice(0, 1).join("-");
    station_finalDate = feature.properties.finalDate;
    if (station_finalDate == null) {
      calendar_finalDate = "c";
    } else {
    calendar_finalDate = station_finalDate.split("-").slice(0, 1).join("-");
  };
    yearRange = calendar_startDate+":"+calendar_finalDate;
    $( ".dateinput" ).datepicker( "option", "yearRange", yearRange);
    $( ".dateinput" ).datepicker( "option", "minDate", new Date(station_startDate));
    $( ".dateinput" ).datepicker( "option", "defaultDate", new Date(station_startDate));

    botoes = true;
    document.getElementById("station_startDate").innerHTML = station_startDate;
    if(station_finalDate == null){
    document.getElementById("station_finalDate").innerHTML = "Até o presente";
   } else {
    document.getElementById("station_finalDate").innerHTML = station_finalDate;
   }
   $("#stationdata").show();


    chart.options.title.text = "Estação nº " + station_inmet + ", " + station_city + " - " + station_state;
    chart.update();
  })
}

var INMETStations_Layer = L.geoJson([], {
  style: style,
  pointToLayer: function(feature, latlng) {
    return new L.CircleMarker(latlng, {radius: 5});
  },
  onEachFeature: INMETStations_Layer_onEachFeature,
});

function loadINMETLayer(){
  $.getJSON(url_stations + "json/inmet/0/", function(data){
    INMETStations_Layer.addData(data);
  })
  // control.addOverlay(INMETStations_Layer, "inmet");

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
      case 'radiação solar':
        variable = 'solarIns';
        break;
      default:
        variable = 'maxTemp';
        break;
    }
    chart_update(chart, data, variable);
  })
}

function Download_INMET_Data(code, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  var url = url_stations + "csv/inmet/" + code + "/" + startDate + "/" + finalDate;
  window.location.href = url;
}

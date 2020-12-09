var ANA_Precip_Style = {
  fillColor: 'green',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

var ANA_Flow_Style = {
  fillColor: 'purple',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

function ANAStations_Layer_onEachFeature(feature, layer){
  layer.bindPopup(feature.properties.popup_content);
  layer.on('click', function() {
    input_station_code.value = feature.properties.omm_code;
    station_city = feature.properties.city;
    station_state = feature.properties.state;
    station_inmet = feature.properties.omm_code;

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

    chart.options.title.text = "Estação nº " + station_inmet + ", " + station_city + " - " + station_state;
    chart.update();
  })
}

var ANA_Precip_Layer = L.geoJson([], {
    style: ANA_Precip_Style,
    pointToLayer: function(feature, latlng) {
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: ANAStations_Layer_onEachFeature,
});

var ANA_Flow_Layer = L.geoJson([], {
    style: ANA_Flow_Style,
    pointToLayer: function(feature, latlng) {
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: ANAStations_Layer_onEachFeature,
});

function loadANALayer(){
  $.getJSON(url_stations + 'json/ana/Pluviométrica/', function (data){
    ANA_Precip_Layer.addData(data);
  })

  $.getJSON(url_stations + 'json/ana/Fluviométrica/', function (data){
    ANA_Flow_Layer.addData(data);
  })

  // control.addOverlay(ANA_Precip_Layer, "ana-precip");
  // control.addOverlay(ANA_Flow_Layer, "ana-flow");

  layers_dic["ana-precip"] = ANA_Precip_Layer;
  layers_dic["ana-flow"] = ANA_Flow_Layer;
}


function Show_ANA_Data(code, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  $.getJSON(url_stations + "json/ana/" + code + "/" + startDate + "/" + finalDate, function(data) {
    chart_update(chart, data, "value");
  })
}

function Download_ANA_Data(code, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  var url = url_stations + "csv/ana/" + code + "/" + startDate + "/" + finalDate;
  window.location.href = url;
}

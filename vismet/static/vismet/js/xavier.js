var XavierStations_Style = {
  fillColor: 'blue',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

function XavierStations_Layer_onEachFeature(feature, layer) {
  var popupContent = feature.properties.popup_content;
  var input_inmet_code = document.getElementById('input_inmet_code');
  layer.bindPopup(popupContent);
  layer.on('click', function() {
    input_inmet_code.value = feature.properties.inmet_code;
    station_city = feature.properties.name;
    station_state = feature.properties.state;
    station_inmet = feature.properties.inmet_code;

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

$.getJSON(url_stations + "json/xavier", function (data) {
  data.forEach(station => {
    station_geojson = {
      "type": "Feature",
      "properties": station.fields,
      "geometry": {
        "type": "Point",
        "coordinates": [station.fields.longitude, station.fields.latitude],
      }
    }

    XavierStations_Layer.addData(station_geojson);
  });
});

control.addOverlay(XavierStations_Layer, "Estações Xavier");

var station_city;
var station_state;
var station_inmet;
var station_variable = document.getElementById("station_variable");
var startStation;

// Função para mudar a legenda do gráfico ao
// selecionar uma variável.
station_variable.addEventListener("change", function() {
  var variable_value = station_variable.value;
  var variable_name;
  var variable_unit;
  var legend;

  switch (variable_value) {
    case "maxTemp":
      variable_name = "Temperatura máxima";
      variable_unit = "ºC";
      break;
    case "minTemp":
      variable_name = "Temperatura mínima";
      variable_unit = "ºC";
      break;
    case "evapo":
      variable_name = "Evapotranspiração";
      variable_unit = "mm";
      break;
    case "relHum":
      variable_name = "Umidade Relativa";
      variable_unit = "%";
      break;
    case "solarIns":
      variable_name = "Irradiação Solar";
      variable_unit = "MJ/m²";
      break;
    case "windSpeed":
      variable_name = "Velocidade do Vento a 2m de altitude";
      variable_unit = "m/s";
      break;
    case "precip":
      variable_name = "Precipitação";
      variable_unit = "mm";
      break;
    default:
      variable_name = "none";
      break;
  }

  chart.options.scales.yAxes[0].scaleLabel.display = true;
  chart.options.scales.yAxes[0].scaleLabel.labelString = variable_unit;
  chart.data.datasets[0].label = variable_name;
  chart.options.legend.display = true;
  chart.update();

});








var btn_submit = $("#btn_submit");

btn_submit.click(function(){

  var inmet_code = $("#input_inmet_code").val();
  var startDate = $("#startDate").val();
  var finalDate = $("#finalDate").val();

  for(i = 0; i < 3; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }


  if(sel_observados_fonte.value == "xavier"){
    var url_api = document.getElementById("url-xavier-stations").value;
  }else if(sel_observados_fonte.value == "inmet"){
    var url_api = document.getElementById("url-inmet-stations").value;
  }

  $.getJSON(url_api + "json" + "/" + inmet_code + "/" + startDate + "/" + finalDate,
    function(data_response){

      removeData(chart);

      var value;

      data_response.forEach((dt, i) => {
        chart.data.labels.push(dt.fields.date);

        value = dt.fields[station_variable.value];

        if(value == 0 || value == "NaN" || value == "-9999"){
          chart.data.datasets[0].data.push(null);
        }
        else{
          chart.data.datasets[0].data.push(value);
        }
      });

      chart.update();
  })
})

var btn_download = $("#btn_download");
btn_download.click(function(){

  if(sel_observados_fonte.value == "xavier"){
    var url_api = $("#url-xavier-stations").val();
  }else if(sel_observados_fonte.value == "inmet"){
    var url_api = $("#url-inmet-stations").val();
  }

  var inmet_code = $("#input_inmet_code").val();
  var startDate = $("#startDate").val();
  var finalDate = $("#finalDate").val();

  for(i = 0; i < 3; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }
  window.location = url_api + "csv" + "/" + inmet_code + "/" + startDate + "/" + finalDate;
})

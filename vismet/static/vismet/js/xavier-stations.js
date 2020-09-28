var station_city;
var station_state;
var station_omm;
var station_variable = document.getElementById("station_variable");

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
      variable_unit = "Cº";
      break;
    case "minTemp":
      variable_name = "Temperatura mínima";
      variable_unit = "Cº";
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

function onEachFeature(feature, layer) {
  var popupContent = feature.properties.popup_content;
  var input_ommcode = document.getElementById('input_ommcode');
  layer.bindPopup(popupContent);
  layer.on('click', function() {
    input_ommcode.value = feature.properties.omm_code;
    station_city = feature.properties.name;
    station_state = feature.properties.state;
    station_omm = feature.properties.omm_code;

    chart.options.title.text = "Estação nº " + station_omm + ", " + station_city + " - " + station_state;
    chart.update();
  })
}

var XavierStation_style = {
  fillColor: 'blue',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

var xaviewrWeatherStation = L.geoJson([], {
    style: XavierStation_style,
    pointToLayer: function(feature, latlng) {
      lat = feature.properties.latitude;
      lng = feature.properties.longitude;
      latlng = L.latLng(lat, lng);
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: onEachFeature,
});

var XavierStation_url = $("#url-xavier-stations").val();

$.getJSON(XavierStation_url, function (data) {
  xaviewrWeatherStation.addData(data);
});

var overlays = {
  "Estações Xavier": xaviewrWeatherStation,
};

control.addOverlay(xaviewrWeatherStation, "Estações Xavier");

var btn_submit = $("#btn_submit");

btn_submit.click(function(){

  var ommCode = $("#input_ommcode").val();
  var startDate = $("#startDate").val();
  var finalDate = $("#finalDate").val();

  for(i = 0; i < 3; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  var url_api_xavierstation = $("#url-xavier-stations").val();

  $.getJSON(url_api_xavierstation + "json" + "/" + ommCode + "/" + startDate + "/" + finalDate,
    function(data_response){
      console.log(data_response);

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
  var ommCode = $("#input_ommcode").val();
  var startDate = $("#startDate").val();
  var finalDate = $("#finalDate").val();

  for(i = 0; i < 3; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }
  window.location = url_api_xavierstation + "csv" + "/" + ommCode + "/" + startDate + "/" + finalDate;
})

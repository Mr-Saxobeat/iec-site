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

function loadXavierLayer(){
  $.getJSON(url_stations + "json/xavier/0/", function (data) {
    XavierStations_Layer.addData(data);
  });
  control.addOverlay(XavierStations_Layer, "xavier");

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
        variable = 'evapo'
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


// var station_city;
// var station_state;
// var station_inmet;
// var station_variable = document.getElementById("station_variable");
// var startStation;
//
// // Função para mudar a legenda do gráfico ao
// // selecionar uma variável.
// station_variable.addEventListener("change", function() {
//   var variable_value = station_variable.value;
//   var variable_name;
//   var variable_unit;
//   var legend;
//
//   switch (variable_value) {
//     case "maxTemp":
//       variable_name = "Temperatura máxima";
//       variable_unit = "ºC";
//       break;
//     case "minTemp":
//       variable_name = "Temperatura mínima";
//       variable_unit = "ºC";
//       break;
//     case "evapo":
//       variable_name = "Evapotranspiração";
//       variable_unit = "mm";
//       break;
//     case "relHum":
//       variable_name = "Umidade Relativa";
//       variable_unit = "%";
//       break;
//     case "solarIns":
//       variable_name = "Irradiação Solar";
//       variable_unit = "MJ/m²";
//       break;
//     case "windSpeed":
//       variable_name = "Velocidade do Vento a 2m de altitude";
//       variable_unit = "m/s";
//       break;
//     case "precip":
//       variable_name = "Precipitação";
//       variable_unit = "mm";
//       break;
//     default:
//       variable_name = "none";
//       break;
//   }
//
//   chart.options.scales.yAxes[0].scaleLabel.display = true;
//   chart.options.scales.yAxes[0].scaleLabel.labelString = variable_unit;
//   chart.data.datasets[0].label = variable_name;
//   chart.options.legend.display = true;
//   chart.update();
//
// });
//
//
//
//
//
//
//
//
// var btn_submit = $("#btn_submit");
//
// btn_submit.click(function(){
//
//   var inmet_code = $("#input_inmet_code").val();
//   var startDate = $("#startDate").val();
//   var finalDate = $("#finalDate").val();
//
//   for(i = 0; i < 3; i++){
//     startDate = startDate.replace("/", "-");
//     finalDate = finalDate.replace("/", "-");
//   }
//
//
//   if(sel_observados_fonte.value == "xavier"){
//     var url_api = document.getElementById("url-xavier-stations").value;
//   }else if(sel_observados_fonte.value == "inmet"){
//     var url_api = document.getElementById("url-inmet-stations").value;
//   }
//
//   $.getJSON(url_api + "json" + "/" + inmet_code + "/" + startDate + "/" + finalDate,
//     function(data_response){
//
//       removeData(chart);
//
//       var value;
//
//       data_response.forEach((dt, i) => {
//         chart.data.labels.push(dt.fields.date);
//
//         value = dt.fields[station_variable.value];
//
//         if(value == 0 || value == "NaN" || value == "-9999"){
//           chart.data.datasets[0].data.push(null);
//         }
//         else{
//           chart.data.datasets[0].data.push(value);
//         }
//       });
//
//       chart.update();
//   })
// })
//
// var btn_download = $("#btn_download");
// btn_download.click(function(){
//
//   if(sel_observados_fonte.value == "xavier"){
//     var url_api = $("#url-xavier-stations").val();
//   }else if(sel_observados_fonte.value == "inmet"){
//     var url_api = $("#url-inmet-stations").val();
//   }
//
//   var inmet_code = $("#input_inmet_code").val();
//   var startDate = $("#startDate").val();
//   var finalDate = $("#finalDate").val();
//
//   for(i = 0; i < 3; i++){
//     startDate = startDate.replace("/", "-");
//     finalDate = finalDate.replace("/", "-");
//   }
//   window.location = url_api + "csv" + "/" + inmet_code + "/" + startDate + "/" + finalDate;
// })

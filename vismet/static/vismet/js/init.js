
var url_stations = document.getElementById("url-stations").value;
var url_data_options = document.getElementById("url-data-options").value;

// Essa variável armazena as opções que poderão ser selecionadas
// de acordo com a categoria, fonte, modelo.
$.getJSON(url_data_options, function (data) {
  createNewChart('line');
  chart.options.scales.yAxes[0].scaleLabel.display = true;
  chart.options.scales.yAxes[0].scaleLabel.labelString = "ºC";
  chart.options.legend.display = true;
  chart.update();

  json_data_options = JSON.parse(JSON.stringify(data));
  loadXavierLayer();
  loadANALayer();
  loadINMETLayer();
  loadETALayer();
  LoadETACity();
  showCategoryData("observados");
  map.addLayer(layers_dic["ana"]);
});



var btn_submit = document.getElementById("btn_submit");
var btn_download = document.getElementById("btn_download");
var input_station_code = document.getElementById("input_station_code");
var input_startDate = document.getElementById("startDate");
var input_finalDate = document.getElementById("finalDate");

btn_submit.addEventListener("click", function() {
  if (selBox_source_display.value.toUpperCase() == "ANA"){
    Show_ANA_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  } else if (selBox_source_display.value.toUpperCase() == "INMET"){
      Show_INMET_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  } else if (selBox_source_display.value.toUpperCase() == "XAVIER"){
    Show_Xavier_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  }
})

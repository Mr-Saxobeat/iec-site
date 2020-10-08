var dataSet_Start = {
  label: "Temperatura Máxima",
  data: [],
}

chart.data.datasets.push(dataSet_Start);

chart.options.scales.yAxes[0].scaleLabel.display = true;
chart.options.scales.yAxes[0].scaleLabel.labelString = "ºC";
chart.options.legend.display = true;
chart.update();

var url_stations = document.getElementById("url-stations").value;
var url_data_options = document.getElementById("url-data-options").value;

// Essa variável armazena as opções que poderão ser selecionadas
// de acordo com a categoria, fonte, modelo.
$.getJSON(url_data_options, function (data) {
  json_data_options = JSON.parse(JSON.stringify(data));
  loadJSONDataOptions(json_data_options);
  showCategoryData("observados");
  loadXavierLayer();
});

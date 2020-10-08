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

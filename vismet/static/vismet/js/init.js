chart.options.scales.yAxes[0].scaleLabel.display = true;
chart.options.scales.yAxes[0].scaleLabel.labelString = "ºC";
chart.data.datasets[0].label = "Temperatura máxima";
chart.options.legend.display = true;
chart.update();

var url_stations = document.getElementById("url-stations").value;

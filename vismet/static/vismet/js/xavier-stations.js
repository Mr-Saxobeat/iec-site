var station_city;
var station_state;
var station_omm;

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

var XavierStation_url = $("#xavier-station-geojson").val();

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
  var variable = $("#variable").val();

  for(i = 0; i < 3; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  $.getJSON(url_api_xavierstation + "json" + "/" + ommCode + "/" + startDate + "/" + finalDate,
    function(data_response){
      console.log(data_response);

      removeData(chart);

      var value;

      data_response.forEach((dt, i) => {
        chart.data.labels.push(dt.fields.date);

        value = dt.fields[variable];

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
  var variable = $("#variable").val();

  for(i = 0; i < 3; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }
  window.location = url_api_xavierstation + "csv" + "/" + ommCode + "/" + startDate + "/" + finalDate;
})

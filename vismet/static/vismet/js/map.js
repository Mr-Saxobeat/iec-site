var station_city;
var station_state;
var station_omm;

function onEachFeature(feature, layer) {
  var popupContent = feature.properties.popup_content;
  var input_stationId = document.getElementById('input_stationId');
  layer.bindPopup(popupContent);
  layer.on('click', function() {
    input_stationId.value = feature.properties.stationId;
    station_city = feature.properties.name;
    station_state = feature.properties.state;
    station_omm = feature.properties.omm_code;

    chart.options.title.text = "Estação nº " + station_omm + ", " + station_city + " - " + station_state;
    chart.update();
  })
}

var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
    '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

var grayscale   = L.tileLayer(mbUrl, {id: 'mapbox/light-v9', attribution: mbAttr}),
  streets  = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11',   attribution: mbAttr});

var xavierWeatherStation_style = {
  fillColor: 'blue',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

var xaviewrWeatherStation = L.geoJson([], {
    style: xavierWeatherStation_style,
    pointToLayer: function(feature, latlng) {
      lat = feature.properties.latitude;
      lng = feature.properties.longitude;
      latlng = L.latLnt(lng, lat);
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: onEachFeature,
});

 var xavierWeatherStation_url = $("#xavierweathergeojson").val();

$.getJSON(xavierWeatherStation_url, function (data) {
  xaviewrWeatherStation.addData(data);
});

var map = L.map('map', {
  center: [-19.3, -42.7],
  zoom: 6,
  layers: [streets, xaviewrWeatherStation],
});

var baseLayers = {
  "Grayscale": grayscale,
  "Streets": streets,
};

var overlays = {
  "Xavier": xaviewrWeatherStation,
};

L.control.layers(baseLayers, overlays).addTo(map);

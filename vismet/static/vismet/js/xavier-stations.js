var station_city;
var station_state;
var station_omm;

function onEachFeature(feature, layer) {
  var popupContent = feature.properties.popup_content;
  var input_stationId = document.getElementById('input_stationId');
  layer.bindPopup(popupContent);
  layer.on('click', function() {
    input_stationId.value = feature.properties.station_id;
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

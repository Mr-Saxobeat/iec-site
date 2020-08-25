cities_layer_style = {
  color: 'red',
};

function onEachFeature(feature, layer) {
  var popupContent = "Nome:" + feature.properties.nome;
  layer.bindPopup(popupContent);
}

var cities_layer = L.geoJson([], {
  style: cities_layer_style,

  onEachFeature: onEachFeature,
})

var url_cities = $("#cities-geojson").val();

$.getJSON(url_cities, function (data) {
  cities_layer.addData(data);
})

control.addOverlay(cities_layer, "Cidades");

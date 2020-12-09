var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
             '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
             'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

var streets  = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11',   attribution: mbAttr});

function City_Layer_onEachFeature(feature, layer) {
  var popupContent = feature.properties.name;
  layer.bindPopup(popupContent);
}

var City_Style = {
  color: 'black',
  weight: 2,
  opacity: 0.1,
};

var City_Layer = L.geoJson([], {
  style: City_Style,
  onEachFeature: City_Layer_onEachFeature,
})

$.getJSON("/plataforma/api/cities/", function (data) {
  City_Layer.addData(data);
  City_Layer.bringToBack();
})

var map = L.map('map', {
  center: [-19.145, -40.407],
  zoom: 6,
  layers: [streets, City_Layer],
});

var baseLayers = {
  "Mapa": streets,
};

var control = L.control.layers(baseLayers).addTo(map);

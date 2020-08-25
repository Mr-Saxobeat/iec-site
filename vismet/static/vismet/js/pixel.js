var boundings = [];
var points = [];

pixels_layer_style = {
  color: "green",
};

var pixels_layer = L.geoJson([], {
  style: pixels_layer_style,
});

var url_pixels = $("#pixels-geojson").val();

$.getJSON(url_pixels, function(data) {
  data.features.forEach(ft => {

    boundings = JSON.parse(ft.properties.boundings);

    // Leaflet pede longitude e latitude, por isso
    // aqui a ordem das coordenadas é invertida.
    boundings[0] = boundings[0].reverse();
    boundings[1] = boundings[1].reverse();

    var points = [
      boundings[0],
      [ boundings[1][0], boundings[0][1] ],
      boundings[1],
      [ boundings[0][0], boundings[1][1] ]
    ];

    var geoJsonFeature = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [points],
      }
    };

    pixels_layer.addData(geoJsonFeature);
  });
})

control.addOverlay(pixels_layer, "Pixels");

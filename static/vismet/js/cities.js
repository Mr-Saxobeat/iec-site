style = {
  color: 'red',
};

var i = 0;

function refreshChart(city_id){
  $.getJSON("http://127.0.0.1:8000/api/pixeldata/" + city_id + "/1-1-1960/1-1-1960/",
            function (data) {
              dates = []
              prec = []

              data.forEach(dt => {
                dates.push(dt.date);
                prec.push(dt.preciptation);
              });

              removeData(chart);
              addData(chart, dates, prec);
              chart.update();
            });

}

function highlightFeature(e) {
  var layer = e.target;

  layer.setStyle({
    color: 'green',
  });
}

function resetHighlight(e) {
  cities_layer.resetStyle(e.target);
}

function onEachFeature(feature, layer) {
  var popupContent = "Nome:" + feature.properties.nome;
  // layer.bindPopup(popupContent);
  layer.on({
    // click: highlightFeature,
    mouseout: resetHighlight,
    mouseover: highlightFeature,
  })
}


var cities_layer = L.geoJson([], {
  style: style,

  onEachFeature: onEachFeature,
})

var url_cities = $("#cities-geojson").val();

$.getJSON(url_cities, function (data) {
  cities_layer.addData(data);
})

control.addOverlay(cities_layer, "Cidades");

cities_layer_style = {
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

              // if(i == 0){
              //   console.log(dates);
              //   console.log(prec);
              //   i = 1;
              // }

              removeData(chart);
              addData(chart, dates, prec);
              chart.update();
            });

}

var i = 0;

function onEachFeature(feature, layer) {
  var popupContent = "Nome:" + feature.properties.nome;
  layer.bindPopup(popupContent);
  layer.on("click", function(){refreshChart(feature.id);});
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

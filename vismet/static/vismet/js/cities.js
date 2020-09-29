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

  if(!L.Browser.ie && !L.Browser.opera && !L.Browser.edge){
    layer.bringToFront();
  }
}

function resetHighlight(e) {
  if(e.target != oldLayer){
    cities_layer.resetStyle(e.target);
  }
}

var oldLayer = null;

function selectFeature(e) {

  if(oldLayer){
    cities_layer.resetStyle(oldLayer);
  }

  var layer = e.target;

  layer.setStyle({
    color: 'blue',
  });

  oldLayer = e.target;

  var feature = e.target.feature;

  $("#city_name")[0].value = feature.properties.nome;
}

function onEachFeature(feature, layer) {
  var popupContent = "Nome:" + feature.properties.nome;
  // layer.bindPopup(popupContent);
  layer.on({
    click: selectFeature,
    mouseout: resetHighlight,
    mouseover: highlightFeature,
  })
}


var cities_layer = L.geoJson([], {
  style: style,

  onEachFeature: onEachFeature,
})

var url_cities = $("#url-cities").val();

$.getJSON(url_cities, function (data) {
  cities_layer.addData(data);
})

control.addOverlay(cities_layer, "Cidades");


var btn_download_city_data = $("#btn_download_city_data");
btn_download_city_data.click(function(){

  var city_name = $("#city_name")[0].value;
  var startDate = $("#city_startDate")[0].value;
  var finalDate = $("#city_finalDate")[0].value;

  for(i = 0; i < 3; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  window.location = url_cities + "csv" + "/" + city_name + "/" + startDate + "/" + finalDate;
})

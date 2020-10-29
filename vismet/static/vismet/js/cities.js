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
    ETA_City_Layer.resetStyle(e.target);
  }
}

var oldLayer = null;

function selectFeature(e) {

  if(oldLayer){
    ETA_City_Layer.resetStyle(oldLayer);
  }

  var layer = e.target;

  layer.setStyle({
    color: 'blue',
  });

  oldLayer = e.target;

  var feature = e.target.feature;
  input_city_name.value = feature.properties.name;
}

function ETA_City_Layer_onEachFeature(feature, layer) {
  var popupContent = "Nome:" + feature.properties.name;
  layer.bindPopup(popupContent);
  layer.on({
    click: selectFeature,
    mouseout: resetHighlight,
    mouseover: highlightFeature,
  })
}

var ETA_City_Style = {
  color: 'red',
};

var ETA_City_Layer = L.geoJson([], {
  style: ETA_City_Style,

  onEachFeature: ETA_City_Layer_onEachFeature,
})

var url_cities = $("#url-cities").val();
function LoadETACity(){
  $.getJSON(url_cities, function (data) {
    ETA_City_Layer.addData(data);
  })
  control.addOverlay(ETA_City_Layer, "eta-city");
  layers_dic["eta por cidade"] = ETA_City_Layer;
}


function showCityData(cityName, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  $.getJSON(url_cities + "json/" + cityName + "/" + startDate + "/" + finalDate, function(data) {
    var variable = 'precip';
    switch (selBox_variable_display.value.toLowerCase()) {
      case 'preciptação':
        variable = 'precip';
        break;
    }
    chart_update(chart, data, variable);
  })
}

var ETA_Pixel_Style = {
  color: "green",
  weight: 0.5,
};
var selected_pixel_id;

function highlightFeature_pixel(e) {
  var layer = e.target;

  layer.setStyle({
    color: 'red',
    weight: 1,
  });

  if(!L.Browser.ie && !L.Browser.opera && !L.Browser.edge){
    layer.bringToFront();
  }
}

function resetHighlight_pixel(e) {
  if(e.target != oldLayer){
    ETA_Pixel_Layer.resetStyle(e.target);
  }
}

var oldLayer = null;

function selectFeature_pixel(e) {

  if(oldLayer){
    ETA_Pixel_Layer.resetStyle(oldLayer);
  }

  var layer = e.target;

  layer.setStyle({
    color: 'blue',
    weight: 3,
  });

  oldLayer = e.target;

  var feature = e.target.feature;
  input_city_name.value = feature.properties.name;

  botoes = true;
}


function ETA_Pixel_Layer_onEachFeature(feature, layer) {
  var pixel_id = feature.properties.id;
  layer.bindPopup(feature.properties.popup_content);
  layer.on("click", function(e) {
    selected_pixel_id = feature.properties.id;
    selected_pixel = feature;

    station_startDate = "1960-01-01";
    calendar_startDate = station_startDate.split("-").slice(0, 1).join("-");
    station_finalDate = "2099-12-01";
    if (station_finalDate == null) {
      calendar_finalDate = "c";
    } else {
    calendar_finalDate = station_finalDate.split("-").slice(0, 1).join("-");
    };
    yearRange = calendar_startDate+":"+calendar_finalDate;
    $( ".dateinput" ).datepicker( "option", "yearRange", "1960:2099");
    $( ".dateinput" ).datepicker( "option", "minDate", new Date(station_startDate));
    $( ".dateinput" ).datepicker( "option", "defaultDate", "01/01/1960");

    chart.options.title.text = "Coordenadas " + feature.properties.latitude + "º, " + feature.properties.longitude + "º"
    botoes = true;
    selectFeature_pixel(e);
  });
  layer.on({
    mouseout: resetHighlight_pixel,
    mouseover: highlightFeature_pixel,
  })
}

var ETA_Pixel_Layer = L.geoJson([], {
  style: ETA_Pixel_Style,
  onEachFeature: ETA_Pixel_Layer_onEachFeature,
});

// var url_pixels = $("#url-pixels").val();

function loadETALayer(){
  var url_pixels = $("#url-pixels").val();
  $.getJSON(url_pixels, function(data) {
    ETA_Pixel_Layer.addData(data);
  })
  // control.addOverlay(ETA_Pixel_Layer, "pixels");
  layers_dic["eta por pixel"] = ETA_Pixel_Layer;
  layers_dic["chirps"] = ETA_Pixel_Layer;
}

function Show_ETA_Data(pixel_id, startDate, finalDate){
  var url_pixels = $("#url-pixels").val();
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  $.getJSON(url_pixels + "json/" + pixel_id + "/" + selBox_model_display.value + "/" +startDate + "/" + finalDate, function(data) {
    var variable = 'evapo';
    switch (selBox_variable_display.value.toLowerCase()) {
      case 'evapotranspiração':
        variable = 'evapo'
        break;
      case 'temperatura mínima':
        variable = "minTemp";
        break;
      case 'temperatura máxima':
        variable = "maxTemp";
        break;
      case 'radiação de onda curta incidente à superficie':
        variable = 'ocis';
        break;
      case 'precipitação':
        variable = 'precip';
        break;
      case 'escoamento superficial':
        variable = 'rnof';
        break;
      case 'temperatura a 2m da superfície':
        variable = 'tp2m';
        break;
      default:
        variable = 'evapo';
        break;
    }
    chart_update(chart, data, variable);
  })
}

function Download_ETA_Data(pixel_id, startDate, finalDate){
  var url_pixels = $("#url-pixels").val();
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  var url = url_pixels + "csv/" + pixel_id + "/" + selBox_model_display.value + "/" +startDate + "/" + finalDate;
  window.location.href = url;
}

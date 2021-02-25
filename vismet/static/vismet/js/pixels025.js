var Pixel_025_Style = {
  color: "purple",
  weight: 0.5,
};
var selected_pixel_id;

function highlightFeature_pixel_025(e) {
  var layer = e.target;

  layer.setStyle({
    color: 'red',
    weight: 1,
  });

  if(!L.Browser.ie && !L.Browser.opera && !L.Browser.edge){
    layer.bringToFront();
  }
}

function resetHighlight_pixel_025(e) {
  if(e.target != oldLayer){
    Pixel_025_Layer.resetStyle(e.target);
  }
}

var oldLayer = null;

function selectFeature_pixel_025(e) {

  if(oldLayer){
    Pixel_025_Layer.resetStyle(oldLayer);
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


function Pixel_025_Layer_onEachFeature(feature, layer) {
  var pixel_id = feature.properties.id;
  layer.bindPopup(feature.properties.popup_content);
  layer.on("click", function(e) {
    selected_pixel_id = feature.properties.id;
    selected_pixel = feature;

    chart.options.title.text = "Coordenadas " + feature.properties.latitude + "º, " + feature.properties.longitude + "º"
    botoes = true;
    selectFeature_pixel_025(e);
  });
  layer.on({
    mouseout: resetHighlight_pixel_025,
    mouseover: highlightFeature_pixel_025,
  })
}

var Pixel_025_Layer = L.geoJson([], {
  style: Pixel_025_Style,
  onEachFeature: Pixel_025_Layer_onEachFeature,
});



function loadPixel_025_Layer(){
  var url_pixels_025 = $("#url-pixels-025").val();
  $.getJSON(url_pixels_025, function(data) {
    Pixel_025_Layer.addData(data);
  })
  // control.addOverlay(Pixel_025_Layer, "pixels 025");
  layers_dic["era5"] = Pixel_025_Layer;
}

// function Show_ETA_Data(pixel_id, startDate, finalDate){
//   for(var i = 0; i <= 2; i++){
//     startDate = startDate.replace("/", "-");
//     finalDate = finalDate.replace("/", "-");
//   }

//   $.getJSON(url_pixels + "json/" + pixel_id + "/" + selBox_model_display.value + "/" +startDate + "/" + finalDate, function(data) {
//     var variable = 'evapo';
//     switch (selBox_variable_display.value.toLowerCase()) {
//       case 'evapotranspiração':
//         variable = 'evapo'
//         break;
//       case 'temperatura mínima':
//         variable = "minTemp";
//         break;
//       case 'temperatura máxima':
//         variable = "maxTemp";
//         break;
//       case 'radiação de onda curta incidente à superficie':
//         variable = 'ocis';
//         break;
//       case 'precipitação':
//         variable = 'precip';
//         break;
//       case 'escoamento superficial':
//         variable = 'rnof';
//         break;
//       case 'temperatura a 2m da superfície':
//         variable = 'tp2m';
//         break;
//       default:
//         variable = 'evapo';
//         break;
//     }
//     chart_update(chart, data, variable);
//   })
// }

// function Download_ETA_Data(pixel_id, startDate, finalDate){
//   for(var i = 0; i <= 2; i++){
//     startDate = startDate.replace("/", "-");
//     finalDate = finalDate.replace("/", "-");
//   }

//   var url = url_pixels + "csv/" + pixel_id + "/" + selBox_model_display.value + "/" +startDate + "/" + finalDate;
//   window.location.href = url;
// }

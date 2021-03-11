var Pixel_01_Style = {
  color: "purple",
  weight: 0.5,
};
var selected_pixel01 = {};

function highlightFeature_pixel_01(e) {
  var layer = e.target;

  layer.setStyle({
    color: 'red',
    weight: 1,
  });

  if(!L.Browser.ie && !L.Browser.opera && !L.Browser.edge){
    layer.bringToFront();
  }
}

function resetHighlight_pixel_01(e) {
  if(e.target != oldLayer){
    Pixel_01_Layer.resetStyle(e.target);
  }
}

var oldLayer = null;

function selectFeature_pixel_01(e) {

  if(oldLayer){
    Pixel_01_Layer.resetStyle(oldLayer);
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


function Pixel_01_Layer_onEachFeature(feature, layer) {
  var pixel_id = feature.properties.id;
  layer.bindPopup(feature.properties.popup_content);
  layer.on("click", function(e) {
    selected_pixel_id = feature.properties.id;
    selected_pixel01["latitude"] = feature.properties.latitude;
    selected_pixel01["longitude"] = feature.properties.longitude;
    selected_pixel01["resolution"] = feature.properties.resolution;
    selected_pixel01["data_model_name"] = "ERA5";
    
    selected_pixel = feature;

    chart.options.title.text = "Coordenadas " + feature.properties.latitude + "º, " + feature.properties.longitude + "º"
    botoes = true;
    selectFeature_pixel_01(e);
  });
  layer.on({
    mouseout: resetHighlight_pixel_01,
    mouseover: highlightFeature_pixel_01,
  })
}

var Pixel_01_Layer = L.geoJson([], {
  style: Pixel_01_Style,
  onEachFeature: Pixel_01_Layer_onEachFeature,
});



function loadPixel_01_Layer(){
  var url_pixels_01 = $("#url-pixels-01").val();
  $.getJSON(url_pixels_01, function(data) {
    Pixel_01_Layer.addData(data);
  })
  control.addOverlay(Pixel_01_Layer, "pixels 01");
  layers_dic["era5-01"] = Pixel_01_Layer;
}

function Show_Pixel01_Data(selected_pixel, startDate, finalDate){
  var url_pixels_01 = $("#url-pixels-01").val();
  startDateList = startDate.split("/");
  finalDateList = finalDate.split("/");
  console.log(selected_pixel);

  selected_pixel01["startDate"] = startDateList[2] + "-" + startDateList[1] + "-" + startDateList[0];
  selected_pixel01["finalDate"] = finalDateList[2] + "-" + finalDateList[1] + "-" + finalDateList[0];

  $.getJSON("/plataforma/api/pixeldata/", selected_pixel01, function(data) {
    console.log(data);
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
      case "umidade relativa":
        variable = 'relHum';
        break;
      default:
        variable = 'evapo';
        break;
    }
    chart_update2(chart, data, variable);
  })
}

function Download_Pixel01_Data(pixel_id, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  var url = url_pixels + "csv/" + pixel_id + "/" + selBox_model_display.value + "/" +startDate + "/" + finalDate;
  window.location.href = url;
}

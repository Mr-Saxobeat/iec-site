var ETA_Pixel_Style = {
  color: "green",
  weight: 0.5,
};
var selected_pixel_id;
function ETA_Pixel_Layer_onEachFeature(feature, layer) {
  var pixel_id = feature.properties.id;
  layer.bindPopup(feature.properties.popup_content);
  layer.on("click", function() {
    selected_pixel_id = feature.properties.id;
  });
}

var ETA_Pixel_Layer = L.geoJson([], {
  style: ETA_Pixel_Style,
  onEachFeature: ETA_Pixel_Layer_onEachFeature,
});

var url_pixels = $("#url-pixels").val();

function loadETALayer(){
  $.getJSON(url_pixels, function(data) {
    ETA_Pixel_Layer.addData(data);
  })
  control.addOverlay(ETA_Pixel_Layer, "pixels");
  layers_dic["eta por pixel"] = ETA_Pixel_Layer;
}

function Show_ETA_Data(pixel_id, startDate, finalDate){
  for(var i = 0; i <= 2; i++){
    startDate = startDate.replace("/", "-");
    finalDate = finalDate.replace("/", "-");
  }

  $.getJSON(url_pixels + "json/" + pixel_id + "/" + startDate + "/" + finalDate, function(data) {
    console.log(data);
    var variable = 'evapo';
    switch (selBox_variable_display.value.toLowerCase()) {
      case 'evapotranspiração':
        variable = 'evapo'
        break;
      case 'umidade relativa':
        variable = 'relHum';
        break;
      case 'radiação solar':
        variable = 'solarIns';
        break;
      case 'temperatura máxima':
        variable = "maxTemp";
        break;
      case 'temperatura mínima':
        variable = "minTemp";
        break;
      case 'velocidade do vento':
        variable = 'windSpeed';
        break;
      default:
        variable = 'evapo';
        break;
    }
    chart_update(chart, data, variable);
  })
}

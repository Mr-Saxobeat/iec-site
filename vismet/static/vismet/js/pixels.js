var ETA_Pixel_Style = {
  color: "green",
  weight: 0.5,
};

function ETA_Pixel_Layer_onEachFeature(feature, layer) {
  var pixel_id = feature.properties.id;
  layer.bindPopup(feature.properties.popup_content);
  layer.on("click", function() {
  });
}

var ETA_Pixel_Layer = L.geoJson([], {
  style: ETA_Pixel_Style,
  onEachFeature: ETA_Pixel_Layer_onEachFeature,
});

function loadETALayer(){
  var url_pixel = $("#url-pixels").val();
  $.getJSON(url_pixel, function(data) {
    ETA_Pixel_Layer.addData(data);
  })
  control.addOverlay(ETA_Pixel_Layer, "pixels");
  layers_dic["eta por pixel"] = ETA_Pixel_Layer;
}

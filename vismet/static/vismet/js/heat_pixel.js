//
var heat_pixel_style = {
  stroke: false,
  fillColor: 'white',
  fillOpacity: 0.2,
  radius: 5,
};

//
// var heat_pixel = L.geoJson([], {
//     style: heat_pixel_style,
//     pointToLayer: function(feature, latlng) {
//       lat = feature.coords[0];
//       lng = feature.coords[1];
//       console.log(lat + ' ' + lng);
//       latlng = L.latLng(lat, lng);
//       return new L.CircleMarker(latlng, {radius: 5});
//     },
// });

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

$.ajax({
  url: "api/pixeldata/",
  dataType: 'json',
  success: function (data) {

    // console.log('ajax');
    // data.forEach(dt => {
    //   if(dt.preciptation > 0){
    //       heat_pixel_style['fillOpacity'] = 0.5;
    //   }
    //   heat_pixel_style['fillColor'] = rgbToHex(parseInt(dt.preciptation) * 255, 255, 255);
    //   var circle = L.circleMarker(dt.coords, heat_pixel_style);
    //   circle.bindPopup("Precipitação: " + dt.preciptation);
    //   circle.addTo(map);
    //   heat_pixel_style['fillOpacity'] = 0.2;
    //
    // });


  },
  error: function (error) {
    console.log(error)
  }
}
)

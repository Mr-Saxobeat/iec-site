var ANA_Precip_Style = {
  fillColor: 'green',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

var ANA_Flow_Style = {
  fillColor: 'purple',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

function ANAStations_Layer_onEachFeature(feature, layer){

}

var ANA_Precip_Layer = L.geoJson([], {
    style: ANA_Precip_Style,
    pointToLayer: function(feature, latlng) {
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: ANAStations_Layer_onEachFeature,
});

var ANA_Flow_Layer = L.geoJson([], {
    style: ANA_Flow_Style,
    pointToLayer: function(feature, latlng) {
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: ANAStations_Layer_onEachFeature,
});

function loadANALayer(){
  $.getJSON(url_stations + 'json/ana/' , function (data) {
    data.forEach(station => {
      station_geojson = {
        "type": "Feature",
        "properties": {
          "omm_code": station.fields.omm_code,
          "inmet_code": station.fields.inmet_code,
          "state": station.fields.state,
          "city": station.fields.city,
          "type": station.fields.type,
          "startDate": station.fields.startDate,
          "finalDate": station.fields.finalDate,
        },
        "geometry": {
          "type": "Point",
          "coordinates": [station.fields.longitude, station.fields.latitude],
        }
      }

      if(station.fields.type == "Fluviométrica"){
        ANA_Precip_Layer.addData(station_geojson);
      }else if(station.fields.type == "Pluviométrica"){
        ANA_Flow_Layer.addData(station_geojson);
      }
    });
  });
  control.addOverlay(ANA_Precip_Layer, "ANA Pluviométrica");
  control.addOverlay(ANA_Flow_Layer, "ANA Fluviométrica");
}

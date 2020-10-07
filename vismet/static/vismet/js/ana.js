var ANAStations_Style = {
  fillColor: 'green',
  weight: 1,
  opacity: 1,
  color: 'black',
  fillOpacity: 1,
};

function ANAStations_Layer_onEachFeature(feature, layer){

}

var ANAStations_Layer = L.geoJson([], {
    style: ANAStations_Style,
    pointToLayer: function(feature, latlng) {
      return new L.CircleMarker(latlng, {radius: 5});
    },
    onEachFeature: ANAStations_Layer_onEachFeature,
});

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

    ANAStations_Layer.addData(station_geojson);
  });
});

control.addOverlay(ANAStations_Layer, "Estações ANA");

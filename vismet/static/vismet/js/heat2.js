$.ajax({
  url: "pixel/",
  dataType: 'json',
  success: function (data) {
    data.features.forEach(ft => {
      bounds = JSON.parse(ft.properties.boundings);
      var rec = L.rectangle(bounds, {color: "#ff7800", weight: 1});
      rec.bindPopup("Coordenadas: " + ft.geometry.coordinates[0] + ", " + ft.geometry.coordinates[1]);
      rec.addTo(map);
    });

  },
  error: function (error) {
    console.log(error)
  }
}
)

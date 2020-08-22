$.ajax({
  url: "pixel/",
  dataType: 'json',
  success: function (data) {
    data.features.forEach(ft => {
      bounds = JSON.parse(ft.properties.boundings);
      var rec = L.rectangle(bounds, {color: "#ff7800", weight: 1});
      rec.bindPopup("Coordenadas: " + ft.geometry.coordinates[0] + ", " + ft.geometry.coordinates[1]);
      // rec.on("click",
      //   $.ajax({
      //       // url: 'api/pixeldata/' + ft.geometry.coordinates[0] + '/' + ft.geometry.coordinates[1] + '1-1-1960/31-12-1960',
      //       url: "pixel/",
      //       dataType: 'json',
      //       success: function (data) {
      //         console.log(data);
      //       },
      //     }),
      //   ),
      rec.addTo(map);
    });

  },
  error: function (error) {
    console.log(error)
  }
}
)

$.ajax({
  url: "cities/",
  dataType: 'json',
  success: function (data) {
    data.features.forEach(ft => {
      latlngs = []
      ft.geometry.coordinates[0].forEach(pt => {
        latlngs.push(pt.reverse());
      });

      var name = ft.properties.nome;

      var pl = L.polygon(latlngs, {color:'black'});
      pl.bindPopup("Nome: " + name);
      pl.addTo(map);
    });

  },
  error: function (error) {
    console.log(error)
  }
}
)

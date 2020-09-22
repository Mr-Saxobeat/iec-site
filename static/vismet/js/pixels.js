/* function to save JSON to file from browser
* adapted from http://bgrins.github.io/devtools-snippets/#console-save
* @param {Object} data -- json object to save
* @param {String} file -- file name to save to
*/
function saveJSON(data, filename){

    if(!data) {
        console.error('No data')
        return;
    }

    if(!filename) filename = 'console.json'

    if(typeof data === "object"){
        data = JSON.stringify(data, undefined, 4)
    }

    var blob = new Blob([data], {type: 'text/json'}),
        e    = document.createEvent('MouseEvents'),
        a    = document.createElement('a')

    a.download = filename
    a.href = window.URL.createObjectURL(blob)
    a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
    e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
    a.dispatchEvent(e)
}

var boundings = [];
var points = [];

pixels_layer_style = {
  color: "green",
  weight: 0.5,
};

var pixel_master_id;

function onEachFeature(feature, layer) {
  var pixel_id = feature.properties.id;
  var popupContent = "Id: " + pixel_id + "<br>Coord: " + feature.properties.coordinates;
  layer.bindPopup(popupContent);
  layer.on("click", function() {
    pixel_master_id = pixel_id;
  });
}

var btn_pixel = $("#btn_pixel");
btn_pixel.click(
  function() {
    var pixel_id = pixel_master_id;
    var pixel_startDate = $("#pixel_startDate").val();
    var pixel_finalDate = $("#pixel_finalDate").val();

    for(i = 0; i < 2; i++){
      pixel_startDate = pixel_startDate.replace("/", "-");
      pixel_finalDate = pixel_finalDate.replace("/", "-");
    }

    console.log("ID = " + pixel_id);
    console.log("d1 = " + pixel_startDate);
    console.log("d2 = " + pixel_finalDate);

    $.getJSON("http://127.0.0.1:8000/api/pixels/csv/" + pixel_id + "/" + pixel_startDate + "/" + pixel_finalDate,
    function (data) {
      console.log(data);
      saveJSON(data, "timestamp.json");
    })
  })


var pixels_layer = L.geoJson([], {
  style: pixels_layer_style,

  onEachFeature: onEachFeature,
});

var url_pixels = $("#pixels-geojson").val();

$.getJSON(url_pixels, function(data) {
  var i = 0;
  data.features.forEach(ft => {
    boundings = JSON.parse(ft.properties.boundings);

    // Leaflet pede longitude e latitude, por isso
    // aqui a ordem das coordenadas é invertida.
    //boundings[0] = boundings[0].reverse();
    //boundings[1] = boundings[1].reverse();

    var points = [
      boundings[0],
      [ boundings[1][0], boundings[0][1] ],
      boundings[1],
      [ boundings[0][0], boundings[1][1] ]
    ];

    var geoJsonFeature = {
      "type": "Feature",
      "properties": {
        "id": ft.id,
        "coordinates": [ft.properties.longitude, ft.properties.latitude],
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [points],
      }
    };

    pixels_layer.addData(geoJsonFeature);
  });
})

control.addOverlay(pixels_layer, "Pixels");

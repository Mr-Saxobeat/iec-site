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
  layer.bindPopup(feature.properties.popup_content);
  layer.on("click", function() {
    pixel_master_id = pixel_id;
  });
}

var url_pixel = $("#url-pixels").val();

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

    window.location = url_pixel + "csv" + "/" + pixel_id + "/" + pixel_startDate + "/" + pixel_finalDate;
  })


var pixels_layer = L.geoJson([], {
  style: pixels_layer_style,

  onEachFeature: onEachFeature,
});

$.getJSON(url_pixel, function(data) {
  var i = 0;
  pixels_layer.addData(data);
})

control.addOverlay(pixels_layer, "Pixels");

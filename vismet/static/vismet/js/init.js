
var selected_source = document.getElementById("selected_source").value;
var url_stations = document.getElementById("url-stations").value;
var url_data_options = document.getElementById("url-data-options").value;
var url_api = document.getElementById("url-api").value;

// Essa variável armazena as opções que poderão ser selecionadas
// de acordo com a categoria, fonte, modelo.
$.getJSON(url_data_options, function (data) {
  createNewChart('line');

  json_data_options = JSON.parse(JSON.stringify(data));
  loadXavierLayer();
  loadANALayer();
  loadINMETLayer();
  loadETALayer();
  LoadETACity();

  if(selected_source != "None"){
    var splited = selected_source.split(";");
    var selected_category = splited[0];
    selected_source = splited[1];


    showCategoryData(selected_category);
    for(var i = 0; i < selBox_source_display.options.length; i++){
      opt = selBox_source_display.options[i];
      if(opt.value.toLowerCase() == selected_source){
        opt.selected = true;
        showLayer(selected_source);

        setVariableSelection(selBox_variable_display, selected_source);
      }
    }
  }
  else{
    showCategoryData("observados");
    map.addLayer(layers_dic["ana"]);
  }
});


var btn_submit = document.getElementById("btn_submit");
var btn_download = document.getElementById("btn_download");
var input_station_code = document.getElementById("input_station_code");
var input_city_name = document.getElementById("input_city_name");
var input_startDate = document.getElementById("startDate");
var input_finalDate = document.getElementById("finalDate");

btn_submit.addEventListener("click", function() {
  if (selBox_source_display.value.toUpperCase() == "ANA"){
    Show_ANA_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  } else if (selBox_source_display.value.toUpperCase() == "INMET"){
    Show_INMET_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  } else if (selBox_source_display.value.toUpperCase() == "XAVIER"){
    Show_Xavier_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  }else if (selBox_source_display.value.toUpperCase() == "ETA POR CIDADE"){
    Show_City_Data(input_city_name.value, input_startDate.value, input_finalDate.value);
  }else if (selBox_source_display.value.toUpperCase() == "ETA POR PIXEL"){
    Show_ETA_Data(selected_pixel_id, input_startDate.value, input_finalDate.value);
  }else if(selBox_source_display.value.toUpperCase() == 'CHIRPS'){
    Show_Chirps_Data(selected_pixel, input_startDate.value, input_finalDate.value);
  }
})

btn_download.addEventListener("click", function() {
  if (selBox_source_display.value.toUpperCase() == "ANA"){
    Download_ANA_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  } else if (selBox_source_display.value.toUpperCase() == "INMET"){
    Download_INMET_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  } else if (selBox_source_display.value.toUpperCase() == "XAVIER"){
    Download_Xavier_Data(input_station_code.value, input_startDate.value, input_finalDate.value);
  }else if (selBox_source_display.value.toUpperCase() == "ETA POR CIDADE"){
    Download_City_Data(input_city_name.value, input_startDate.value, input_finalDate.value);
  }else if (selBox_source_display.value.toUpperCase() == "ETA POR PIXEL"){
    Download_ETA_Data(selected_pixel_id, input_startDate.value, input_finalDate.value);
  }
})

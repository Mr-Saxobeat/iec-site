
var selected_source = document.getElementById("selected_source").value;
var url_stations = document.getElementById("url-stations").value;
var url_data_options = document.getElementById("url-data-options").value;

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
    showCityData(input_city_name.value, input_startDate.value, input_finalDate.value);
  }
})

var json_data_options = [];
var json_current_category = [];

var selBox_source_display = null;
var selBox_variable_display = null;
var selBox_chart_max_value = null;
var selBox_chart_min_value = null;

var divObservedData = document.getElementById("div-observados");
var divReanaliseData = document.getElementById("div-reanálise");
var divSimulatedData = document.getElementById("div-simulados");

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function variable_display_change(selBox_source, selBox_variable, selBox_chart_max_value, selBox_chart_min_value){
  var selected_source = selBox_source.value;
  var selected_variable = selBox_variable.value;
  var y_max_value = selBox_chart_max_value.value
  var y_min_value = selBox_chart_min_value.value

  if(selected_source.toLowerCase() == 'ana'){
    if(selected_variable.toLowerCase() == 'precipitação'){
      showLayer('ana-precip');
    }else if(selected_variable.toLowerCase() == 'vazão'){
      showLayer('ana-flow');
    }
  }

  var chartType = json_current_category["sources"][selected_source][selected_variable]["chartType"];
  var chartColor = json_current_category["sources"][selected_source][selected_variable]["chartColor"];
  var chartUnit = json_current_category["sources"][selected_source][selected_variable]["unit"];
  createNewChart(chartType, chartColor, chartUnit, capitalizeFirstLetter(selected_variable), y_max_value, y_min_value);
  chart.update();
}

// selectBox: DOM select object
function removeAllOptions(selectBox){
  while(selectBox.options.length > 0){
    selectBox.remove(0);
  }
}

function showLayer(layer_name){

  for (var layer in layers_dic) {
    map.removeLayer(layers_dic[layer]);
  }

  if(layer_name == "ana"){
    layer_name = "ana-precip";
  }

  var curLay = layers_dic[layer_name];
  map.addLayer(curLay);
  curLay.bringToFront();
}

function capitalize(word){
  capitalized = "";
  words = word.split(" ");
  words.forEach(wrd => {
    capitalized += wrd[0].toUpperCase() + wrd.slice(1).toLowerCase() + " ";
  });

  return capitalized;
}

// selectBox: DOM select object;
// source: json of the selected data source,
// it's a child of json_current_category object.
function setModelSelection(selectBox, selected_source){
  removeAllOptions(selectBox);
  var available_models = json_current_category['sources'][selected_source]['models'];

  available_models.forEach(model => {
    newOpt = new Option(model, model);
    selectBox.add(newOpt, undefined);
  });
}

// selectBox: DOM select object;
// source: json of the selected data source,
// it's a child of json_current_category object.
function setVariableSelection(selectBox, selected_source){
  removeAllOptions(selectBox);
  var available_variables = json_current_category['sources'][selected_source];

  for (var key in available_variables){
    if(key == 'models' || key == 'display_name'){
      continue;
    }
    newOpt = new Option(capitalize(key), key);
    selectBox.add(newOpt, undefined);
  }
}

// Essa função adiciona as opções no menu de seleção
// de fontes de dados disponíveis para a categoria escolhida.
// selectBox: DOM select object
function setSourceDataSelection(selectBox){
  removeAllOptions(selectBox);
  var newOpt;
  Object.keys(json_current_category['sources']).forEach(source => {
    newOpt = new Option(json_current_category['sources'][source]["display_name"], source);
    selectBox.add(newOpt, undefined);
  });
}

// Esta função irá mostrar o menu e as layers referentes à categoria de dados
// a partir do botão clicado "observardos", "reanálise" ou "simulados".
// div_last_name: string with the last name of id's div
function showCategoryData(div_last_name){
  // Esconde todas divs
  divObservedData.style.display = "none";
  divReanaliseData.style.display = "none";
  divSimulatedData.style.display = "none";

  // Pega a div selecionada a partir do valor passado pelo parâmetro
  // e então exibe somente ela.
  var selectedDiv = document.getElementById("div-" + div_last_name);
  selectedDiv.style.display = "block";

  json_current_category = json_data_options[div_last_name]

  selBox_source_display = selectedDiv.getElementsByClassName("sel-data-source")[0];
  selBox_variable_display = selectedDiv.getElementsByClassName("sel-data-variable")[0];
  selBox_model_display = selectedDiv.getElementsByClassName("sel-data-model")[0];
  selBox_chart_max = selectedDiv.getElementsByClassName("sel-chart-max-value")[0];
  selBox_chart_min = selectedDiv.getElementsByClassName("sel-chart-min-value")[0];
  setSourceDataSelection(selBox_source_display, json_current_category);

  selBox_source_display.addEventListener("change", function() {
    if(selBox_model_display != undefined){
      setModelSelection(selBox_model_display, selBox_source_display.value);
    }
    setVariableSelection(selBox_variable_display, selBox_source_display.value);
    showLayer(selBox_source_display.value);

    variable_display_change(selBox_source_display, selBox_variable_display, selBox_chart_max, selBox_chart_min);
    });

  selBox_variable_display.addEventListener("change", function() {
    variable_display_change(selBox_source_display, selBox_variable_display, selBox_chart_max, selBox_chart_min);
  })

  selBox_chart_max.addEventListener("change", function() {
    chart.options.scales.yAxes[0].ticks.max = parseFloat(selBox_chart_max.value);
    chart.options.scales.yAxes[0].ticks.min = parseFloat(selBox_chart_min.value);
    chart.update();
  })

  var evt = document.createEvent("HTMLEvents");
  evt.initEvent("change", false, true);
  selBox_source_display.dispatchEvent(evt);
  selBox_variable_display.dispatchEvent(evt);
}

// Armazena os botões de categorias em variáveis e adiciona um listener
// para click em cada um deles.
var btnObservedData = document.getElementById("btn-observados");
var btnReanaliseData = document.getElementById("btn-reanálise");
var btnSimulatedData = document.getElementById("btn-simulados");
btnObservedData.addEventListener("click", function() {
  showCategoryData(btnObservedData.value);
});
btnReanaliseData.addEventListener("click", function() {
  showCategoryData(btnReanaliseData.value);
});
btnSimulatedData.addEventListener("click", function() {
  showCategoryData(btnSimulatedData.value);
});

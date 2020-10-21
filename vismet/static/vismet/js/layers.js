var json_data_options = [];
var json_current_category = [];

var selBox_source_display = null;
var selBox_variable_display = null;

var divObservedData = document.getElementById("div-observados");
var divReanaliseData = document.getElementById("div-reanálise");
var divSimulatedData = document.getElementById("div-simulados");

function variable_display_change(selBox_source, selBox_variable){
  if(selBox_source.value == 'ana'){
    var selected_variable = selBox_variable.value.toUpperCase();
    if(selected_variable == 'PRECIPITAÇÃO'){
      showLayer('ana-precip');
    }else if(selected_variable == 'VAZÃO'){
      showLayer('ana-flow');
    }
  }
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

  map.addLayer(layers_dic[layer_name]);
}

// selectBox: DOM select object;
// source: json of the selected data source,
// it's a child of json_current_category object.
function setVariableSelection(selectBox, selected_source){
  removeAllOptions(selectBox);
  var available_variables = null;

  json_current_category.sources.forEach(source => {
    if(source.name == selected_source){
      available_variables = source.variables;
    }
  });

  var newOpt;
  available_variables.forEach(variable => {
    newOpt = new Option(variable, variable);
    selectBox.add(newOpt, undefined);
  });
}

// Essa função adiciona as opções no menu de seleção
// de fontes de dados disponíveis para a categoria escolhida.
// selectBox: DOM select object
function setSourceDataSelection(selectBox){
  removeAllOptions(selectBox);
  var newOpt;
  json_current_category.sources.forEach(source => {
    newOpt = new Option(source.name, source.name);
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

  for(i = 0; i <= 10; i++){ // O valor de i <= foi arbitrário!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if(json_data_options[i].category == div_last_name){
      // Esta variável carrega o json com a categoria atual e suas fontes
      // e variáveis de cada fonte. Ela é usada nas outras funções.
      json_current_category = json_data_options[i];
      break;
    }
  }

  selBox_source_display = selectedDiv.getElementsByClassName("sel-data-source")[0];
  selBox_variable_display = selectedDiv.getElementsByClassName("sel-data-variable")[0];
  setSourceDataSelection(selBox_source_display, div_last_name);

  selBox_source_display.addEventListener("change", function() {
    setVariableSelection(selBox_variable_display, selBox_source_display.value);
    showLayer(selBox_source_display.value);
    });
  var evt = document.createEvent("HTMLEvents");
  evt.initEvent("change", false, true);
  selBox_source_display.dispatchEvent(evt);

  selBox_variable_display.addEventListener("change", function() {
    variable_display_change(selBox_source_display, selBox_variable_display);
  })

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

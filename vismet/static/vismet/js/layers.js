var json_data_options = [];
var json_current_category = [];

var divObservedData = document.getElementById("div-observados");
var divReanaliseData = document.getElementById("div-reanálise");
var divSimulatedData = document.getElementById("div-simulados");

// selectBox: DOM select object
function removeAllOptions(selectBox){
  while(selectBox.options.length > 0){
    selectBox.remove(0);
  }
}

// selectBox: DOM select object;
// source: json of the selected data source,
// it's a child of json_current_category object.
function setVariableSelection(selectBox, source){
  removeAllOptions(selectBox);
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

  var selectBox = selectedDiv.getElementsByClassName("sel-data-source")[0];
  setSourceDataSelection(selectBox, div_last_name);
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

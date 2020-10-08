// Esta função irá mostrar o menu e as layers referentes à categoria de dados
// a partir do botão clicado "observardos", "reanálise" ou "simulados".
var json_data_options = [];
var current_category = [];

var divObservedData = document.getElementById("div-observados");
var divReanaliseData = document.getElementById("div-reanálise");
var divSimulatedData = document.getElementById("div-simulados");

function loadJSONDataOptions(data){
  json_data_options = data;
}

function removeAllOptions(selectBox){
  while(selectBox.options.length > 0){
    selectBox.remove(0);
  }
}

function setVariableSelection(selectBox, source){
  removeAllOptions(selectBox);
  var i;


}

function setSourceDataSelection(selectBox){
  removeAllOptions(selectBox);
  var newOpt;
  current_category.sources.forEach(source => {
    newOpt = new Option(source.name, source.name);
    selectBox.add(newOpt, undefined);
  });
}

function showCategoryData(div_last_name){
  divObservedData.style.display = "none";
  divReanaliseData.style.display = "none";
  divSimulatedData.style.display = "none";

  var selectedDiv = document.getElementById("div-" + div_last_name);
  selectedDiv.style.display = "block";
  var i = 0;

  for(i = 0; i <= 10; i++){ // O valor de i <= foi arbitrário!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if(json_data_options[i].category == div_last_name){
      current_category = json_data_options[i];
      break;
    }
  }

  var selectBox = selectedDiv.getElementsByClassName("sel-data-source")[0];
  setSourceDataSelection(selectBox, div_last_name);
}

var btnObservedData = document.getElementById("btn-observados");
var btnReanaliseData = document.getElementById("btn-reanálise");
var btnSimulatedData = document.getElementById("btn-simulados");

btnObservedData.addEventListener("click", function() {
  console.log("clicou " + btnObservedData.value);
  showCategoryData(btnObservedData.value);
});

btnReanaliseData.addEventListener("click", function() {
  console.log("clicou " + btnReanaliseData.value);
  showCategoryData(btnReanaliseData.value);
});

btnSimulatedData.addEventListener("click", function() {
  console.log("clicou " + btnSimulatedData.value);
  showCategoryData(btnSimulatedData.value);
});

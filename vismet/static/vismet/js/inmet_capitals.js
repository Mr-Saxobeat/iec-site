function pegaData(id) {
 $("#" + id).datepicker({
   showOn: 'focus',
   dateFormat: 'dd/mm/yy',
   dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
   dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
   dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
   defaultDate: new Date(2020, 08, 01),
   monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
   monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
   nextText: 'Próximo',
   prevText: 'Anterior',
   minDate: new Date(1980, 0, 1),
   maxDate: new Date(2022, 12, 31),
   changeYear: true,
   changeMonth: true,
 });
}

var date_box = $("#date")[0];
date_box.onfocus = function(){ pegaData(this.id); };

var btn_capitals = $("#btn_capitals");
var url = "https://apitempo.inmet.gov.br/condicao/capitais/";

btn_capitals.click(function () {
  var date = date_box.value;
  var day = date.substring(0, 2);
  var month = date.substring(3, 5);
  var year = date.substring(6, 10);

  $.getJSON(url + year + "-" + month + "-" + day,
    function(data) {
      removeData(chart);
      updateChart(data);
    })

});

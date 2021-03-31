$("#btn_submit, #btn_download").prop('disabled', true);


var botoes = botoes;

var toValidate = $('#startDate, #finalDate'),
    valid = false;
    
toValidate.change(function () {
    if ($(this).val().length === 0) {
        $(this).data('valid', false);
    } else {
        $(this).data('valid', true);
    }
    toValidate.each(function () {
        if ($(this).data('valid') == true) {
            valid = true;
        } else {
            valid = false;
        }
    });

    if (valid === true && botoes == true){
        jQuery("#btn_submit, #btn_download").prop('disabled', false);
    } else {
        jQuery("#btn_submit, #btn_download").prop('disabled', true);
    }
}); // Validação para liberação dos botões

$(document).ready(function(){
  $("#btn_submit").click(function(){
    $("#chartdownload, .chart-container").show();
  });
});

$(document).ready(function(){
  $("getData").on("click",function(){
    $.ajax({
      type:"GET",
      url:"https://apitempo.inmet.gov.br/estacoes",
      beforeSend: function(){
        $("loader").show();
      },
      complete: function(){
        $("loader").hide();
      },
    });
  });
  selfinalYear = finalDate.substring(6);
  tempogrande = finalDate - startDate
}); // TBD

function screenshot(){
    html2canvas(document.getElementById("chartdownload")).addEventListener('click', function(){canvas=>{
      var url_base64jp = document.getElementById("chart").toDataURL("image/png");
      var a =  document.getElementById("chartdownload");
      a.href = url_base64jp;
    }
  });
}

function screenshot(){
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;  
  html2canvas(document.getElementById("chart")).then(canvas=>{
    var image = canvas.toDataURL("image/png").replace("image/png","image/octet-stream");  
    window.location.href=image
  });
}

$("#btn_submit").click(function() {
  $("html, body").animate({ scrollTop: $(document).height() });
  return false;
}); // Sobe a página ao clicar em Visualizar



$(document).ready(function(){
    $('.frequency').on('change', function() {
      if ( this.value == '1')
      {
        $(".day").show();
        $(".month").hide();
      }
      else
      {
        $(".day").hide();
        $(".month").show();
      }
    });
}); // Muda o tipo de seleção exibida, diária ou mensal, ao clicar no radio button

$(".w3-bar-item").click(function () {
  $(".frequency").prop('checked', false);
  $(".day, .month").hide();
}); // Esconde os campos de imput de data quando outra categoria é selecionada

$(".frequency").click(function(event){
  var $msd = $("#startDate");
  var $month = $("#startMonth");
  var $year = $("#startYear");

  let min;
  let max;
  if (event.target.id === "simulal"){
    $('#startYear, #finalYear').empty();
    min = 1960
    max = 2099
  } else{
    $('#startYear, #finalYear').empty();
    min = 1979
    max = 2021
  }

  $('select').change(function () {
    var val = "01/" + $month.val() + "/" + $year.val();
      $msd.val(val);
  });

    select = document.getElementById('startYear');

    for (var i = min; i<=max; i++){
       var opt = document.createElement('option');
       opt.value = i;
       opt.innerHTML = i;
       select.appendChild(opt);
    }

    var $mfd = $("#finalDate");
    var $monthf = $("#finalMonth");
    var $yearf = $("#finalYear");
    
  $('select').change(function () {
    var val = "01/" + $monthf.val() + "/" + $yearf.val();
      $mfd.val(val);
  });
  
    selectf = document.getElementById('finalYear');

    for (var i = min; i<=max; i++){
        var opt = document.createElement('option');
        opt.value = i;
        opt.innerHTML = i;
        selectf.appendChild(opt);
    }
}); // Função para gerar os anos do monthpicker

$('input:radio').on('click', function() {
  if($(this).attr('class') == 'frequency') {
      $('input:text#startDate, input:text#finalDate').val('');
      if (botoes == true){
        $("#btn_submit, #btn_download").prop('disabled', false);
      }
  } 
}); // TBD

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
});

$(document).ready(function(){
  $("#btn_submit").click(function(){
    $("#chartdownload, .chart-container").show();
  });
});

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
});
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
    $("#chart_download, .chart-container").show();
  });
});
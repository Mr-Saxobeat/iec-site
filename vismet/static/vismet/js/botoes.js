$("#btn_submit, #btn_download").prop('disabled', true);

var toValidate = $('#startDate, #finalDate'),
    valid = false;

var mapa = botoes;

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

    if (valid === true && botoes == 1){
        jQuery("#btn_submit, #btn_download").prop('disabled', false);
    } else {
        jQuery("#btn_submit, #btn_download").prop('disabled', true);
    }
});


$("#startDate, #finalDate").datepicker();

$("#finalDate").change(function () {
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("finalDate").value;
 
    if ((Date.parse(endDate) < Date.parse(startDate))) {
        alert("A data final deve ser maior do que a inicial");
        document.getElementById("finalDate").value = "";
    }
});
$("#startDate, #finalDate").datepicker();

$("#finalDate").change(function () {
    var startDate = document.getElementById("startDate").value;
    var finalDate = document.getElementById("finalDate").value;
 
    if ((Date.parse(finalDate) <= Date.parse(startDate))) {
        alert("A data final deve ser maior do que a inicial");
        document.getElementById("finalDate").value = "";
    }
});
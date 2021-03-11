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
});

$(document).ready(function() {
  const monthNames = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
  let qntYears = 4;
  let selectYear = $("#year");
  let selectMonth = $("#month");
  let selectDay = $("#day");
  let currentYear = new Date().getFullYear();

  for (var y = 0; y < qntYears; y++) {
    let date = new Date(currentYear);
    let yearElem = document.createElement("option");
    yearElem.value = currentYear
    yearElem.textContent = currentYear;
    selectYear.append(yearElem);
    currentYear--;
  }

  for (var m = 0; m < 12; m++) {
    let month = monthNames[m];
    let monthElem = document.createElement("option");
    monthElem.value = m;
    monthElem.textContent = month;
    selectMonth.append(monthElem);
  }

  var d = new Date();
  var month = d.getMonth();
  var year = d.getFullYear();
  var day = d.getDate();

  selectYear.val(year);
  selectYear.on("change", AdjustDays);
  selectMonth.val(month);
  selectMonth.on("change", AdjustDays);

  AdjustDays();
  selectDay.val(day)

  function AdjustDays() {
    var year = selectYear.val();
    var month = parseInt(selectMonth.val()) + 1;
    selectDay.empty();

    //get the last day, so the number of days in that month
    var days = new Date(year, month, 0).getDate();

    //lets create the days of that month
    for (var d = 1; d <= days; d++) {
      var dayElem = document.createElement("option");
      dayElem.value = d;
      dayElem.textContent = d;
      selectDay.append(dayElem);
    }
  }
});


$(document).ready(function(){
  $('.frequency').on('change', function() {
    if ( this.value == '0')
    {
      var src = document.getElementById("startDate"),
      dst0 = document.getElementById("year");
      dst1 = document.getElementById("month");
      dst = "01/"+dst1+"/"+dst0

      src.addEventListener('input', function() {
          src.value = dst.value;
      });
    }
  });
});
var chart_data;
var chart_labels;
var intervals = ["HOURLY", "DAILY", "MONTHLY", "YEARLY"];

$("#btn_submit").click(function () {
  var model = "ETA";
  var model_id = $("#model-id").val();

  var interval_id = $("#intervale-id").val();
  var interval = intervals[interval_id - 1];

  var start_month = $("#start-month").val();
  var start_year = $("#start-year").val();

  var final_month = $("#final-month").val();
  var final_year = $("#final-year").val();

  var variable = $("#variable").val();

  var latitude = $("#latitude").val();
  var longitude = $("longitude").val();

  $.ajax({
    url: "https://projeta.cptec.inpe.br/api/v1/public/" + model + "/" + model_id + "/" +
          interval + "/" + interval_id + "/" + start_month + "/" + start_year + "/" +
          final_month + "/" + final_year + "/" + variable + "/" + latitude + "/" + longitude,
    dataType: 'json',
    success: function (data) {
      console.log(data);
    },
    error: function (error) {
      console.log(error);
    }
  })
})

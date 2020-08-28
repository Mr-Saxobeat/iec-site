var chart_data;
var chart_labels;

$("#btn_submit").click(function () {
  var ommCode = $("#input_ommcode").val();
  var startDate = $("#startDate").val();
  var finalDate = $("#finalDate").val();
  var variable = $("#variable").val();

  $.ajax({
    url: "ajaxrequest/",
    data: {
      'omm_code': ommCode,
      'startDate': startDate,
      'finalDate': finalDate,
    },
    dataType: 'json',
    success: function (data) {
      chart_data = data;
      updateChart(chart, variable);
    },
    error: function (error) {
      console.log(error)
    }
  });
});

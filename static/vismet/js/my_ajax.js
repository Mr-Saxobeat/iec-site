var chart_data;
var chart_labels;

$("#btn_submit").click(function () {
  var stationId = $("#input_stationId").val();
  var startDate = $("#startDate").val();
  var finalDate = $("#finalDate").val();
  var variable = $("#variable").val();

  $.ajax({
    url: "ajaxrequest/",
    data: {
      'stationId': stationId,
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

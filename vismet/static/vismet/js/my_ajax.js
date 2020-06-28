$("#btn_submit").click(function () {
  var stationId = $("#input_stationId").val();
  var startDate = $("#startDate").val();
  var finalDate = $("#finalDate").val();

  $.ajax({
    url: "ajaxrequest/",
    data: {
      'stationId': stationId,
      'startDate': startDate,
      'finalDate': finalDate,
    },
    dataType: 'json',
    success: function (data) {
      removeData(chart);
      console.log(data);

      data.forEach((obj) => {
        date = [String(obj.fields.date)];
        console.log(date);
        temp = [obj.fields.temp];

        addData(chart, date, temp);
        chart.update();
      });
    },
    error: function (error) {
      console.log(eval(error));
    }
  });
});

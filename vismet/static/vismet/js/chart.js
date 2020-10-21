var selectedOption = $("#variable");

// selectedOption.change(function () { updateChart(chart, selectedOption.val()); });

var chart = new Chart('chart', {
  options: {
    title: {
      display: true,
      fontSize: 0,
      text: '',
    },
    scales:{
        yAxes: [{
            display: true,
            labelString: "",
            fontColor: '#666',
        }],
        xAxes: [{
            display: true,
            labelString: "Data",
            fontColor: '#666',
        }],
    },
    legend: {
      display: false,
    }
  },
  type: 'line',
});

function chart_removeData(chart) {
  dtSet0 = chart.data.datasets[0];
  while(dtSet0.data.length > 0){
    dtSet0.data.pop();
    chart.data.labels.pop();
  }
}

function chart_addData(json_data, variable){
  json_data.forEach(data => {
    date = data.fields.date;
    date = date.substring(8,10) + '/' + date.substring(5,7) + '/' + date.substring(0,4);
    chart.data.labels.push(date);

    value = data.fields[variable];

    chart.data.datasets.forEach((dataset) => {
      dataset.data.push(value);
    });
  });
}

function chart_update(chart, json_data, variable){
  chart_removeData(chart);
  chart_addData(json_data, variable);
  chart.update();
}

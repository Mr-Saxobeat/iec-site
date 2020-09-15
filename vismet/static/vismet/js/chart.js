var selectedOption = $("#variable");

selectedOption.change(function () { updateChart(chart, selectedOption.val()); });

var chart = new Chart('chart', {
  options: {
    title: {
      display: true,
      fontSize: 20,
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
  data: {
    labels: [],
    datasets: [
      {
        data: [],
      }
    ]
  }
});

function removeData(chart) {
  dtSet0 = chart.data.datasets[0];
  while(dtSet0.data.length > 0){
    dtSet0.data.pop();
    chart.data.labels.pop();
  }
}

function addData(chart, labels, data) {
  labels.forEach((lb) => {
    date = lb.substring(8,10) + '/' + lb.substring(5,7) + '/' + lb.substring(0,4);
    chart.data.labels.push(date);
    });

    var dtSet = chart.data.datasets;

    chart.data.datasets.forEach((dataset) => {
      data.forEach((dt) => {
        if(dt == 0 || dt == "NaN" || dt == "-9999"){
          dataset.data.push(null);
        }
        else{
          dataset.data.push(dt);
        }
      });
    });
}

function updateChart(chart, variable){
        removeData(chart);
        chart_data.forEach((obj) => {
          array_date = [String(obj.fields.date)];
          array_data = [obj.fields[variable]];

          addData(chart, array_date, array_data);
          chart.update();
        });
}

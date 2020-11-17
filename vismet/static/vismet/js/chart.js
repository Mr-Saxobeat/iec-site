var selectedOption = $("#variable");

// selectedOption.change(function () { updateChart(chart, selectedOption.val()); });
var chart;
function createNewChart(type, color, unit, legend){
  if(chart){
    chart.destroy();
  }

  var config = {
    options: {
      title: {
        display: false,
        fontSize: 10,
        text: legend,
      },
      scales:{
        yAxes: [{
          fontColor: '#666',
          scaleLabel: {
            labelString: unit,
            display: true,
          }
        }],
        xAxes: [{
          display: true,
          labelString: "Data",
          fontColor: '#666',
        }],
      },
      legend: {
        display: true,
        labels: ["teste"]
      }
    },
    type: type,
    data: {
      datasets: [{
        data: [],
        borderColor: color,
      }]
    }
  }


  // var temp = jQuery.extend(true, {}, config);
  chart = new Chart('chart', config);

  if(type == 'bar'){
    chart.data.datasets[0].backgroundColor = color;
    chart.update();
  }

  chart.update();
}

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

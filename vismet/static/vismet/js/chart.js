var selectedOption = $("#variable");

// selectedOption.change(function () { updateChart(chart, selectedOption.val()); });
var chart;
function createNewChart(type, color, unit, legend_data, y_max_value, y_min_value){
  if(chart){
    chart.destroy();
  }

  var config = {
    options: {
      maintainAspectRatio: false,
      title: {
        display: true,
        fontSize: 20,
        text: "",
      },
      scales:{
        yAxes: [{
          scaleLabel: {
            labelString: unit,
            display: true,
          },
          ticks: {
            max: parseFloat(y_max_value),
            min: parseFloat(y_min_value),
          },
          // display: true,
          // labelString: "Data",
          fontColor: '#666',
        }],
        xAxes: [{
          ticks: {
            autoSkip: true,
            autoSkipPadding: 30,
            maxRotation: 0,
            minRotation: 0,
          },
          display: true,
          labelString: "Data",
          fontColor: '#666',
        }],
      },
      // legend: {
      //   display: true,
      //   labels: ["teste"]
      // }
    },
    type: type,
    data: {
      datasets: [{
        label: legend_data,
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
  var day;
  var month;
  var year;

  json_data.forEach(data => {
    date = data.fields.date;
    day = date.substring(8,10);
    month = date.substring(5,7);
    year = date.substring(2,4);

    

    if(json_current_category.name == "simulados" || 
       json_current_category.name == "reanálise"){
      date = month + '/' + year;
    }else{
      date = day + '/' + month + '/' + year;
    }
    
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


function chart_addData2(json_data, variable){
  var day;
  var month;
  var year;
  json_data.forEach(data => {
    date = data.date;
    day = date.substring(8,10);
    month = date.substring(5,7);
    year = date.substring(2,4);
    date = month + '/' + year;
    chart.data.labels.push(date);

    value = data[variable];
    chart.data.datasets.forEach((dataset) => {
      dataset.data.push(value);
    });
  });
}

function chart_update2(chart, json_data, variable){
  chart_removeData(chart);
  chart_addData2(json_data, variable);
  chart.update();
}

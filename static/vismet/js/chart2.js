var chart = new Chart('chart', {
  options: {
    title: {
      display: true,
      fontSize: 20,
      text: 'Temperaturas máximas:',
    },
      scales:{
          yAxes: [{
              display: true,
              labelString: "ºC",
              fontColor: '#666',
          }],
          xAxes: [{
              display: true,
              labelString: "Data",
              fontColor: '#666',
          }],
      },
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

function addData(label, dt) {

    chart.data.labels.push(label);

    var dtSet = chart.data.datasets;

    chart.data.datasets.forEach((dataset) => {

        if(dt == 0 || dt == "NaN"){
          dataset.data.push(null);
        }
        else{
          dataset.data.push(dt);
        }

    });

    chart.update();
}

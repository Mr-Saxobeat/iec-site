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
      display: true,
    }
  },
  type: 'bar',
  data: {
    labels: [],
    datasets: [
      {
        label: "Temperatura máxima",
        data: [],
        backgroundColor: "#eb6134",
      },
      {
        label: "Temperatura mínima",
        data: [],
        backgroundColor: "#348feb",
      }
    ]
  }
});

function removeData(chart) {
  dtSet0 = chart.data.datasets[0];
  dtSet1 = chart.data.datasets[1];

  while(dtSet0.data.length > 0){
    dtSet0.data.pop();
    chart.data.labels.pop();
  }

  while(dtSet1.data.length > 0){
    dtSet1.data.pop();
    chart.data.labels.pop();
  }
}

function updateChart(data){
  console.log(data);

  var dts_tMax = chart.data.datasets[0];
  var dts_tMin = chart.data.datasets[1];

  data.forEach(dt => {
    chart.data.labels.push(dt["CAPITAL"]);

    if(dt["TMAX18"] == "*"){
      dts_tMax.data.push(null);
    }
    else{
      dts_tMax.data.push(dt["TMAX18"]);
    }

    if(dt["TMIN18"] == "*"){
      dts_tMin.data.push(null);
    }
    else{
      dts_tMin.data.push(dt["TMIN18"]);
    }

    chart.update();

  });
}

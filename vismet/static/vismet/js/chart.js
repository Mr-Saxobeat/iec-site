
var myData;
var stationNum;
var optTempMax = $('#tempMax');
var optTempMin = $('#tempMin');
var optSolRad = $('#solRad');
var fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/f4ce6b69e5d3457ae52215edf57445c4/raw/705cfaf2cb35afc1b595495a7de9ca4b333c800a/tMax-inmet.csv';
var selectedOption;

d3.csv(fileUrl).then(getCsv);

function getCsv(csvData) {
  myData = csvData;
}

function choose(csvData){
    myData = csvData;
    updateChart(stationNum);
}

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
        if(dt == 0 || dt == "NaN"){
          dataset.data.push(null);
        }
        else{
          dataset.data.push(dt);
        }
      });
    });
}

function updateChart(id){
        stationNum = id;
        var stationData = myData[id];
        var labels = Object.keys(myData);

        labels.pop();

        var stationLevels = [];

        myData.forEach(dt => {
            stationLevels.push(dt[id]);
        });

        removeData(chart);
        addData(chart, labels, stationLevels);

        chart.update();
}

optTempMax.click(function(){
    fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/f4ce6b69e5d3457ae52215edf57445c4/raw/705cfaf2cb35afc1b595495a7de9ca4b333c800a/tMax-inmet.csv';
    chart.options.title.text = "Temperaturas máximas";
    d3.csv(fileUrl).then(choose);
});

optTempMin.click(function(){
    fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/208642a743eb6ef0bf649b6f1e1138e3/raw/968676550eb5f0acdba4140f82a79aefe6baf9e0/tMin-inmet.csv';
    chart.options.title.text = "Temperaturas mínimas";
    d3.csv(fileUrl).then(choose);
});

optSolRad.click(function(){
    fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/afb28a15b4497e6c0ac255779523fb02/raw/27c0b7273acd6b5ce57353f1e00b3bc95ac956f3/sRadiation-inmet.csv';
    chart.options.title.text = "Radiação solar";
    d3.csv(fileUrl).then(choose);
})

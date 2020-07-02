var myData;
var stationNum;
var optTempMax = $('#tempMax');
var optSolRad = $('#solRad');
var optTempMin = $('#tempMin');
var fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/f4ce6b69e5d3457ae52215edf57445c4/raw/705cfaf2cb35afc1b595495a7de9ca4b333c800a/tMax-inmet.csv';
var selectedOption;

d3.csv(fileUrl).then(getCsv);

function getCsv(csvData) {
  myData = csvData;
}

function choose(csvData){
    myData = csvData;
    updateChart(stationNum, "");
}

var chart = new Chart('chart', {
  options: {
    responsive: true,
    maintainAspecRatio: true,
    title: {
      display: true,
      fontSize: 20,
      text: 'Estação Climática ',
    },
    scales:{
        beginAtZero: true,
        yAxes:[{
          scaleLabel: {
            display: true,
            labelString: 'Temperatura Cº',
            fontSize: 15,
          }
        }],
    },
  },
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        display: false,
        label: "",
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
  day = 1;
  date = "0" + day + "/01/2010";
  labels.forEach((lb) => {
    chart.data.labels.push(date);

    day = day + 1;
    if(day <= 9){
      date = "0" + day + "01/2010";
    }else{
      date = day + "/01/2010";
    }

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

function updateChart(id, newTitle){
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

        if (newTitle != ""){
          chart.options.title.text = newTitle;
        }
        chart.update();
}

optTempMax.click(function(){
    fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/f4ce6b69e5d3457ae52215edf57445c4/raw/705cfaf2cb35afc1b595495a7de9ca4b333c800a/tMax-inmet.csv';
    chart.data.datasets[0].label = "Temperaturas Máximas";
    chart.options.scales.yAxes[0].scaleLabel.labelString = "Temperatura Cº";
    d3.csv(fileUrl).then(choose);
});

optTempMin.click(function(){
    fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/208642a743eb6ef0bf649b6f1e1138e3/raw/968676550eb5f0acdba4140f82a79aefe6baf9e0/tMin-inmet.csv';
    chart.data.datasets[0].label = "Temperaturas Mínimas";
    chart.options.scales.yAxes[0].scaleLabel.labelString = "Temperatura Cº";
    d3.csv(fileUrl).then(choose);
});

optSolRad.click(function(){
    fileUrl = 'https://gist.githubusercontent.com/Mr-Saxobeat/afb28a15b4497e6c0ac255779523fb02/raw/27c0b7273acd6b5ce57353f1e00b3bc95ac956f3/sRadiation-inmet.csv';
    chart.data.datasets[0].label = "Radiação Solar";
    chart.options.scales.yAxes[0].scaleLabel.labelString = "Radiação MJ/m²";
    d3.csv(fileUrl).then(choose);
})

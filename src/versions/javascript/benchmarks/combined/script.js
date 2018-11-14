// Adapted from http://www.chartjs.org/samples/latest/charts/line/basic.html

var chartColors = {
      red: 'rgb(255, 99, 132)',
      orange: 'rgb(255, 159, 64)',
      yellow: 'rgb(255, 205, 86)',
      green: 'rgb(75, 192, 192)',
      blue: 'rgb(54, 162, 235)',
      purple: 'rgb(153, 102, 255)',
      grey: 'rgb(201, 203, 207)'
};

var config = {
      type: "line",
      data: {
            labels: [],
            datasets: [{
                  label: "Data",
                  backgroundColor: window.chartColors.red,
                  borderColor: window.chartColors.red,
                  data: [],
                  fill: false,
            }]
      },
      options: {
            responsive: true,
            title: {
                  display: true,
                  text: "Combined Benchmark"
            },
            tooltips: {
                  mode: 'index',
                  intersect: false,
            },
            hover: {
                  mode: 'nearest',
                  intersect: true
            },
            scales: {
                  xAxes: [{
                        display: true,
                        scaleLabel: {
                              display: true,
                              labelString: "x"
                        }
                  }],
                  yAxes: [{
                        display: true,
                        scaleLabel: {
                              display: true,
                              labelString: "y"
                        }
                  }]
            }
      }
};

window.onload = function() {
      var ctx = document.getElementById("canvas").getContext('2d');
      window.chart = new Chart(ctx, config);
};